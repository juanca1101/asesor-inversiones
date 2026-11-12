"""Amplia el dataset original (500 filas) a 2000 filas con datos SIMULADOS.

- Conserva las 500 filas originales (fuente = "original").
- Agrega 1500 filas nuevas (fuente = "simulado") que respetan la estructura estadistica del original:
    * el perfil se reparte igual que en el original,
    * el plazo depende del perfil (el perfil Bajo nunca llega a 36 meses o mas),
    * el monto NO depende del perfil (igual que en el original),
    * el tipo de activo depende del perfil (y un poco del plazo),
    * rendimiento y comision dependen del tipo de activo y del plazo, con ruido.
- Incorpora 2 tipos de activo nuevos y 7 entidades nuevas (Nu Colombia, Pibank, Davivienda,
  Porvenir, Proteccion, Wenia, Bitso). Los pesos con que se asignan son SUPUESTOS de simulacion,
  no participaciones de mercado reales.

Importante: como los datos son simulados, ampliar el dataset NO hace al modelo mas preciso en el mundo
real; sirve para tener mas ejemplos y cubrir mas opciones. El ruido aleatorio se mantiene a proposito
para que las metricas sigan siendo honestas.

Uso:  python generar_dataset.py
"""
import numpy as np
import pandas as pd

RNG = np.random.default_rng(2026)
N_TOTAL = 2000

orig = pd.read_csv("dataset_asesor_inversiones_500.csv")
orig["fuente"] = "original"
N_NUEVAS = N_TOTAL - len(orig)

PERFILES = ["Alto", "Medio", "Bajo"]
TIPOS_ORIG_POR_PERFIL = orig.groupby("perfil_riesgo")["tipo_activo_recomendado"].unique().apply(list).to_dict()

# ---------------------------------------------------------------- 1) distribuciones aprendidas del original
p_perfil = orig["perfil_riesgo"].value_counts(normalize=True)
p_primera = (
    orig.groupby("perfil_riesgo")["es_primera_vez_invirtiendo"].value_counts(normalize=True).unstack(fill_value=0)
)
p_plazo = {
    pf: g["plazo_meses"].value_counts(normalize=True).sort_index() for pf, g in orig.groupby("perfil_riesgo")
}
montos = orig["monto_inversion_usd"].value_counts(normalize=True).sort_index()


def corto(plazo: int) -> str:
    return "corto" if plazo <= 12 else "largo"


# P(tipo | perfil, plazo corto/largo) con suavizado dentro de los tipos observados
p_tipo = {}
for pf in PERFILES:
    for b in ("corto", "largo"):
        sub = orig[(orig["perfil_riesgo"] == pf) & (orig["plazo_meses"].map(corto) == b)]
        cuentas = sub["tipo_activo_recomendado"].value_counts().reindex(TIPOS_ORIG_POR_PERFIL[pf], fill_value=0) + 1.0
        p_tipo[(pf, b)] = cuentas / cuentas.sum()

p_plat = {t: g["plataforma_recomendada"].value_counts(normalize=True) for t, g in orig.groupby("tipo_activo_recomendado")}

# rendimiento y comision ~ a + b*log(plazo) por tipo, con ruido normal (residuos del original)
modelo_rc = {}
for t, g in orig.groupby("tipo_activo_recomendado"):
    x = np.log(g["plazo_meses"].to_numpy())
    params = {}
    for col in ("rendimiento_esperado_pct", "comision_pct"):
        b, a = np.polyfit(x, g[col].to_numpy(), 1)
        resid = g[col].to_numpy() - (a + b * x)
        params[col] = (a, b, resid.std(ddof=2))
    modelo_rc[t] = params

# ---------------------------------------------------------------- 2) tipos nuevos (supuestos de simulacion)
NUEVO_BAJO = "Cuenta de Ahorro Remunerada"
NUEVO_MEDIO = "Fondo de Pensión Voluntaria"


def prob_cuenta_remunerada(plazo: int, primera: bool, monto: int) -> float:
    p = 0.32 if plazo <= 12 else 0.10
    p += 0.08 if primera else 0.0
    p += 0.10 if monto <= 200 else 0.0
    return min(p, 0.6)


def prob_pension(plazo: int) -> float:
    if plazo >= 60:
        return 0.28
    if plazo >= 36:
        return 0.20
    if plazo >= 24:
        return 0.10
    return 0.04


