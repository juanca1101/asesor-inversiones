"""Motor de recomendacion: cuestionario de perfil + modelos de ML + reglas de negocio."""
import os
import subprocess
import sys

import joblib
import numpy as np
import pandas as pd

from plataformas import (
    DESCRIPCION_ACTIVO,
    MONEDA_ACTIVO,
    PLATAFORMAS,
    REFERENCIA_COP,
)

# Si no existe modelo.joblib (primer arranque en el servidor), se entrena en segundos.
if not os.path.exists("modelo.joblib"):
    subprocess.run([sys.executable, "entrenar.py"], check=True)
BUNDLE = joblib.load("modelo.joblib")

PERFILES = ["Bajo", "Medio", "Alto"]
TRM_DEFECTO = 3270.0  # TRM aprox. del 10-nov-2026; el usuario puede cambiarla
MONTO_MIN_USD, MONTO_MAX_USD = 50.0, 50000.0  # rango con el que se entreno el modelo
PLAZOS = [1, 3, 6, 12, 24, 36, 48, 60, 120]

# --------------------------------------------------------------- Cuestionario de perfil
# Cada pregunta: (texto, [(opcion, puntos), ...]).  7 preguntas -> 7 a 21 puntos.
PREGUNTAS = [
    (
        "Si tu inversión cae 20% en un mes, ¿qué harías?",
        [("Vendo todo para no perder más", 1), ("Espero y no hago nada", 2), ("Compro más porque está barata", 3)],
    ),
    (
        "¿Cuál es tu objetivo principal con este dinero?",
        [("Cuidarlo, aunque gane poco", 1), ("Que crezca de forma moderada", 2), ("Maximizar la ganancia asumiendo riesgo", 3)],
    ),
    (
        "¿Qué parte de tus ahorros vas a invertir?",
        [("Más de la mitad", 1), ("Entre 20% y 50%", 2), ("Menos del 20%", 3)],
    ),
    (
        "¿Cuánta experiencia tienes invirtiendo?",
        [("Ninguna", 1), ("Algo (fondos, CDT, etc.)", 2), ("Bastante (acciones, ETFs, etc.)", 3)],
    ),
    (
        "¿Cuándo podrías necesitar este dinero?",
        [("Podría necesitarlo pronto", 1), ("Dentro de algunos años", 2), ("No lo necesito en mucho tiempo", 3)],
    ),
    (
        "¿Qué tan estables son tus ingresos?",
        [("Varían mucho", 1), ("Más o menos estables", 2), ("Muy estables", 3)],
    ),
    (
        "¿En qué rango de edad estás?",
        [("Más de 55 años", 1), ("Entre 36 y 55 años", 2), ("Entre 18 y 35 años", 3)],
    ),
]
PUNTOS_MIN, PUNTOS_MAX = len(PREGUNTAS), len(PREGUNTAS) * 3

OBJETIVOS = [
    "Hacer crecer mi dinero",
    "Ahorrar para una meta (viaje, estudio, carro)",
    "Comprar vivienda",
    "Pensión / retiro",
    "Generar un ingreso extra",
]


def perfil_desde_puntos(puntos: int) -> str:
    if puntos <= 11:
        return "Bajo"
    if puntos <= 16:
        return "Medio"
    return "Alto"


DESCRIPCION_PERFIL = {
    "Bajo": "Conservador: priorizas no perder y aceptas ganar menos.",
    "Medio": "Moderado: aceptas altibajos a cambio de un mejor rendimiento.",
    "Alto": "Agresivo: toleras caídas fuertes buscando mayores ganancias.",
}


# --------------------------------------------------------------- Formato y monedas
def a_usd(monto: float, moneda: str, trm: float) -> float:
    return monto if moneda == "USD" else monto / trm


def fmt(valor: float, moneda: str) -> str:
    if moneda == "COP":
        return "$" + f"{valor:,.0f}".replace(",", ".") + " COP"
    return f"US${valor:,.0f}"


def fmt_pct(x: float, dec: int = 1) -> str:
    return f"{x:.{dec}f}%".replace(".", ",")


