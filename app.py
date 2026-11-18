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
# DICCIONARIO MAESTRO: CUBRE EL 100% DE COMBINACIONES DE LA BASE DE DATOS
# ==============================================================================
CATALOGO_FINANCIERO_DETALLADO = {
    # ------------------- TRII -------------------
    ("Trii", "Acciones Individuales"): [
        "🟢 **Mercado Local (Ecopetrol, Bancolombia, ISA):** \n- **Ganancia:** Por valorización y pago de Dividendos.\n- **Retención:** 10% sobre dividendos.\n- **Comisión Trii:** ~$14.900 COP fijos por cada vez que compres o vendas (si el monto es <5M).",
        "🌐 **Mercado Global (Nu Holdings, Apple en MGC):** \n- Cotizan en pesos pero siguen el precio en dólares."
    ],
    ("Trii", "ETFs"): [
        "📊 **iShares COLCAP (ICOLCAP):** Compras las empresas más grandes de Colombia. Comisión del fondo ~0.60% anual.",
        "🇺🇸 **iShares S&P 500 (CSPX):** Sigue a EE.UU. Acumula los dividendos para que no pagues impuestos en Colombia."
    ],
    ("Trii", "ETFs Sectoriales"): [
        "📈 **ETFs Temáticos:** Acceso a sectores específicos (Tecnología, Energía) a través del Mercado Global Colombiano."
    ],
    ("Trii", "Fondos Indexados"): [
        "🌎 **Fondos de Acciones Globales:** Siguen índices mundiales. Cobra comisión de administración anual del fondo."
    ],
    ("Trii", "Carteras Colectivas"): [
        "💼 **Fondo Vista (Alta Liquidez):** \n- **Rentabilidad:** ~6%-8% anual.\n- **Impuestos:** 7% de Retención en la Fuente sobre rendimientos financieros."
    ],
    ("Trii", "Fondo de Deuda"): [
        "📉 **Fondo Renta Fija Acciones & Valores:** \n- Invierte en deuda de empresas colombianas.\n- **Retención:** 7% sobre las ganancias."
    ],
    ("Trii", "Bonos de Gobierno"): [
        "📜 **Deuda del Estado (TES):** \n- **Mecanismo:** A través de Trii inviertes en un fondo administrado por Acciones & Valores que compra TES del gobierno.\n- **Impuestos:** 7% de retención en la fuente sobre ganancias."
    ],
    ("Trii", "CDT"): [
        "🏦 **CDT Digital Acciones & Valores:** \n- Tasa E.A. Fija garantizada. **4% de Retención en la Fuente** automática."
    ],

    # ------------------- TYBA -------------------
    ("tyba", "Carteras Colectivas"): [
        "💼 **Fondo tyba Pocket (Bajo riesgo):** \n- Ideal para empezar. Rentabilidad moderada.\n- **Impuestos:** 7% sobre rendimientos."
    ],
    ("tyba", "Fondo de Deuda"): [
        "📉 **Fondo Renta Fija Credicorp:** \n- Invierte en bonos corporativos. Retención del 7% sobre las ganancias."
    ],
    ("tyba", "Bonos de Gobierno"): [
        "📜 **Fondos de Deuda Pública:** \n- **Mecanismo:** Portafolios de Credicorp Capital enfocados 100% en Bonos del Gobierno (TES).\n- **Impuestos:** 7% de retención en la fuente."
    ],
    ("tyba", "Fondos Indexados"): [
        "📊 **Fondo Acciones Globales:** \n- Atado a índices como el S&P 500. Retención del 7% sobre rendimientos."
    ],
    ("tyba", "Fondo de Pensión Voluntaria"): [
        "🎯 **Portafolios Credicorp:** \n- **Beneficio Tributario:** El dinero que aportas reduce tu impuesto de Renta (hasta 30% del ingreso)."
    ],
    ("tyba", "CDT"): [
        "🏦 **CDT Digital Mibanco:** \n- Tasa fija E.A. **4% de Retención en la Fuente**."
    ],

    # ------------------- BANCOLOMBIA -------------------
    ("Bancolombia eTrading", "Acciones Individuales"): [
        "🇨🇴 **Acciones Locales y MGC:** \n- **Comisiones Altas:** 0.2% + IVA por operación (Comisión mínima de $20.000 + IVA). Ideal solo para montos grandes."
    ],
    ("Bancolombia eTrading", "ETFs"): [
        "📊 **iShares COLCAP:** ETFs globales disponibles en la bolsa local."
    ],
    ("Bancolombia eTrading", "Carteras Colectivas"): [
        "💼 **Fiducuenta / Plan Semilla:** Alta liquidez, se administran desde la App Personas."
    ],
    ("Bancolombia eTrading", "Fondo de Deuda"): [
        "📉 **Fidurenta Bancolombia:** Para perfiles conservadores."
    ],
    ("Bancolombia eTrading", "Bonos de Gobierno"): [
        "📜 **Participación en TES:** A través de fondos de renta fija pública de Fiduciaria Bancolombia."
    ],
    ("Bancolombia eTrading", "CDT"): [
        "🏦 **CDT Físico o Virtual:** Tasa fija, 4% de retención."
    ],

    # ------------------- HAPI -------------------
    ("Hapi", "Fondos Indexados"): [
        "📈 **VOO (S&P 500) / QQQ (Nasdaq 100):** \n- **Comisión de Compra:** **0% (Cero dólares)** por operar.\n- **Impuesto EE.UU.:** Retención automática del **30%** de los dividendos por ser extranjero (La valorización NO tiene retención)."
    ],
    ("Hapi", "ETFs"): [
        "🌎 **VT / VTI:** Fondos de Vanguard para cubrir todo el mercado de EE.UU. o Mundial."
    ],
    ("Hapi", "ETFs Sectoriales"): [
        "🚀 **XLK / XLV:** Invierte en sectores específicos (Tecnología, Salud)."
    ],
    ("Hapi", "Acciones Individuales"): [
        "🍎 **Apple / Tesla / Amazon:** \n- Fracciones desde $5 USD. Igual impuesto del 30% sobre dividendos."
    ],
    ("Hapi", "Carteras Colectivas"): [
        "💼 **Portafolios Temáticos Hapi:** Cestas prearmadas."
    ],
    ("Hapi", "Criptomonedas"): [
        "₿ **Bitcoin / Ethereum:** Puedes comprar con el mismo saldo de tus acciones."
    ],

    # ------------------- INTERACTIVE BROKERS -------------------
    ("Interactive Brokers", "Fondos Indexados"): [
        "🏦 **ETFs Globales (VOO, VT):** \n- **Comisión:** Aprox $0.005 USD por acción (Mínimo $1 USD).\n- **Hack Tributario:** Puedes comprar ETFs de Irlanda (Ej. VWRA) para bajar la retención de dividendos del 30% al **15%**."
    ],
    ("Interactive Brokers", "ETFs"): ["📊 **Miles de ETFs globales:** Vanguard, iShares, Invesco."],
    ("Interactive Brokers", "ETFs Sectoriales"): ["🚀 **Todos los sectores:** Desde Inteligencia Artificial hasta Energías Limpias."],
    ("Interactive Brokers", "Acciones Individuales"): ["🏢 **NYSE / NASDAQ:** Acceso total al mercado accionario."],
    ("Interactive Brokers", "Carteras Colectivas"): ["💼 **Mutual Funds:** Fondos mutuos de grandes gestoras (BlackRock, Fidelity)."],
    ("Interactive Brokers", "Bonos de Gobierno"): [
        "📜 **T-Bills y T-Bonds (EE.UU.):** \n- Bonos del tesoro americano, altísima seguridad global."
    ],

    # ------------------- BANCOS LOCALES (Nu, Lulo, Pibank, Davivienda) -------------------
    ("Nu Colombia", "CDT"): ["🟣 **CDT Digital Nu:** Tasa Fija E.A. **4% de Retención en la Fuente**. Seguro Fogafín."],
    ("Nu Colombia", "Cuenta de Ahorro Remunerada"): ["🟣 **Cajitas Nu:** Rentabilidad diaria. **7% de Retención** sobre intereses. Sin cuota de manejo."],
    ("Lulo Bank", "CDT"): ["🟡 **CDT Lulo Bank:** Tasa Fija. 4% de retención. No se puede cancelar antes del plazo."],
    ("Lulo Bank", "Cuenta de Ahorro Remunerada"): ["🟡 **Bolsillos Lulo:** Intereses diarios. 7% de retención sobre rendimientos."],
    ("Pibank", "CDT"): ["🔴 **CDT Pibank:** Puedes pedir que te paguen los intereses mensuales a tu cuenta."],
    ("Pibank", "Cuenta de Ahorro Remunerada"): ["🔴 **Cuenta Pibank:** Liquidación automática cada mes. Da el 100% de la tasa desde $1 peso."],
    ("Davivienda", "CDT"): ["🏠 **CDT Móvil Davivienda:** 4% de retención en la fuente sobre intereses. Seguro Fogafín."],
    ("Davivienda", "Carteras Colectivas"): ["🏠 **Fondo Superior / Fondo Interés:** Administrados por Fiduciaria Davivienda."],
    ("Davivienda", "Fondo de Deuda"): ["📉 **Fondo Renta Fija Plazo 30:** Ideal para perfil conservador a corto plazo."],
    ("Davivienda", "Fondo de Pensión Voluntaria"): ["🎯 **Dafuturo:** Reduce tu pago de impuesto de Renta (hasta 30% del ingreso). Pierdes el beneficio si retiras antes de 10 años sin justa causa."],
    
    # ------------------- FONDOS DE PENSIÓN -------------------
    ("Porvenir", "Fondo de Pensión Voluntaria"): ["👴 **Portafolios Porvenir:** Estrategias conservadoras o de renta variable internacional. Ideal para beneficios tributarios."],
    ("Protección", "Fondo de Pensión Voluntaria"): ["🛡️ **Portafolios Protección:** Desde liquidez inmediata hasta acciones globales. Útil para declarar renta a tu favor."],

    # ------------------- CRIPTOMONEDAS -------------------
    ("eToro", "Criptomonedas"): ["₿ **Crypto en eToro:** Compra directa del activo subyacente. Sin billetera privada."],
    ("eToro", "Acciones Individuales"): ["🏢 **Cero comisiones** en acciones reales. Ganancias por el spread."],
    ("eToro", "ETFs"): ["📊 **SPY, VOO:** Disponibles como CFD o activo subyacente."],
    ("eToro", "ETFs Sectoriales"): ["🚀 **Tecnología, Energía:** A través de ETFs temáticos."],
    ("Bitso", "Criptomonedas"): ["₿ **Bitcoin / Ethereum / USDC:** \n- Comisión del ~0.5% al 1% en el spread. Debes declarar tus ganancias en Renta."],
    ("Binance", "Criptomonedas"): ["₿ **Cripto Global:** \n- Comisión del 0.1% (La más baja). Requiere usar mercado P2P para fondear."],
    ("Wenia", "Criptomonedas"): ["🟣 **COPW (Criptopeso):** \n- Conexión con Bancolombia/Nequi. No tiene seguro Fogafín."],
    ("Kraken", "Criptomonedas"): ["🐙 **Kraken Pro:** Alta seguridad, ideal para trading avanzado."],
    ("Buda", "Criptomonedas"): ["🇨🇱 **Buda:** Fondeo directo por PSE en Colombia. Altamente regulado en Chile."]
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
        st.info("💡 Faltan campos por llenar. Completa todas las preguntas y el monto inicial para generar el análisis tributario y financiero.")
        
    if st.button("Analizar Portafolio", disabled=not campos_llenos):
        with st.spinner("Calculando impuestos, comisiones y rentabilidades de todo el mercado..."):
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
                <div class="card" style="margin-bottom: 5px; margin-top: 20px;">
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
                            st.warning(f"⚠️ **Atención:** El mínimo sugerido aquí es {p['minimo_txt']}. Tu monto no alcanza, pero revisa la estructura de costos para el futuro.")
                        
                        col_izq, col_der = st.columns([1.3, 1])
                        with col_izq:
                            st.write(f"**📱 App/Banco:** {p['nombre']}")
                            st.write(f"**💸 Costos/Comisiones (Resumen App):** {p['costos']}")
                            
                            # DESPLIEGUE DEL ANÁLISIS FINANCIERO ESPECÍFICO (Ahora sí cubre el 100%)
                            catalogo = CATALOGO_FINANCIERO_DETALLADO.get((p['nombre'], act_tipo), [])
                            if catalogo:
                                st.markdown("---")
                                st.markdown(f"**⚖️ Desglose de Impuestos, Comisiones y Rentabilidad ({act_tipo} en {p['nombre']}):**")
                                for item in catalogo:
                                    st.markdown(f"{item}")
                                    st.markdown("<br>", unsafe_allow_html=True)
                            else:
                                st.info(f"📌 {act_tipo} disponible en {p['nombre']}. Costos e impuestos según política general de la app.")
                            
                        with col_der:
                            with st.container(border=True):
                                st.markdown("##### 💰 Proyección Matemática")
                                st.write(f"Capital Aportado: **{motor.fmt(r['total_aportado'], moneda)}**")
                                st.write(f"Ganancia Bruta: **+ {motor.fmt(r['ganancia'] + (r['total_aportado'] * (r['comision_pct'] / 100)), moneda)}**")
                                st.write(f"Desc./Impuestos Total: **- {motor.fmt(r['total_aportado'] * (r['comision_pct'] / 100), moneda)}**")
                                st.markdown(f"#### Libre para ti: <span style='color:#059669'>**{motor.fmt(r['valor_final'], moneda)}**</span>", unsafe_allow_html=True)
                            
                            df_serie = r['serie'].copy()
                            df_serie.rename(columns={
                                "Con tu inversión": f"Crecimiento Neto",
                                "Solo lo que aportas": "Bolsillo"
                            }, inplace=True)
                            st.area_chart(df_serie, color=["#0ea5e9", "#94a3b8"], height=230)
                
if __name__ == "__main__":
    main()