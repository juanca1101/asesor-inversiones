import streamlit as st
import motor
from estilos import CSS
import pandas as pd
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

@st.cache_data(ttl=3600)
def obtener_trm_actual():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        respuesta = requests.get(url, timeout=5)
        datos = respuesta.json()
        return float(datos['rates']['COP'])
    except Exception:
        return motor.TRM_DEFECTO

# ==============================================================================
# DICCIONARIO AVANZADO: LISTAS DE CATÁLOGO DETALLADO
# ==============================================================================
CATALOGO_DETALLADO = {
    ("Trii", "Acciones Individuales"): [
        "🟢 **Mercado Local (BVC):** Ecopetrol, Bancolombia, ISA, Celsia, Grupo Argos, GEB.",
        "🌐 **Mercado Global:** Nu Holdings, Apple, Amazon (a través del MGC)."
    ],
    ("Trii", "ETFs"): [
        "📊 **iShares COLCAP (ICOLCAP):** Invierte en las empresas más grandes de Colombia.",
        "🇺🇸 **iShares S&P 500 (CSPX):** Invierte en las 500 empresas más grandes de EE.UU."
    ],
    ("Trii", "Carteras Colectivas"): [
        "💼 **Fondo Acciones & Valores Vista:** Bajo riesgo, puedes retirar tu dinero rápido."
    ],
    ("Trii", "Fondo de Deuda"): [
        "📈 **Fondo Renta Fija Acciones & Valores:** Invierte en deuda de empresas y estado."
    ],
    ("Trii", "CDT"): [
        "🏦 **CDT Digital:** Emitido por Acciones & Valores. Se abre directo en la app sin papeleo."
    ],
    
    ("Hapi", "Fondos Indexados"): [
        "📈 **VOO:** Sigue el S&P 500 (Empresas grandes de EE.UU).",
        "💻 **QQQ:** Sigue el Nasdaq 100 (Sector tecnológico).",
        "🏭 **DIA:** Sigue el Dow Jones (Sector industrial)."
    ],
    ("Hapi", "ETFs"): [
        "🌎 **VT:** Vanguard Total World (Acciones de todo el mundo).",
        "🛡️ **VTI:** Vanguard Total Stock Market (Todo el mercado de EE.UU)."
    ],
    ("Hapi", "Acciones Individuales"): [
        "🍎 **Apple (AAPL):** Fracciones desde $5 USD.",
        "🚗 **Tesla (TSLA):** Fracciones desde $5 USD.",
        "🛒 **Amazon (AMZN):** Fracciones desde $5 USD.",
        "🤖 **Nvidia (NVDA):** Fracciones desde $5 USD."
    ],
    
    ("Interactive Brokers", "Fondos Indexados"): [
        "🏦 **Fondos Vanguard:** VFIAX, VTSAX.",
        "📈 **ETFs equivalentes:** VOO, IVV."
    ],
    ("Interactive Brokers", "Acciones Individuales"): [
        "🌐 **NYSE & NASDAQ:** Acceso a literalmente todas las acciones de EE.UU.",
        "🌍 **Mercado Europeo/Asiático:** Acceso a bolsas globales."
    ],
    
    ("Nu Colombia", "Cuenta de Ahorro Remunerada"): [
        "🟣 **Cajitas Nu:** Mueve tu plata a la cajita para generar rendimiento diario sin cobro de 4x1000 al sacarlo a tu cuenta."
    ],
    ("Nu Colombia", "CDT"): [
        "🟣 **CDT Digital Nu:** Desde $50.000 COP, plazos flexibles desde 60 días."
    ],
    
    ("Lulo Bank", "Cuenta de Ahorro Remunerada"): [
        "🟡 **Bolsillos Lulo:** Crea una meta, ponle un nombre y guarda ahí el dinero con rentabilidad."
    ],
    ("Lulo Bank", "CDT"): [
        "🟡 **CDT Lulo Bank:** Tasa fija asegurada. Liquidación a término."
    ],
    
    ("tyba", "Carteras Colectivas"): [
        "💼 **Fondo tyba Pocket:** Muy bajo riesgo.",
        "📈 **Fondo Acciones Globales:** Alto riesgo, renta variable."
    ],
    ("tyba", "CDT"): [
        "🏦 **CDT Mibanco:** Contratado 100% digital a través de la app tyba."
    ],
    
    ("Bancolombia eTrading", "Acciones Individuales"): [
        "🇨🇴 **Todas las acciones del COLCAP.**",
        "🌐 **Mercado Global Colombiano (MGC).**"
    ],
    ("Bancolombia eTrading", "Carteras Colectivas"): [
        "💼 **Fiducuenta:** Alta liquidez (Se busca en la App Personas, no en eTrading).",
        "🌱 **Plan Semilla:** Ahorro programado."
    ],
    
    ("Pibank", "Cuenta de Ahorro Remunerada"): [
        "🔴 **Cuenta Pibank:** Liquidación de intereses automática cada mes."
    ],
    ("Pibank", "CDT"): [
        "🔴 **CDT Pibank:** Tradicionalmente ofrece las tasas más competitivas del mercado."
    ],
    
    ("Davivienda", "CDT"): [
        "🏠 **CDT Móvil Davivienda:** Se abre desde la app transaccional del banco."
    ],
    ("Davivienda", "Fondo de Pensión Voluntaria"): [
        "🏠 **Dafuturo:** Te permite elegir portafolio Conservador, Moderado o Mayor Riesgo."
    ],
    
    ("Porvenir", "Fondo de Pensión Voluntaria"): [
        "👴 **Portafolio Conservador:** Invierte principalmente en renta fija local.",
        "🚀 **Portafolio Crecimiento:** Renta variable internacional."
    ],
    
    ("Bitso", "Criptomonedas"): [
        "₿ **Bitcoin (BTC)**",
        "🦇 **Ethereum (ETH)**",
        "💵 **USDC (Dólar digital estable)**"
    ],
    ("Binance", "Criptomonedas"): [
        "₿ **Bitcoin (BTC) & Ethereum (ETH)**",
        "💵 **USDT (Tether)**",
        "🚀 **Más de 350 altcoins (Solana, Cardano, etc.)**"
    ]
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
    
    if moneda == "USD":
        st.info(f"🌐 **TRM en Vivo:** El mercado calcula hoy el Dólar a **${trm_vivo:,.2f} COP**")
    
    monto, aporte = None, None
    if moneda == "COP":
        monto = st.number_input("Monto inicial a invertir (COP)", min_value=0, step=50000, value=None, placeholder="Ej: 100000")
        if monto is not None:
            st.caption(f"💰 Monto registrado: **${monto:,.0f} COP**".replace(",", "."))
        aporte = st.number_input("Aporte mensual (COP, opcional)", min_value=0, step=10000, value=None, placeholder="Ej: 50000")
        if aporte is not None:
            st.caption(f"🔄 Aporte mensual: **${aporte:,.0f} COP**".replace(",", "."))
            
    elif moneda == "USD":
        monto = st.number_input("Monto inicial a invertir (USD)", min_value=0, step=50, value=None, placeholder="Ej: 100")
        if monto is not None:
            st.caption(f"💰 Monto registrado: **${monto:,.0f} USD**".replace(",", "."))
        aporte = st.number_input("Aporte mensual (USD, opcional)", min_value=0, step=10, value=None, placeholder="Ej: 50")
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
    campos_llenos = all([primera, objetivo, moneda, plazo_txt, monto is not None]) and all(resp_actualizadas)
    
    if not campos_llenos:
        st.info("💡 Faltan campos por llenar. Completa todas las preguntas y el monto inicial.")
        
    if st.button("Analizar Portafolio", disabled=not campos_llenos):
        with st.spinner("Desbloqueando todo el catálogo de entidades y opciones exactas..."):
            puntos = sum(dict(o)[r] for (_, o), r in zip(motor.PREGUNTAS, resp_actualizadas))
            perfil = motor.perfil_desde_puntos(puntos)
            
            out = motor.recomendar(
                primera_vez=(primera == "Sí, es mi primera vez"),
                monto=float(monto),
                moneda=moneda,
                trm=trm_vivo, 
                plazo=plazo_txt,
                perfil=perfil,
                pref_moneda="Me da igual",
                pref_entidad=motor.ENTIDAD_IGUAL,
                aporte_mensual=float(aporte) if aporte is not None else 0.0,
                n=10 
            )
            
            st.markdown(f"### Tu Perfil IA: **{perfil}** (Puntaje: {puntos})")
            monto_usd = motor.a_usd(float(monto), moneda, trm_vivo)
            
            for i, r in enumerate(out["resultados"]):
                act_tipo = r['tipo']
                
                plataformas_completas = [p for p in motor.PLATAFORMAS if act_tipo in p.get('tipos', [])]
                
                if not plataformas_completas:
                    continue

                html(f"""
                <div class="card" style="margin-bottom: 5px;">
                  <div class="card-header" style="margin-bottom: 5px;">
                    <h3 class="card-title">Opción {i+1}: {act_tipo}</h3>
                    <span class="badge { 'b-cop' if r['moneda_activo'] == 'COP' else 'b-usd' }">{r['moneda_activo']}</span>
                  </div>
                  <p style="margin-top:0; color: #475569;">{r['descripcion']}</p>
                </div>
                """)
                
                tabs = st.tabs([p['nombre'] for p in plataformas_completas])
                
                for idx, p in enumerate(plataformas_completas):
                    with tabs[idx]:
                        if monto_usd < p['min_usd']:
                            st.warning(f"⚠️ **Atención:** El mínimo sugerido aquí es {p['minimo_txt']}. Tu monto actual no alcanza, pero te mostramos la opción para que la conozcas a futuro.")
                        
                        col_izq, col_der = st.columns([1.2, 1])
                        with col_izq:
                            st.write(f"**📱 App/Banco:** {p['nombre']}")
                            st.write(f"**💸 Costos/Comisiones reales:** {p['costos']}")
                            
                            # RENDERIZAMOS EL CATÁLOGO DETALLADO EN VIÑETAS
                            catalogo = CATALOGO_DETALLADO.get((p['nombre'], act_tipo), [])
                            if catalogo:
                                st.markdown("---")
                                st.markdown(f"**📌 Catálogo exacto de {act_tipo} en {p['nombre']}:**")
                                for item in catalogo:
                                    st.markdown(f"- {item}")
                            else:
                                st.info(f"📌 Búscalo como '{act_tipo}' en el menú principal o buscador de la app.")
                            
                        with col_der:
                            # Contenedor gris para destacar la matemática
                            with st.container(border=True):
                                st.markdown("##### 💰 Proyección Matemática")
                                st.write(f"Capital Aportado: **{motor.fmt(r['total_aportado'], moneda)}**")
                                st.write(f"Ganancia Bruta: **+ {motor.fmt(r['ganancia'] + (r['total_aportado'] * (r['comision_pct'] / 100)), moneda)}**")
                                st.write(f"Descuento/Comisión: **- {motor.fmt(r['total_aportado'] * (r['comision_pct'] / 100), moneda)}**")
                                st.markdown(f"#### Libre: <span style='color:#059669'>**{motor.fmt(r['valor_final'], moneda)}**</span>", unsafe_allow_html=True)
                            
                            df_serie = r['serie'].copy()
                            df_serie.rename(columns={
                                "Con tu inversión": f"Crecimiento",
                                "Solo lo que aportas": "Bolsillo"
                            }, inplace=True)
                            st.area_chart(df_serie, color=["#0ea5e9", "#94a3b8"], height=200)
                
                st.markdown("<br><hr><br>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()