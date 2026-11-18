import streamlit as st
import motor
from estilos import CSS
import pandas as pd
import numpy as np
import requests

st.set_page_config(
    page_title="Asesor de Inversiones IA",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.markdown(CSS, unsafe_allow_html=True)

def html(texto: str) -> None:
    st.markdown(texto, unsafe_allow_html=True)

# ---------------------------------------------------------
# NUEVO: CONEXIÓN EN VIVO A LA TASA DEL DÓLAR (INTERNET)
# ---------------------------------------------------------
@st.cache_data(ttl=3600) # Se actualiza cada hora para que la app sea rápida
def obtener_trm_actual():
    try:
        # API gratuita que devuelve la tasa del Dólar global
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        respuesta = requests.get(url, timeout=5)
        datos = respuesta.json()
        return float(datos['rates']['COP'])
    except Exception:
        # Si no hay internet, usa el por defecto del motor
        return motor.TRM_DEFECTO

# Diccionario inteligente para dar nombres reales
EJEMPLOS_ESPECIFICOS = {
    ("Trii", "Acciones Individuales"): "Acciones locales: Ecopetrol, Bancolombia, ISA, Grupo Argos, Nu Holdings.",
    ("Trii", "ETFs"): "iShares COLCAP (Mercado local), ETF S&P 500 (Mercado Global).",
    ("Trii", "Carteras Colectivas"): "Fondo Acciones & Valores Vista (Ideal para liquidez inmediata).",
    ("Trii", "Fondo de Deuda"): "Fondo Renta Fija Acciones & Valores.",
    ("Trii", "CDT"): "CDT Digital Acciones & Valores (Gestionado en app).",
    ("tyba", "Carteras Colectivas"): "Fondo tyba Pocket (Bajo riesgo), Fondo tyba Acciones Globales (Alto riesgo).",
    ("tyba", "Fondo de Deuda"): "Fondo Renta Fija tyba.",
    ("tyba", "CDT"): "CDT Digital Mibanco (Contratado directamente en la app tyba).",
    ("tyba", "Fondo de Pensión Voluntaria"): "Portafolios de pensión voluntaria Credicorp Capital.",
    ("Nu Colombia", "Cuenta de Ahorro Remunerada"): "Cajitas Nu (Rendimiento diario).",
    ("Nu Colombia", "CDT"): "CDT Digital Nu (Plazos flexibles desde 60 días).",
    ("Lulo Bank", "Cuenta de Ahorro Remunerada"): "Bolsillos Lulo (Rendimiento por metas).",
    ("Lulo Bank", "CDT"): "CDT Lulo Bank (Tasa fija garantizada).",
    ("Interactive Brokers", "ETFs"): "VOO (S&P 500), QQQ (Nasdaq 100), VT (Vanguard Total World).",
    ("Interactive Brokers", "Acciones Individuales"): "Apple (AAPL), Microsoft (MSFT), Amazon (AMZN), Nvidia (NVDA).",
    ("Hapi", "ETFs"): "SPY (S&P 500), QQQ (Nasdaq 100), DIA (Dow Jones).",
    ("Hapi", "Acciones Individuales"): "Fracciones de acciones de EE.UU. desde $5 USD (Tesla, Apple, Google, Meta).",
    ("Bancolombia eTrading", "Acciones Individuales"): "Acciones del COLCAP y Mercado Global Colombiano (MGC).",
    ("Bancolombia eTrading", "ETFs"): "iShares COLCAP, ETFs globales a través de MGC.",
    ("Bancolombia eTrading", "Carteras Colectivas"): "Fiducuenta, Plan Semilla.",
    ("Pibank", "Cuenta de Ahorro Remunerada"): "Cuenta Pibank (Liquidación de intereses mensual, sin comisiones).",
    ("Pibank", "CDT"): "CDT Pibank (Tradicionalmente con las mejores tasas del mercado).",
    ("Davivienda", "CDT"): "CDT Móvil Davivienda.",
    ("Davivienda", "Carteras Colectivas"): "Fondo Superior, Fondo Interés.",
    ("Davivienda", "Fondo de Pensión Voluntaria"): "Dafuturo (Múltiples portafolios).",
    ("Porvenir", "Fondo de Pensión Voluntaria"): "Portafolio Conservador, Moderado o Crecimiento.",
    ("Protección", "Fondo de Pensión Voluntaria"): "Portafolio Liquidez, Portafolio Acciones Globales.",
    ("Wenia", "Criptomonedas"): "COPW (Criptopeso), Bitcoin (BTC), Ethereum (ETH).",
    ("Bitso", "Criptomonedas"): "Bitcoin (BTC), Ethereum (ETH), USDC (Dólar digital estable).",
    ("Binance", "Criptomonedas"): "Bitcoin, Ethereum, USDT, y cientos de altcoins (Alto riesgo).",
    ("Kraken", "Criptomonedas"): "Bitcoin (BTC), Ethereum (ETH), USDC."
}

def main():
    trm_vivo = obtener_trm_actual()
    
    html('<div class="hero"><h1>🤖 Asesor Inteligente de Inversiones</h1><p>Configura tu perfil para obtener opciones de mercado basadas en IA.</p></div>')
    
    st.subheader("1. Configura tu Inversión")
    
    primera = st.selectbox("¿Es tu primera vez invirtiendo?", ["Sí, es mi primera vez", "No, ya he invertido antes"], index=None, placeholder="Elige una opción")
    objetivo = st.selectbox("¿Para qué quieres invertir?", motor.OBJETIVOS, index=None, placeholder="Elige una opción")
    moneda_txt = st.selectbox("¿En qué moneda prefieres invertir?", ["Pesos Colombianos (COP)", "Dólares (USD)"], index=None, placeholder="Elige una opción")
    plazo_txt = st.selectbox("¿A qué plazo?", options=motor.PLAZOS, format_func=lambda x: f"{x} meses" if x > 1 else "1 mes", index=None, placeholder="Elige una opción")

    moneda = "COP" if moneda_txt == "Pesos Colombianos (COP)" else "USD" if moneda_txt == "Dólares (USD)" else None
    
    # ---------------------------------------------------------
    # Diseño visual de la tasa en Vivo para USD
    # ---------------------------------------------------------
    if moneda == "USD":
        st.info(f"🌐 **TRM en Vivo:** El mercado calcula hoy el Dólar a **${trm_vivo:,.2f} COP**")
    
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
        with st.spinner("Desbloqueando todo el catálogo de entidades (Procesando 100% de la base)..."):
            puntos = sum(dict(o)[r] for (_, o), r in zip(motor.PREGUNTAS, resp_actualizadas))
            perfil = motor.perfil_desde_puntos(puntos)
            
            # EL TRUCO ESTÁ AQUÍ: "n=10" OBLIGA AL MOTOR A TRAER MÁS OPCIONES
            out = motor.recomendar(
                primera_vez=(primera == "Sí, es mi primera vez"),
                monto=float(monto),
                moneda=moneda,
                trm=trm_vivo,  # <-- Inyectamos el Dólar en Vivo 
                plazo=plazo_txt,
                perfil=perfil,
                pref_moneda="Me da igual",
                pref_entidad=motor.ENTIDAD_IGUAL,
                aporte_mensual=float(aporte) if aporte is not None else 0.0,
                n=10 
            )
            
            st.markdown(f"### Tu Perfil IA: **{perfil}** (Puntaje: {puntos})")
            st.markdown("A continuación, te detallamos **todas las carteras y entidades disponibles**, cuánto ganarás y qué activos específicos buscar en cada aplicación:")
            
            monto_usd = motor.a_usd(float(monto), moneda, trm_vivo)
            
            for i, r in enumerate(out["resultados"]):
                act_tipo = r['tipo']
                
                plataformas_completas = []
                for p in motor.PLATAFORMAS:
                    if act_tipo in p.get('tipos', []):
                        if monto_usd >= p['min_usd']:
                            plataformas_completas.append(p)
                
                tasa_esp = r['rendimiento_anual_pct']
                com_esp = r['comision_pct']
                val_fin = r['valor_final']
                aportado = r['total_aportado']
                ganancia_neta = r['ganancia']
                
                descuento = aportado * (com_esp / 100)
                ganancia_bruta = ganancia_neta + descuento

                html(f"""
                <div class="card" style="margin-bottom: 5px;">
                  <div class="card-header" style="margin-bottom: 5px;">
                    <h3 class="card-title">Opción {i+1}: {act_tipo}</h3>
                    <span class="badge { 'b-cop' if r['moneda_activo'] == 'COP' else 'b-usd' }">{r['moneda_activo']}</span>
                  </div>
                  <p style="margin-top:0; color: #475569;">{r['descripcion']}</p>
                </div>
                """)
                
                if not plataformas_completas:
                    st.warning(f"No encontramos una aplicación que acepte el monto actual para {act_tipo}.")
                    continue
                
                tabs = st.tabs([p['nombre'] for p in plataformas_completas])
                
                for idx, p in enumerate(plataformas_completas):
                    with tabs[idx]:
                        col_izq, col_der = st.columns([1, 1.2])
                        with col_izq:
                            st.write(f"**📱 App/Banco:** {p['nombre']}")
                            st.write(f"**💸 Costos/Comisiones reales:** {p['costos']}")
                            
                            sugerencia = EJEMPLOS_ESPECIFICOS.get((p['nombre'], act_tipo), f"Opciones de {act_tipo} directo en el buscador de la app.")
                            st.info(f"**📌 ¿Qué debes buscar exactamente?:**\n\n{sugerencia}")
                            
                            st.markdown("---")
                            st.markdown("**💰 Tus números exactos:**")
                            st.write(f"Tu Capital Aportado: **{motor.fmt(aportado, moneda)}**")
                            st.write(f"Ganancia Bruta: **+ {motor.fmt(ganancia_bruta, moneda)}**")
                            st.write(f"Descuento (Comisión/Impuesto): **- {motor.fmt(descuento, moneda)}**")
                            st.markdown(f"#### Libre para ti: <span style='color:#059669'>**{motor.fmt(val_fin, moneda)}**</span>", unsafe_allow_html=True)

                        with col_der:
                            df_serie = r['serie'].copy()
                            df_serie.rename(columns={
                                "Con tu inversión": f"Proyección en {p['nombre']}",
                                "Solo lo que aportas": "Dinero de tu bolsillo"
                            }, inplace=True)
                            st.area_chart(df_serie, color=["#0ea5e9", "#94a3b8"])
                
                st.markdown("<br><hr><br>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()