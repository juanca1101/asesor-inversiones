"""Entrena los modelos del Asesor de Inversiones y los guarda en modelo.joblib.

Uso:  python entrenar.py
"""
import warnings

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_predict
from sklearn.metrics import mean_absolute_error, r2_score, top_k_accuracy_score

warnings.filterwarnings("ignore")

df = pd.read_csv("dataset_asesor_inversiones_500.csv")

PERFILES = ["Bajo", "Medio", "Alto"]
TIPOS_POR_PERFIL = (
    df.groupby("perfil_riesgo")["tipo_activo_recomendado"]
    .unique()
    .apply(sorted)
    .to_dict()
)
TIPOS = sorted(df["tipo_activo_recomendado"].unique())


def features(d: pd.DataFrame) -> pd.DataFrame:
    """Convierte las respuestas del usuario en columnas numericas."""
    out = pd.DataFrame(index=d.index)
    out["primera_vez"] = (d["es_primera_vez_invirtiendo"] == "Si").astype(int)
    out["log_monto"] = np.log(d["monto_inversion_usd"])
    out["log_plazo"] = np.log(d["plazo_meses"])
    for p in PERFILES:
        out[f"perfil_{p}"] = (d["perfil_riesgo"] == p).astype(int)
    return out


def features_con_tipo(d: pd.DataFrame) -> pd.DataFrame:
    out = features(d)
    for t in TIPOS:
        out[f"tipo_{t}"] = (d["tipo_activo_recomendado"] == t).astype(int)
    return out


X = features(df)
Xt = features_con_tipo(df)

# ---------------------------------------------------------------- 1) Tipo de activo
# Se predice DENTRO del perfil de riesgo (cada perfil tiene solo 3 activos posibles).
clf_tipo = GradientBoostingClassifier(n_estimators=60, max_depth=2, random_state=42)
cv = StratifiedKFold(5, shuffle=True, random_state=42)
proba = cross_val_predict(clf_tipo, X, df["tipo_activo_recomendado"], cv=cv, method="predict_proba")
clases = np.array(sorted(df["tipo_activo_recomendado"].unique()))

top1, top2, top3 = [], [], []
for i, perfil in enumerate(df["perfil_riesgo"]):
    permitidos = np.isin(clases, TIPOS_POR_PERFIL[perfil])
    p = np.where(permitidos, proba[i], 0)
    orden = clases[np.argsort(-p)]
    real = df["tipo_activo_recomendado"].iloc[i]
    top1.append(orden[0] == real)
    top2.append(real in orden[:2])
    top3.append(real in orden[:3])
metricas = {
    "tipo_top1": float(np.mean(top1)),
    "tipo_top2": float(np.mean(top2)),
    "tipo_top3": float(np.mean(top3)),
}
clf_tipo.fit(X, df["tipo_activo_recomendado"])

# ---------------------------------------------------------------- 2) Rendimiento y comision
kf = KFold(5, shuffle=True, random_state=42)
reg_rend = GradientBoostingRegressor(n_estimators=150, max_depth=3, learning_rate=0.05, random_state=42)
reg_com = GradientBoostingRegressor(n_estimators=150, max_depth=3, learning_rate=0.05, random_state=42)
for nombre, reg, col in [("rend", reg_rend, "rendimiento_esperado_pct"), ("com", reg_com, "comision_pct")]:
    pred = cross_val_predict(reg, Xt, df[col], cv=kf)
    metricas[f"{nombre}_r2"] = float(r2_score(df[col], pred))
    metricas[f"{nombre}_mae"] = float(mean_absolute_error(df[col], pred))
    reg.fit(Xt, df[col])

# ---------------------------------------------------------------- 3) Plataformas por tipo
plataformas = {}
for tipo, g in df.groupby("tipo_activo_recomendado"):
    plataformas[tipo] = g["plataforma_recomendada"].value_counts(normalize=True).round(3).to_dict()

# ---------------------------------------------------------------- 4) Cuestionario de perfil
# El perfil se obtiene del cuestionario (no se "adivina" desde monto y plazo:
# en el dataset el monto no tiene relacion con el perfil y el plazo da un techo ~57%).
joblib.dump(
    {
        "clf_tipo": clf_tipo,
        "reg_rend": reg_rend,
        "reg_com": reg_com,
        "clases": clases,
        "tipos_por_perfil": TIPOS_POR_PERFIL,
        "plataformas": plataformas,
        "columnas_x": list(X.columns),
        "columnas_xt": list(Xt.columns),
        "tipos": TIPOS,
        "metricas": metricas,
    },
    "modelo.joblib",
)

print("Metricas (validacion cruzada de 5 particiones):")
for k, v in metricas.items():
    print(f"  {k}: {v:.3f}")
