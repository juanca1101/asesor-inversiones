"""Motor de recomendacion: cuestionario de perfil + modelos de ML."""
import os
import subprocess
import sys

import joblib
import numpy as np
import pandas as pd

# Si no existe modelo.joblib (primer arranque en el servidor), se entrena en segundos.
if not os.path.exists("modelo.joblib"):
    subprocess.run([sys.executable, "entrenar.py"], check=True)
BUNDLE = joblib.load("modelo.joblib")
PERFILES = ["Bajo", "Medio", "Alto"]

# --------------------------------------------------------------- Cuestionario de perfil
# Cada pregunta: (texto, [(opcion, puntos), ...]).  Suma 5-15 puntos.
PREGUNTAS = [
    (
        "Si tu inversion cae 20% en un mes, ¿que harias?",
        [("Vendo todo para no perder mas", 1), ("Espero y no hago nada", 2), ("Compro mas porque esta barata", 3)],
    ),
    (
        "¿Cual es tu objetivo principal?",
        [("Cuidar mi dinero, aunque gane poco", 1), ("Que crezca de forma moderada", 2), ("Maximizar la ganancia, asumiendo riesgo", 3)],
    ),
    (
        "¿Que parte de tus ahorros vas a invertir?",
        [("Mas de la mitad", 1), ("Entre 20% y 50%", 2), ("Menos del 20%", 3)],
    ),
    (
        "¿Cuanta experiencia tienes invirtiendo?",
        [("Ninguna", 1), ("Algo (fondos, CDT, etc.)", 2), ("Bastante (acciones, ETFs, etc.)", 3)],
    ),
    (
        "¿Cuando podrias necesitar este dinero?",
        [("Podria necesitarlo pronto", 1), ("Dentro de algunos años", 2), ("No lo necesito en mucho tiempo", 3)],
    ),
]


def perfil_desde_puntos(puntos: int) -> str:
    if puntos <= 8:
        return "Bajo"
    if puntos <= 12:
        return "Medio"
    return "Alto"


# --------------------------------------------------------------- Recomendacion
def _fila(primera_vez: bool, monto: float, plazo: int, perfil: str, tipo: str | None = None) -> pd.DataFrame:
    d = {
        "primera_vez": int(primera_vez),
        "log_monto": np.log(monto),
        "log_plazo": np.log(plazo),
    }
    for p in PERFILES:
        d[f"perfil_{p}"] = int(perfil == p)
    if tipo is not None:
        for t in BUNDLE["tipos"]:
            d[f"tipo_{t}"] = int(tipo == t)
        return pd.DataFrame([d], columns=BUNDLE["columnas_xt"])
    return pd.DataFrame([d], columns=BUNDLE["columnas_x"])


def recomendar(primera_vez: bool, monto: float, plazo: int, perfil: str, n: int = 3) -> list[dict]:
    """Devuelve hasta `n` opciones ordenadas por probabilidad, con estimaciones."""
    X = _fila(primera_vez, monto, plazo, perfil)
    proba = BUNDLE["clf_tipo"].predict_proba(X)[0]
    clases = BUNDLE["clases"]
    permitidos = np.isin(clases, BUNDLE["tipos_por_perfil"][perfil])
    p = np.where(permitidos, proba, 0.0)
    p = p / p.sum()
    orden = np.argsort(-p)[:n]

    resultados = []
    for i in orden:
        tipo = clases[i]
        Xt = _fila(primera_vez, monto, plazo, perfil, tipo)
        rend = float(BUNDLE["reg_rend"].predict(Xt)[0])
        com = max(0.0, float(BUNDLE["reg_com"].predict(Xt)[0]))
        plats = BUNDLE["plataformas"][tipo]
        top_plats = sorted(plats.items(), key=lambda kv: -kv[1])[:2]
        costo_com = monto * com / 100
        valor_final = monto * (1 + rend / 100) ** (plazo / 12) - costo_com
        resultados.append(
            {
                "tipo": tipo,
                "afinidad": float(p[i]),
                "rendimiento_anual_pct": rend,
                "comision_pct": com,
                "plataformas": [x[0] for x in top_plats],
                "costo_comision_usd": costo_com,
                "valor_final_usd": valor_final,
                "ganancia_usd": valor_final - monto,
            }
        )
    return resultados


def advertencias(perfil: str, plazo: int, monto: float) -> list[str]:
    av = []
    if perfil == "Alto" and plazo < 12:
        av.append("Un perfil agresivo a menos de 12 meses es muy volatil: el valor puede bajar bastante en ese tiempo.")
    if perfil == "Bajo" and plazo > 60:
        av.append("Con un plazo tan largo, un perfil muy conservador podria quedar por debajo de la inflacion.")
    if monto < 100:
        av.append("Con montos pequeños las comisiones minimas de algunas plataformas pesan mas en el resultado.")
    return av