# --------------------------------------------------------------- Modelo
def _fila(primera_vez: bool, monto_usd: float, plazo: int, perfil: str, tipo: str | None = None) -> pd.DataFrame:
    d = {
        "primera_vez": int(primera_vez),
        "log_monto": np.log(monto_usd),
        "log_plazo": np.log(plazo),
    }
    for p in PERFILES:
        d[f"perfil_{p}"] = int(perfil == p)
    if tipo is not None:
        for t in BUNDLE["tipos"]:
            d[f"tipo_{t}"] = int(tipo == t)
        return pd.DataFrame([d], columns=BUNDLE["columnas_xt"])
    return pd.DataFrame([d], columns=BUNDLE["columnas_x"])


def _factor_moneda(tipo: str, preferencia: str) -> float:
    """Ajusta la afinidad segun la moneda preferida (soft: no elimina, reordena)."""
    if preferencia == "Me da igual":
        return 1.0
    objetivo = "COP" if preferencia == "Pesos" else "USD"
    m = MONEDA_ACTIVO[tipo]
    if m == objetivo:
        return 1.0
    if m == "Mixta":
        return 0.8
    return 0.35


ENTIDAD_LOCAL = "Solo entidades colombianas vigiladas"
ENTIDAD_INTERNACIONAL = "Prefiero plataformas internacionales"
ENTIDAD_IGUAL = "Me da igual"


def plataformas_para(tipo: str, preferencia_entidad: str, monto_usd: float, n: int = 4) -> list[dict]:
    prior = BUNDLE["plataformas"].get(tipo, {})
    cands = []
    for p in PLATAFORMAS:
        if tipo not in p["tipos"]:
            continue
        if preferencia_entidad == ENTIDAD_LOCAL and not p["vigilada_sfc"]:
            continue
        if preferencia_entidad == ENTIDAD_INTERNACIONAL and p["origen"] == "Colombia":
            continue
        alcanza = monto_usd >= p["min_usd"]
        score = prior.get(p["nombre"], 0.0) + 0.05 + (0.0 if alcanza else -1.0)
        cands.append((score, alcanza, p))
    if any(alc for _, alc, _ in cands):
        cands = [c for c in cands if c[1]]  # solo las que aceptan tu monto
    cands.sort(key=lambda x: -x[0])
    return [dict(p, alcanza_minimo=alc) for _, alc, p in cands[:n]]


def proyeccion(monto: float, aporte_mensual: float, rend_anual_pct: float, comision_pct: float, plazo: int) -> pd.DataFrame:
    """Valor mes a mes en la moneda del usuario. Comision = % de lo depositado (aprox.)."""
    i = (1 + rend_anual_pct / 100) ** (1 / 12) - 1
    filas = []
    saldo = monto
    aportado = monto
    for m in range(0, plazo + 1):
        if m > 0:
            saldo = saldo * (1 + i) + aporte_mensual
            aportado += aporte_mensual
        filas.append(
            {
                "mes": m,
                "Con tu inversión": saldo - aportado * comision_pct / 100,
                "Solo lo que aportas": aportado,
            }
        )
    return pd.DataFrame(filas).set_index("mes")


