import streamlit as st
import motor
from estilos import CSS
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Asesor de Inversiones IA",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.markdown(CSS, unsafe_allow_html=True)

def html(texto: str) -> None:
    st.markdown(texto, unsafe_allow_html=True)

def main():
    html('<div class="hero"><h1>🤖 Asesor Inteligente de Inversiones</h1><p>Configura tu perfil para obtener opciones de mercado basadas en IA.</p></div>')
    
    st.subheader("1. Configura tu Inversión")
    
    # Selectbox con placeholder "Elige una opción"
    primera = st.selectbox("¿Es tu primera vez invirtiendo?", ["Sí, es mi primera vez", "No, ya he invertido antes"], index=None, placeholder="Elige una opción")
    objetivo = st.selectbox("¿Para qué quieres invertir?", motor.OBJETIVOS, index=None, placeholder="Elige una opción")
    moneda_txt = st.selectbox("¿En qué moneda prefieres invertir?", ["Pesos Colombianos (COP)", "Dólares (USD)"], index=None, placeholder="Elige una opción")
    plazo_txt = st.selectbox("¿A qué plazo?", options=motor.PLAZOS, format_func=lambda x: f"{x} meses" if x > 1 else "1 mes", index=None, placeholder="Elige una opción")

    moneda = "COP" if moneda_txt == "Pesos Colombianos (COP)" else "USD" if moneda_txt == "Dólares (USD)" else None
    
    monto, aporte = None, None
    if moneda == "COP":
        monto = st.number_input("Monto inicial a invertir (COP)", min_value=0, step=50000, value=None, placeholder="Ej: 100000")
        if monto is not None:
            st.caption(f"💰 Monto registrado: **${monto:,.0f} COP**".replace(",", "."))
            
        aporte = st.number_input("Aporte mensual estimado (COP)", min_value=0, step=10000, value=None, placeholder="Ej: 50000")
        if aporte is not None:
            st.caption(f"🔄 Aporte mensual: **${aporte:,.0f} COP**".replace(",", "."))
            
    elif moneda == "USD":
        monto = st.number_input("Monto inicial a invertir (USD)", min_value=0, step=50, value=None, placeholder="Ej: 100")
        if monto is not None:
            st.caption(f"💰 Monto registrado: **${monto:,.0f} USD**".replace(",", "."))
            
        aporte = st.number_input("Aporte mensual estimado (USD)", min_value=0, step=10, value=None, placeholder="Ej: 50")
        if aporte is not None:
            st.caption(f"🔄 Aporte mensual: **${aporte:,.0f} USD**".replace(",", "."))
        
    st.markdown("---")
    st.subheader("2. Test de Riesgo")
    
    resp_actualizadas = []
    for i, (pregunta, opciones) in enumerate(motor.PREGUNTAS):
        textos = [o for o, _ in opciones]
        r = st.selectbox(pregunta, textos, index=None, key=f"p_{i}", placeholder="Elige una opción")
        resp_actualizadas.append(r)
        
    st.markdown("---")
    
    # Validación ESTRICTA para evitar que el programa se rompa
    campos_llenos = (
        primera is not None and 
        objetivo is not None and 
        moneda is not None and 
        plazo_txt is not None and 
        monto is not None and 
        all(r is not None for r in resp_actualizadas)
    )
    
    # Lógica Visual: Le indicamos al usuario qué debe hacer antes de poder presionar el botón
    if not campos_llenos:
        st.info("💡 Faltan campos por llenar. Completa todas las preguntas y el monto inicial para habilitar el análisis.")
        
    # El botón estará literalmente DESACTIVADO (gris) hasta que 'campos_llenos' sea True
    if st.button("Analizar Portafolio", disabled=not campos_llenos):
        with st.spinner("Analizando miles de registros..."):
            puntos = sum(dict(o)[r] for (_, o), r in zip(motor.PREGUNTAS, resp_actualizadas))
            perfil = motor.perfil_desde_puntos(puntos)
            
            # El motor ya recibe la data validada 100% segura
            out = motor.recomendar(
                monto, aporte if aporte is not None else 0,
                plazo_txt, moneda,
                puntos, objetivo,
                primera == "Sí, es mi primera vez",
                True, "Ambas", motor.TRM_DEFECTO
            )
            
            st.markdown(f"### Tu Perfil: **{perfil}** (Puntaje: {puntos})")
            
            for r in out["recomendaciones"]:
                act = r['activo']
                pos = "pos" if r['ganancia'] > 0 else ""
                html(f"""
                <div class="card">
                  <div class="card-header">
                    <h3 class="card-title">{act['nombre']}</h3>
                    <span class="badge { 'b-cop' if act['moneda'] == 'COP' else 'b-usd' }">{act['moneda']}</span>
                  </div>
                  <div class="metric-grid">
                    <div class="metric"><div class="lbl">Tasa Esperada</div><div class="val">{motor.fmt_pct(r['rendimiento_anual_pct'])}</div></div>
                    <div class="metric"><div class="lbl">Comisión (Estimada)</div><div class="val">{motor.fmt_pct(r['comision_pct'], 2)}</div></div>
                    <div class="metric"><div class="lbl">Valor Final Estimado</div><div class="val {pos}">{motor.fmt(r['valor_final'], act['moneda'])}</div></div>
                  </div>
                  <div class="small">Aportando {motor.fmt(r['total_aportado'], act['moneda'])}, tu ganancia limpia estimada es de <b>{motor.fmt(r['ganancia'], act['moneda'])}</b>.</div>
                </div>
                """)
                
            st.markdown("#### Proyección de Crecimiento")
            if out["recomendaciones"]:
                mejor_opcion = out["recomendaciones"][0]
                meses = pd.date_range(start="2026-01-01", periods=plazo_txt, freq="ME")
                
                capital = [monto]
                for i in range(1, plazo_txt):
                    capital.append(capital[-1] * (1 + (mejor_opcion['rendimiento_anual_pct']/12)) + (aporte if aporte else 0))
                
                df_graf = pd.DataFrame({"Mes": meses, "Capital Proyectado": capital}).set_index("Mes")
                st.area_chart(df_graf, color="#3b82f6")

if __name__ == "__main__":
    main()