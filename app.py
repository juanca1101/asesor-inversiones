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
# BASE DE DATOS FINANCIERA: DESGLOSE DE IMPUESTOS, COMISIONES Y RENTABILIDAD
# ==============================================================================
CATALOGO_FINANCIERO_DETALLADO = {
    # ------------------- TRII -------------------
    ("Trii", "Acciones Individuales"): [
        "🟢 **Mercado Local (Ecopetrol, Bancolombia, ISA):** \n- **Ganancia:** Por valorización (sube el precio) y pago de Dividendos.\n- **Retención (Impuesto):** Te descuentan el **10%** sobre los dividendos que te paguen.\n- **Comisión Trii:** Cobran ~$14.900 COP fijos por cada vez que compres o vendas (si el monto es menor a 5M).",
        "🌐 **Mercado Global (Nu Holdings, Apple en MGC):** \n- **Ganancia:** Cotizan en pesos pero siguen el precio en dólares (te proteges si el dólar sube). No suelen pagar dividendos altos, la ganancia es por crecimiento del precio."
    ],
    ("Trii", "ETFs"): [
        "📊 **iShares COLCAP (ICOLCAP):** \n- **Detalle:** Compras las 20 empresas más grandes de Colombia de un solo golpe.\n- **Costos:** Tiene una comisión de administración interna del fondo de aprox **0.60%** anual.\n- **Impuestos:** Retención del 10% sobre dividendos repartidos.",
        "🇺🇸 **iShares S&P 500 (CSPX):** \n- **Detalle:** Sigue a las 500 top de EE. UU.\n- **Ventaja:** Acumula los dividendos automáticamente para no pagar impuestos en Colombia hasta que lo vendas."
    ],
    ("Trii", "CDT"): [
        "🏦 **CDT Digital Acciones & Valores:** \n- **Ganancia:** Tasa E.A. Fija garantizada.\n- **Retención de Ley:** Se te descuenta el **4% de Retención en la Fuente** de forma automática sobre los intereses que ganes."
    ],
    ("Trii", "Carteras Colectivas"): [
        "💼 **Fondo Vista (Liquidez):** \n- **Rentabilidad:** Variable, suele rondar el 6%-8% anual.\n- **Comisión:** El fondo descuenta un % de administración antes de mostrarte tu saldo.\n- **Retención:** 7% de Retención en la Fuente sobre los rendimientos financieros."
    ],

    # ------------------- HAPI -------------------
    ("Hapi", "Fondos Indexados"): [
        "📈 **VOO (S&P 500) / QQQ (Nasdaq 100):** \n- **Rentabilidad Histórica:** ~10% a 12% anual en DÓLARES.\n- **Comisión de Compra:** **0% (Cero dólares)** por operar.\n- **Retención (Impuesto EE.UU.):** Por ser extranjero, el gobierno de EE.UU. te retiene automáticamente el **30% de los dividendos** que paguen estos fondos. La valorización del fondo NO tiene retención en EE.UU.\n- **Costos Ocultos:** Fondeo desde Colombia por PSE cuesta ~0.45% (Mínimo $2.99 USD)."
    ],
    ("Hapi", "Acciones Individuales"): [
        "🍎 **Apple / Tesla / Amazon / Nvidia:** \n- **Inversión:** Puedes comprar fracciones desde $5 USD.\n- **Riesgo:** Alto (volatilidad diaria).\n- **Impuestos:** Igual que los ETFs, retención del 30% en dividendos. Si vendes con ganancia, debes declararlo como ganancia ocasional en Colombia al traer el dinero."
    ],

    # ------------------- INTERACTIVE BROKERS -------------------
    ("Interactive Brokers", "Fondos Indexados"): [
        "🏦 **ETFs Globales (VOO, VT):** \n- **Comisión:** Aprox $0.005 USD por acción (Mínimo $1 USD por operación).\n- **Ventaja Pro:** Puedes comprar ETFs domiciliados en Irlanda (Ej. VWRA) para que la retención de dividendos baje del 30% al **15%**, ahorrando muchos impuestos a largo plazo."
    ],

    # ------------------- BANCOS: CDTs Y CUENTAS (Nu, Lulo, Pibank, Davivienda) -------------------
    ("Nu Colombia", "CDT"): [
        "🟣 **CDT Digital Nu (Desde 60 días):** \n- **Tasa:** Fija E.A. (Ej. 9% a 11% dependiendo del plazo).\n- **Impuestos:** Por ley, el banco aplica **4% de Retención en la Fuente** sobre tu ganancia al vencimiento.\n- **Seguro:** Tu capital y ganancias están protegidos por Fogafín hasta por $50 millones de pesos."
    ],
    ("Nu Colombia", "Cuenta de Ahorro Remunerada"): [
        "🟣 **Cajitas Nu:** \n- **Rentabilidad:** Tasa E.A. que se liquida a diario.\n- **Retención:** Aplica **7% de Retención en la Fuente** sobre los intereses diarios pagados.\n- **Ventaja:** Cero comisiones de manejo. Al sacar el dinero de la cajita a tu cuenta Nu NO te cobran 4x1000."
    ],
    ("Lulo Bank", "CDT"): [
        "🟡 **CDT Lulo Bank:** \n- **Impuestos:** Igual que todos, **4% de retención** sobre la ganancia bruta.\n- **Características:** No permite cancelarlo antes de la fecha (es ilíquido hasta el vencimiento)."
    ],
    ("Lulo Bank", "Cuenta de Ahorro Remunerada"): [
        "🟡 **Bolsillos Lulo:** \n- **Rentabilidad:** Genera intereses diarios.\n- **Retención:** 7% sobre rendimientos financieros pagados."
    ],
    ("Pibank", "CDT"): [
        "🔴 **CDT Pibank:** \n- **Ventaja Única:** Te permite elegir si quieres que te paguen los intereses mensuales o al final del plazo.\n- **Impuestos:** 4% de retención en la fuente sobre lo que te paguen."
    ],
    ("Pibank", "Cuenta de Ahorro Remunerada"): [
        "🔴 **Cuenta Pibank:** \n- **Beneficios:** Da el 100% de la rentabilidad prometida desde el primer peso, sin condiciones. Retención del 7% sobre las ganancias mensuales."
    ],
    ("Davivienda", "CDT"): [
        "🏠 **CDT Móvil Davivienda:** \n- **Seguridad:** Banco tradicional, protección Fogafín 50M. \n- **Impuestos:** 4% de retención en la fuente sobre intereses."
    ],
    ("Davivienda", "Fondo de Pensión Voluntaria"): [
        "🏠 **Dafuturo (Pensión Voluntaria):** \n- **Beneficio Tributario:** El dinero que aportas reduce tu base para el pago de impuesto de Renta (hasta 30% del ingreso).\n- **Comisión:** Cobra comisión de administración anual (~1.5% a 3%).\n- **Condición:** Si retiras la plata antes de 10 años para algo diferente a compra de vivienda, pierdes el beneficio tributario y te cobran la retención de golpe."
    ],

    # ------------------- TYBA -------------------
    ("tyba", "Carteras Colectivas"): [
        "💼 **Fondo tyba Pocket (Bajo riesgo):** \n- **Comisión:** Cobra ~1.2% E.A. por administración.\n- **Retención:** 7% sobre rendimientos."
    ],
    ("tyba", "Fondo de Pensión Voluntaria"): [
        "💼 **Portafolios Credicorp:** \n- **Estrategia:** Ideal para bajar impuestos anuales.\n- **Condiciones:** Rentabilidad variable según mercado, cobra comisión de administración del fondo."
    ],

    # ------------------- BANCOLOMBIA -------------------
    ("Bancolombia eTrading", "Acciones Individuales"): [
        "🇨🇴 **Comisiones Bancolombia:** \n- Es el más costoso para montos pequeños. Cobra **0.2% + IVA** por operación, con una comisión mínima de **$20.000 COP + IVA** (Si compras $100.000 en acciones, ya pierdes casi el 25% solo en comisión). Ideal solo para montos grandes."
    ],

    # ------------------- CRIPTOMONEDAS -------------------
    ("Bitso", "Criptomonedas"): [
        "₿ **Bitcoin / Ethereum / USDC:** \n- **Comisión:** Cobran entre 0.5% y 1% en el *spread* (la diferencia entre precio de compra y venta).\n- **Impuestos:** No hay retención en la fuente automática, PERO es tu obligación legal declararlo en tu impuesto de Renta si sacas ganancias a tu cuenta bancaria."
    ],
    ("Binance", "Criptomonedas"): [
        "₿ **Cripto Global:** \n- **Comisión:** 0.1% por operación (La más baja del mercado).\n- **Fondeo:** Debes usar P2P (Comprar dólares digitales a otras personas), lo que tiene un ligero sobrecosto en la tasa de cambio."
    ],
    ("Wenia", "Criptomonedas"): [
        "🟣 **COPW (Criptopeso de Bancolombia):** \n- **Ventaja:** Conexión directa y rápida con Nequi o Bancolombia para fondear.\n- **Riesgos:** Está domiciliada en Bermudas, **NO** tiene seguro Fogafín. Comisiones de conversión incluidas en el precio."
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
                            
                            # DESPLIEGUE DEL ANÁLISIS FINANCIERO ESPECÍFICO
                            catalogo = CATALOGO_FINANCIERO_DETALLADO.get((p['nombre'], act_tipo), [])
                            if catalogo:
                                st.markdown("---")
                                st.markdown(f"**⚖️ Desglose de Impuestos, Comisiones y Rentabilidad ({act_tipo} en {p['nombre']}):**")
                                for item in catalogo:
                                    st.markdown(f"{item}")
                                    st.markdown("<br>", unsafe_allow_html=True)
                            else:
                                st.info(f"📌 Los costos, impuestos y opciones detalladas aplican según las políticas generales de {p['nombre']}.")
                            
                        with col_der:
                            # Contenedor gris para destacar la matemática global del modelo
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