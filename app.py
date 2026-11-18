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
# Cargamos tus estilos que ya estaban perfectos
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
            
        aporte = st.number_input("Aporte mensual estimado (COP, opcional)", min_value=0, step=10000, value=None, placeholder="Ej: 50000")
        if aporte is not None:
            st.caption(f"🔄 Aporte mensual: **${aporte:,.0f} COP**".replace(",", "."))
            
    elif moneda == "USD":
        monto = st.number_input("Monto inicial a invertir (USD)", min_value=0, step=50, value=None, placeholder="Ej: 100")
        if monto is not None:
            st.caption(f"💰 Monto registrado: **${monto:,.0f} USD**".replace(",", "."))
            
        aporte = st.number_input("Aporte mensual estimado (USD, opcional)", min_value=0, step=10, value=None, placeholder="Ej: 50")
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
    
    campos_llenos = (
        primera is not None and 
        objetivo is not None and 
        moneda is not None and 
        plazo_txt is not None and 
        monto is not None and 
        all(r is not None for r in resp_actualizadas)
    )
    
    if not campos_llenos:
        st.info("💡 Faltan campos por llenar. Completa todas las preguntas y el monto inicial para habilitar el análisis.")
        
    if st.button("Analizar Portafolio", disabled=not campos_llenos):
        with st.spinner("Analizando opciones en las plataformas..."):
            puntos = sum(dict(o)[r] for (_, o), r in zip(motor.PREGUNTAS, resp_actualizadas))
            perfil = motor.perfil_desde_puntos(puntos)
            
            # Conexión exacta a tu motor de inteligencia
            out = motor.recomendar(
                primera_vez=(primera == "Sí, es mi primera vez"),
                monto=float(monto),
                moneda=moneda,
                trm=motor.TRM_DEFECTO,
                plazo=plazo_txt,
                perfil=perfil,
                pref_moneda="Me da igual",
                pref_entidad=motor.ENTIDAD_IGUAL,
                aporte_mensual=float(aporte) if aporte is not None else 0.0
            )
            
            st.markdown(f"### Tu Perfil IA: **{perfil}** (Puntaje: {puntos})")
            st.markdown("A continuación, te detallamos las carteras exactas, cuánto ganarás y qué aplicaciones usar:")
            
            # Recorremos cada tipo de activo recomendado
            for i, r in enumerate(out["resultados"]):
                act_tipo = r['tipo']
                
                # Cálculos exactos según el modelo
                tasa_esp = r['rendimiento_anual_pct']
                com_esp = r['comision_pct']
                val_fin = r['valor_final']
                aportado = r['total_aportado']
                ganancia_neta = r['ganancia']
                
                # Desglose de ganancia bruta vs retenciones/comisiones
                descuento = aportado * (com_esp / 100)
                ganancia_bruta = ganancia_neta + descuento

                # Mostramos la tarjeta principal (Categoría)
                html(f"""
                <div class="card" style="margin-bottom: 5px;">
                  <div class="card-header" style="margin-bottom: 5px;">
                    <h3 class="card-title">Opción {i+1}: {act_tipo}</h3>
                    <span class="badge { 'b-cop' if r['moneda_activo'] == 'COP' else 'b-usd' }">{r['moneda_activo']}</span>
                  </div>
                  <p style="margin-top:0; color: #475569;">{r['descripcion']}</p>
                </div>
                """)
                
                plataformas = r.get('plataformas', [])
                if not plataformas:
                    st.info("No encontramos una aplicación vigilada para esta opción con tus filtros.")
                    continue
                
                # Creamos las pestañas por cada aplicación disponible
                tabs = st.tabs([p['nombre'] for p in plataformas])
                
                # Llenamos cada pestaña con la info específica y su gráfico
                for idx, p in enumerate(plataformas):
                    with tabs[idx]:
                        col_izq, col_der = st.columns([1, 1.2])
                        with col_izq:
                            st.write(f"**📱 App/Banco:** {p['nombre']}")
                            st.write(f"**🎯 ¿En qué inviertes aquí?:** {p['ofrece']}")
                            st.write(f"**💸 Costos/Comisiones reales:** {p['costos']}")
                            
                            st.markdown("---")
                            st.markdown("**💰 Tus números exactos:**")
                            st.write(f"Tu Capital Aportado: **{motor.fmt(aportado, moneda)}**")
                            st.write(f"Ganancia Bruta: **+ {motor.fmt(ganancia_bruta, moneda)}**")
                            st.write(f"Descuento (Comisión/Impuesto): **- {motor.fmt(descuento, moneda)}**")
                            st.markdown(f"#### Libre para ti: <span style='color:#059669'>**{motor.fmt(val_fin, moneda)}**</span>", unsafe_allow_html=True)

                        with col_der:
                            # Generamos el gráfico individual para esta pestaña
                            df_serie = r['serie'].copy()
                            df_serie.rename(columns={
                                "Con tu inversión": f"Proyección en {p['nombre']}",
                                "Solo lo que aportas": "Dinero de tu bolsillo"
                            }, inplace=True)
                            
                            st.area_chart(df_serie, color=["#0ea5e9", "#94a3b8"])
                
                st.markdown("<br><hr><br>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()