def recomendar(
    primera_vez: bool,
    monto: float,
    moneda: str,
    trm: float,
    plazo: int,
    perfil: str,
    pref_moneda: str = "Me da igual",
    pref_entidad: str = ENTIDAD_IGUAL,
    aporte_mensual: float = 0.0,
    n: int = 3,
) -> dict:
    monto_usd = a_usd(monto, moneda, trm)
    monto_modelo = float(np.clip(monto_usd, MONTO_MIN_USD, MONTO_MAX_USD))

    X = _fila(primera_vez, monto_modelo, plazo, perfil)
    proba = BUNDLE["clf_tipo"].predict_proba(X)[0]
    clases = BUNDLE["clases"]
    permitidos = np.isin(clases, BUNDLE["tipos_por_perfil"][perfil])
    p = np.where(permitidos, proba, 0.0)

    omitidos = []
    for i, tipo in enumerate(clases):
        if not permitidos[i]:
            continue
        # Sin plataformas con tu preferencia (ej. cripto + "solo vigiladas") se omite el activo
        if not plataformas_para(tipo, pref_entidad, monto_usd):
            p[i] = 0.0
            omitidos.append(str(tipo))
            continue
        p[i] *= _factor_moneda(tipo, pref_moneda)

    if p.sum() == 0:  # caso extremo: volver al ranking original
        p = np.where(permitidos, proba, 0.0)
    p = p / p.sum()
    orden = [i for i in np.argsort(-p) if p[i] >= 0.03][:n] or [int(np.argmax(p))]  # sin opciones con afinidad ~0

    resultados = []
    for i in orden:
        tipo = str(clases[i])
        Xt = _fila(primera_vez, monto_modelo, plazo, perfil, tipo)
        rend = float(BUNDLE["reg_rend"].predict(Xt)[0])
        com = max(0.0, float(BUNDLE["reg_com"].predict(Xt)[0]))
        serie = proyeccion(monto, aporte_mensual, rend, com, plazo)
        total_aportado = monto + aporte_mensual * plazo
        valor_final = float(serie["Con tu inversión"].iloc[-1])
        resultados.append(
            {
                "tipo": tipo,
                "descripcion": DESCRIPCION_ACTIVO[tipo],
                "afinidad": float(p[i]),
                "moneda_activo": MONEDA_ACTIVO[tipo],
                "rendimiento_anual_pct": rend,
                "comision_pct": com,
                "plataformas": plataformas_para(tipo, pref_entidad, monto_usd),
                "referencia_cop": REFERENCIA_COP.get(tipo),
                "total_aportado": total_aportado,
                "valor_final": valor_final,
                "ganancia": valor_final - total_aportado,
                "serie": serie,
            }
        )
    return {
        "resultados": resultados,
        "omitidos": omitidos,
        "monto_usd": monto_usd,
        "monto_ajustado": monto_modelo != monto_usd,
    }


# --------------------------------------------------------------- Consejos segun contexto
def advertencias(
    perfil: str,
    plazo: int,
    monto_usd: float,
    objetivo: str,
    tiene_fondo_emergencia: bool,
    tiene_deudas_caras: bool,
    moneda_monto: str,
    pref_moneda: str,
    trm: float | None = None,
) -> list[tuple[str, str]]:
    """Lista de (nivel, mensaje). nivel: 'alto' | 'medio' | 'info'."""
    av = []
    if tiene_deudas_caras:
        av.append(("alto", "Tienes deudas con intereses altos: pagarlas suele rendir más que casi cualquier inversión. Considera destinar primero ese dinero a la deuda."))
    if not tiene_fondo_emergencia:
        av.append(("alto", "Aún no tienes fondo de emergencia. Lo ideal es reservar 3 a 6 meses de gastos en algo líquido antes de invertir a largo plazo."))
    if perfil == "Alto" and plazo < 12:
        av.append(("medio", "Un perfil agresivo a menos de 12 meses es muy volátil: el valor puede bajar bastante en ese tiempo."))
    if perfil == "Bajo" and plazo > 60:
        av.append(("info", "Con un plazo tan largo, un perfil muy conservador podría quedar por debajo de la inflación."))
    if objetivo == "Comprar vivienda" and plazo <= 24 and perfil != "Bajo":
        av.append(("medio", "Si necesitarás el dinero pronto para una vivienda, evita activos que puedan caer justo cuando vayas a vender."))
    if monto_usd < 100:
        base = "Con montos pequeños las comisiones fijas pesan mucho. "
        if trm:
            pct = 14900 / (monto_usd * trm) * 100
            base += f"Por ejemplo, la tarifa fija de ~$14.900 COP de comprar acciones en una app como Trii equivaldría a ~{pct:.0f}% de tu monto. "
        base += "Con poco dinero suelen convenir los fondos de inversión colectiva (sin cobro por operación) o juntar varios aportes antes de comprar."
        av.append(("medio", base))
    if (moneda_monto == "COP" and pref_moneda == "Dólares") or (moneda_monto == "USD" and pref_moneda == "Pesos"):
        av.append(("info", "Cambiar de moneda tiene costo (comisión y diferencia entre compra y venta) y riesgo cambiario: si el dólar se mueve contra ti, tu ganancia cambia."))
    return av
