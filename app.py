import streamlit as st

import motor

st.set_page_config(page_title="Asesor de Inversiones IA", page_icon="📈", layout="centered")

st.title("📈 Asesor de Inversiones con IA")
st.caption(
    "Proyecto académico de Inteligencia Artificial. Responde unas preguntas y recibe "
    "recomendaciones de tipo de activo, plataformas y una proyección estimada."
)

with st.form("formulario"):
    st.subheader("1. Tu inversión")
    primera = st.radio("¿Es tu primera vez invirtiendo?", ["Sí", "No"], horizontal=True)
    monto = st.number_input(
        "¿Cuánto vas a invertir? (USD)", min_value=50.0, max_value=50000.0, value=1000.0, step=50.0
    )
    plazo_meses = st.select_slider(
        "¿A qué plazo?",
        options=[1, 3, 6, 12, 24, 36, 48, 60, 120],
        value=24,
        format_func=lambda m: f"{m} meses" if m < 12 else f"{m // 12} año(s)" if m % 12 == 0 else f"{m} meses",
    )

    st.subheader("2. Tu perfil de riesgo")
    puntos = 0
    for i, (pregunta, opciones) in enumerate(motor.PREGUNTAS):
        etiqueta = st.radio(pregunta, [o[0] for o in opciones], key=f"p{i}")
        puntos += dict(opciones)[etiqueta]

    enviar = st.form_submit_button("Obtener recomendación", type="primary")

if enviar:
    perfil = motor.perfil_desde_puntos(puntos)
    es_primera = primera == "Sí"

    st.success(f"Tu perfil de riesgo es **{perfil}** ({puntos}/15 puntos).")
    for aviso in motor.advertencias(perfil, plazo_meses, monto):
        st.warning(aviso)

    st.subheader("Recomendaciones para ti")
    resultados = motor.recomendar(es_primera, monto, plazo_meses, perfil)

    for n, r in enumerate(resultados, start=1):
        with st.container(border=True):
            st.markdown(f"### {n}. {r['tipo']}")
            c1, c2, c3 = st.columns(3)
            c1.metric("Rendimiento anual esperado", f"{r['rendimiento_anual_pct']:.1f}%")
            c2.metric("Comisión estimada", f"{r['comision_pct']:.2f}%")
            c3.metric("Valor estimado al final", f"${r['valor_final_usd']:,.0f}")
            st.write(f"**Plataformas sugeridas:** {', '.join(r['plataformas'])}")
            st.write(f"Ganancia estimada: **${r['ganancia_usd']:,.0f}** (ya descontada la comisión).")
            st.progress(min(max(r["afinidad"], 0.0), 1.0), text=f"Afinidad con tu caso: {r['afinidad']:.0%}")

    with st.expander("¿Cómo se calculó esto?"):
        m = motor.BUNDLE["metricas"]
        st.markdown(
            f"""
- Tu **perfil** sale del cuestionario (suma de puntos), no se adivina con el monto.
- Un modelo de IA (Gradient Boosting) ordena los activos posibles para tu perfil. La opción correcta
  queda entre las 2 primeras el **{m['tipo_top2']:.0%}** de las veces y entre las 3 primeras el **{m['tipo_top3']:.0%}**.
- Otro modelo estima rendimiento y comisión (R² de {m['rend_r2']:.2f} y {m['com_r2']:.2f}; error promedio de
  {m['rend_mae']:.1f} puntos en rendimiento).
- Valor final = monto × (1 + rendimiento)^(años) − comisión. Es una proyección, no una promesa.
"""
        )

st.divider()
st.caption(
    "⚠️ Herramienta educativa. Los datos de entrenamiento son sintéticos (500 registros) y los resultados "
    "no constituyen asesoría financiera. Consulta a un profesional antes de invertir."
)