# a + b*log(plazo) y desviacion para los tipos nuevos (misma escala que el dataset original)
NUEVOS_RC = {
    NUEVO_BAJO: {"rendimiento_esperado_pct": (4.6, 0.12, 0.7), "comision_pct": (0.06, 0.0, 0.04)},
    NUEVO_MEDIO: {"rendimiento_esperado_pct": (7.2, 0.45, 1.3), "comision_pct": (1.3, 0.0, 0.3)},
}

# ---------------------------------------------------------------- 3) entidades nuevas por tipo (pesos supuestos)
# Para cada tipo: probabilidad de que la fila use una entidad NUEVA y como se reparte entre ellas.
PLAT_NUEVAS = {
    "CDT": (0.45, {"Nu Colombia": 0.34, "Pibank": 0.30, "Davivienda": 0.20, "Trii": 0.16}),
    "Bonos de Gobierno": (0.15, {"Trii": 1.0}),
    "Fondo de Deuda": (0.20, {"Davivienda": 0.6, "Trii": 0.4}),
    "Carteras Colectivas": (0.30, {"Davivienda": 0.5, "tyba": 0.5}),
    "Criptomonedas": (0.30, {"Wenia": 0.55, "Bitso": 0.45}),
    NUEVO_BAJO: (1.0, {"Nu Colombia": 0.40, "Lulo Bank": 0.25, "Pibank": 0.20, "Davivienda": 0.15}),
    NUEVO_MEDIO: (1.0, {"Porvenir": 0.34, "Protección": 0.30, "Davivienda": 0.20, "tyba": 0.16}),
}


def elegir(serie_o_dict):
    if isinstance(serie_o_dict, dict):
        nombres, probs = list(serie_o_dict.keys()), np.array(list(serie_o_dict.values()), dtype=float)
    else:
        nombres, probs = list(serie_o_dict.index), serie_o_dict.to_numpy(dtype=float)
    return RNG.choice(nombres, p=probs / probs.sum())


def plataforma(tipo: str) -> str:
    if tipo in PLAT_NUEVAS:
        prob_nueva, pesos = PLAT_NUEVAS[tipo]
        if RNG.random() < prob_nueva:
            return elegir(pesos)
    return elegir(p_plat[tipo])


def rc(tipo: str, plazo: int):
    fuente = NUEVOS_RC.get(tipo) or modelo_rc[tipo]
    x = np.log(plazo)
    out = []
    for col, minimo in (("rendimiento_esperado_pct", 0.5), ("comision_pct", 0.0)):
        a, b, s = fuente[col]
        out.append(round(max(minimo, a + b * x + RNG.normal(0, s)), 2))
    return out


# ---------------------------------------------------------------- 4) generar filas
filas = []
for _ in range(N_NUEVAS):
    perfil = elegir(p_perfil)
    primera = elegir(p_primera.loc[perfil])
    plazo = int(elegir(p_plazo[perfil]))
    monto = int(elegir(montos))

    tipo = None
    if perfil == "Bajo" and RNG.random() < prob_cuenta_remunerada(plazo, primera == "Si", monto):
        tipo = NUEVO_BAJO
    elif perfil == "Medio" and RNG.random() < prob_pension(plazo):
        tipo = NUEVO_MEDIO
    if tipo is None:
        tipo = elegir(p_tipo[(perfil, corto(plazo))])

    rend, com = rc(tipo, plazo)
    filas.append(
        {
            "es_primera_vez_invirtiendo": primera,
            "monto_inversion_usd": monto,
            "plazo_meses": plazo,
            "perfil_riesgo": perfil,
            "tipo_activo_recomendado": tipo,
            "plataforma_recomendada": plataforma(tipo),
            "comision_pct": com,
            "rendimiento_esperado_pct": rend,
            "fuente": "simulado",
        }
    )

nuevo = pd.DataFrame(filas)
df = pd.concat([orig, nuevo], ignore_index=True).sample(frac=1, random_state=7).reset_index(drop=True)
df.to_csv("dataset_asesor_inversiones_2000.csv", index=False)

print(f"Filas: {len(df)}  (original: {(df.fuente == 'original').sum()}, simulado: {(df.fuente == 'simulado').sum()})")
print(df["perfil_riesgo"].value_counts(normalize=True).round(3).to_dict())
print(df["tipo_activo_recomendado"].value_counts().to_dict())
print(df["plataforma_recomendada"].value_counts().to_dict())
