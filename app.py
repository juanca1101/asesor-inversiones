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
# PERFIL DE CADA ENTIDAD (TIPO, QUÉ ES, CÓMO FUNCIONA Y AJUSTE RELATIVO)
# ==============================================================================
PERFIL_ENTIDADES = {
    "Trii": {
        "tipo": "Fintech / Comisionista de Bolsa",
        "que_es": "Aplicación colombiana respaldada por la comisionista Acciones & Valores, vigilada por la Superfinanciera.",
        "como_funciona": "Recargas saldo en pesos por PSE o Nequi, buscas la acción, ETF o fondo en la app y compras en segundos. Tus activos quedan a tu nombre en el depósito central (Deceval).",
        "delta_tasa": 0.25,
        "delta_com": 0.05,
    },
    "tyba": {
        "tipo": "Fintech de Inversiones (Credicorp Capital)",
        "que_es": "Plataforma digital del grupo financiero Credicorp Capital, vigilada por la Superfinanciera.",
        "como_funciona": "Eliges un fondo o CDT según tu meta, transfieres por PSE y un equipo de expertos administra el portafolio por ti sin que tengas que comprar acciones una por una.",
        "delta_tasa": 0.15,
        "delta_com": 0.15,
    },
    "Nu Colombia": {
        "tipo": "Neobanco / Compañía de Financiamiento",
        "que_es": "Banco 100% digital vigilado por la Superfinanciera y cubierto por el seguro de depósitos Fogafín hasta $50 millones.",
        "como_funciona": "Abres tu cuenta gratis desde el celular, creas 'Cajitas' para ahorro con rendimiento diario o abres un CDT digital desde $50.000 COP con tasa fija.",
        "delta_tasa": 0.65,
        "delta_com": -0.05,
    },
    "Lulo Bank": {
        "tipo": "Neobanco Digital",
        "que_es": "Primer banco 100% digital aprobado en Colombia, vigilado por la Superfinanciera y con seguro Fogafín.",
        "como_funciona": "Creas 'Bolsillos' dentro de la app para ganar intereses diarios manteniendo tu plata disponible, o pactas un CDT digital a tasa fija desde $100.000 COP.",
        "delta_tasa": 0.85,
        "delta_com": -0.05,
    },
    "Pibank": {
        "tipo": "Neobanco de Ahorro e Inversión (Banco Pichincha)",
        "que_es": "Marca digital especializada en ahorro y CDTs de alta rentabilidad, vigilada por la Superfinanciera y con seguro Fogafín.",
        "como_funciona": "No tiene tarjetas ni sucursales; transfieres desde otro banco y tu dinero empieza a generar rendimientos desde el primer peso.",
        "delta_tasa": 1.15,
        "delta_com": -0.08,
    },
    "Davivienda": {
        "tipo": "Banco Tradicional",
        "que_es": "Uno de los bancos más grandes de Colombia, vigilado por la Superfinanciera y respaldado por Fogafín.",
        "como_funciona": "Desde la App Davivienda o el portal web puedes abrir un CDT Móvil, invertir en fondos de Fiduciaria Davivienda o aportar a pensión voluntaria Dafuturo.",
        "delta_tasa": -0.35,
        "delta_com": 0.12,
    },
    "Bancolombia eTrading": {
        "tipo": "Banca Tradicional / Comisionista de Bolsa",
        "que_es": "Plataforma bursátil de Valores Bancolombia, vigilada por la Superfinanciera.",
        "como_funciona": "Conectas tu cuenta de ahorros Bancolombia para comprar acciones colombianas, ETFs del Mercado Global (MGC) o trasladar fondos a Fiducuenta.",
        "delta_tasa": -0.45,
        "delta_com": 0.25,
    },
    "Hapi": {
        "tipo": "Broker Internacional (EE. UU.)",
        "que_es": "Corredor de bolsa regulado en Estados Unidos (SEC/FINRA) con protección SIPC hasta US$500.000.",
        "como_funciona": "Depositas pesos colombianos por PSE (la app los convierte a dólares) y puedes comprar fracciones de acciones o ETFs de EE. UU. desde US$5 sin comisión por orden.",
        "delta_tasa": 0.30,
        "delta_com": 0.10,
    },
    "Interactive Brokers": {
        "tipo": "Broker Institucional Internacional (EE. UU.)",
        "que_es": "Uno de los brokers más grandes y sólidos del mundo, regulado en EE. UU. (SEC/FINRA) con seguro SIPC.",
        "como_funciona": "Envías dólares mediante transferencia internacional y accedes directamente a más de 150 bolsas mundiales con las comisiones más bajas del mercado.",
        "delta_tasa": 0.75,
        "delta_com": -0.25,
    },
    "eToro": {
        "tipo": "Plataforma de Inversión Social (Broker Internacional)",
        "que_es": "Broker global regulado en Europa (CySEC) y Reino Unido (FCA), famoso por su función de Copy Trading.",
        "como_funciona": "Fondeas tu cuenta en dólares con tarjeta o transferencia y puedes invertir por tu cuenta o copiar automáticamente los movimientos de inversionistas experimentados.",
        "delta_tasa": 0.10,
        "delta_com": 0.20,
    },
    "Porvenir": {
        "tipo": "Administradora de Fondos de Pensiones (AFP)",
        "que_es": "Fondo privado de pensiones y cesantías vigilado por la Superfinanciera.",
        "como_funciona": "Abres una cuenta de Pensión Voluntaria, eliges portafolios locales o globales según tu riesgo y obtienes beneficios tributarios en tu declaración de renta.",
        "delta_tasa": 0.20,
        "delta_com": 0.18,
    },
    "Protección": {
        "tipo": "Administradora de Fondos de Pensiones (AFP)",
        "que_es": "Entidad administradora de fondos de pensiones obligatorias, voluntarias y cesantías vigilada por la Superfinanciera.",
        "como_funciona": "Realizas aportes periódicos o únicos a portafolios diversificados de largo plazo con opción de deducción en retención en la fuente.",
        "delta_tasa": 0.15,
        "delta_com": 0.20,
    },
    "Wenia": {
        "tipo": "Plataforma de Activos Digitales (Grupo Cibest)",
        "que_es": "App de criptoactivos respaldada por el grupo empresarial de Bancolombia (constituida en Bermudas, sin seguro Fogafín).",
        "como_funciona": "Recargas desde Nequi o Bancolombia, conviertes tus pesos a criptopesos (COPW) y compras Bitcoin, Ethereum o dólares digitales de forma sencilla.",
        "delta_tasa": -0.40,
        "delta_com": 0.25,
    },
    "Bitso": {
        "tipo": "Exchange de Criptomonedas",
        "que_es": "Plataforma latinoamericana de intercambio de criptoactivos con operación directa en Colombia.",
        "como_funciona": "Transfieres pesos por PSE y compras Bitcoin, Ethereum o USDC (dólar digital) asumiendo directamente la custodia y volatilidad del mercado.",
        "delta_tasa": 0.10,
        "delta_com": 0.15,
    },
    "Binance": {
        "tipo": "Exchange Global de Criptomonedas",
        "que_es": "La plataforma de intercambio de criptoactivos más grande del mundo por volumen de operaciones (no vigilada por la Superfinanciera).",
        "como_funciona": "Compras USDT mediante comercio P2P en pesos y accedes a cientos de criptomonedas y opciones de staking con las comisiones más bajas.",
        "delta_tasa": 0.90,
        "delta_com": -0.30,
    },
    "Kraken": {
        "tipo": "Exchange Internacional de Criptomonedas",
        "que_es": "Plataforma estadounidense de intercambio cripto reconocida por sus altos estándares de seguridad.",
        "como_funciona": "Depositas dólares o criptoactivos y operas en mercado spot o Kraken Pro con comisiones escalonadas según volumen.",
        "delta_tasa": 0.40,
        "delta_com": -0.10,
    },
    "Buda": {
        "tipo": "Exchange Regional de Criptomonedas",
        "que_es": "Plataforma de origen chileno con operación formal en Colombia para compra y venta de criptoactivos.",
        "como_funciona": "Depositas pesos por PSE y compras Bitcoin, Ethereum o stablecoins directamente en moneda local.",
        "delta_tasa": -0.15,
        "delta_com": 0.18,
    }
}

# ==============================================================================
# DICCIONARIO MAESTRO: DESGLOSE POR ACTIVO Y ENTIDAD
# ==============================================================================
CATALOGO_FINANCIERO_DETALLADO = {
    ("Trii", "Acciones Individuales"): [
        "🟢 **Mercado Local (Ecopetrol, Bancolombia, ISA):** Ganancia por valorización y dividendos (retención del **10%** sobre dividendos). Comisión Trii: ~$14.900 COP fijos por orden hasta $5M.",
        "🌐 **Mercado Global (Nu Holdings, Apple en MGC):** Cotizan en pesos siguiendo el precio en dólares."
    ],
    ("Trii", "ETFs"): [
        "📊 **iShares COLCAP (ICOLCAP):** Invierte en las empresas líderes de Colombia. Comisión interna del fondo ~0,60% anual.",
        "🇺🇸 **iShares S&P 500 (CSPX):** Sigue a las 500 empresas más grandes de EE. UU. acumulando dividendos."
    ],
    ("Trii", "ETFs Sectoriales"): [
        "📈 **ETFs Temáticos:** Exposición a sectores específicos (Tecnología, Energía) vía Mercado Global Colombiano."
    ],
    ("Trii", "Fondos Indexados"): [
        "🌎 **Fondos de Acciones Globales:** Replican índices internacionales con administración profesional."
    ],
    ("Trii", "Carteras Colectivas"): [
        "💼 **Fondo Acciones & Valores Vista:** Liquidez inmediata. Retención del **7%** sobre los rendimientos generados."
    ],
    ("Trii", "Fondo de Deuda"): [
        "📉 **Fondo Renta Fija Acciones & Valores:** Títulos de deuda corporativa. Retención del **7%** sobre ganancias."
    ],
    ("Trii", "Bonos de Gobierno"): [
        "📜 **Deuda Pública (TES):** Inversión en títulos del Estado colombiano mediante fondo administrado. Retención del **7%**."
    ],
    ("Trii", "CDT"): [
        "🏦 **CDT Digital Acciones & Valores:** Tasa fija pactada desde el inicio. Retención en la fuente del **4%** sobre intereses."
    ],
    ("tyba", "Carteras Colectivas"): [
        "💼 **Fondo tyba Pocket / Acciones Globales:** Portafolios diversificados según riesgo. Retención del **7%** sobre rendimientos."
    ],
    ("tyba", "Fondo de Deuda"): [
        "📉 **Fondo Renta Fija Credicorp:** Bonos corporativos y deuda privada. Retención del **7%**."
    ],
    ("tyba", "Bonos de Gobierno"): [
        "📜 **Fondos de Deuda Pública:** Portafolios de Credicorp Capital concentrados en TES. Retención del **7%**."
    ],
    ("tyba", "Fondos Indexados"): [
        "📊 **Fondo Acciones Globales:** Atado a índices internacionales como el S&P 500. Retención del **7%**."
    ],
    ("tyba", "Fondo de Pensión Voluntaria"): [
        "🎯 **Portafolios Credicorp:** Permite deducir aportes de la base de renta (hasta 30% del ingreso, tope 3.800 UVT)."
    ],
    ("tyba", "CDT"): [
        "🏦 **CDT Digital Mibanco:** Emitido 100% digital desde tyba. Retención en la fuente del **4%**."
    ],
    ("Bancolombia eTrading", "Acciones Individuales"): [
        "🇨🇴 **Acciones Locales y MGC:** Comisión de **0,2% + IVA** por operación (mínimo ~$20.000 + IVA). Recomendado para montos altos."
    ],
    ("Bancolombia eTrading", "ETFs"): [
        "📊 **iShares COLCAP y MGC:** Acceso a canastas de acciones locales e internacionales."
    ],
    ("Bancolombia eTrading", "Carteras Colectivas"): [
        "💼 **Fiducuenta / Plan Semilla:** Disponibilidad rápida desde la App Personas. Retención del **7%** sobre rendimientos."
    ],
    ("Bancolombia eTrading", "Fondo de Deuda"): [
        "📉 **Fidurenta Bancolombia:** Renta fija conservadora administrada por Fiduciaria Bancolombia."
    ],
    ("Bancolombia eTrading", "Bonos de Gobierno"): [
        "📜 **Fondos TES Bancolombia:** Exposición a deuda pública colombiana."
    ],
    ("Bancolombia eTrading", "CDT"): [
        "🏦 **CDT Virtual Bancolombia:** Tasa fija y retención en la fuente del **4%**."
    ],
    ("Hapi", "Fondos Indexados"): [
        "📈 **VOO (S&P 500) / QQQ (Nasdaq 100):** 0% comisión de corretaje. EE. UU. retiene **30%** sobre dividendos (no sobre valorización)."
    ],
    ("Hapi", "ETFs"): [
        "🌎 **VT / VTI:** Diversificación en todo el mercado de EE. UU. o mundial desde US$5."
    ],
    ("Hapi", "ETFs Sectoriales"): [
        "🚀 **XLK / XLV / XLE:** ETFs especializados en tecnología, salud o energía."
    ],
    ("Hapi", "Acciones Individuales"): [
        "🍎 **Apple / Tesla / Nvidia:** Acciones fraccionadas desde US$5. Retención del **30%** en dividendos."
    ],
    ("Hapi", "Carteras Colectivas"): [
        "💼 **Portafolios Temáticos Hapi:** Canastas prearmadas por sectores."
    ],
    ("Hapi", "Criptomonedas"): [
        "₿ **Bitcoin / Ethereum:** Compra directa con saldo en dólares (no cubiertas por SIPC)."
    ],
    ("Interactive Brokers", "Fondos Indexados"): [
        "🏦 **ETFs Globales e Irlandeses (VWRA, CSPX):** Comisiones desde US$1. Los ETFs domiciliados en Irlanda reducen la retención de dividendos del 30% al **15%**."
    ],
    ("Interactive Brokers", "ETFs"): ["📊 **VOO, QQQ, VT:** Acceso directo a los ETFs más líquidos del mundo."],
    ("Interactive Brokers", "ETFs Sectoriales"): ["🚀 **Cobertura global:** ETFs sectoriales en bolsas de EE. UU. y Europa."],
    ("Interactive Brokers", "Acciones Individuales"): ["🏢 **NYSE / NASDAQ:** Compra directa de acciones completas o fraccionadas."],
    ("Interactive Brokers", "Carteras Colectivas"): ["💼 **Mutual Funds:** Miles de fondos de Vanguard, BlackRock y Fidelity."],
    ("Interactive Brokers", "Bonos de Gobierno"): ["📜 **US Treasury Bills (T-Bills):** Bonos del Tesoro de EE. UU. de altísima seguridad."],
    ("Nu Colombia", "CDT"): ["🟣 **CDT Digital Nu:** Plazos desde 60 días. Retención en la fuente del **4%** sobre intereses. Seguro Fogafín."],
    ("Nu Colombia", "Cuenta de Ahorro Remunerada"): ["🟣 **Cajitas Nu:** Abono diario de intereses. Retención del **7%** sobre rendimientos. Sin cuota de manejo ni 4x1000 interno."],
    ("Lulo Bank", "CDT"): ["🟡 **CDT Lulo Bank:** Plazos de 90 a 540 días con tasa fija. Retención en la fuente del **4%**."],
    ("Lulo Bank", "Cuenta de Ahorro Remunerada"): ["🟡 **Bolsillos Lulo:** Rendimientos diarios con disponibilidad inmediata. Retención del **7%**."],
    ("Pibank", "CDT"): ["🔴 **CDT Pibank:** Permite elegir pago de intereses mensual o al vencimiento. Retención del **4%**."],
    ("Pibank", "Cuenta de Ahorro Remunerada"): ["🔴 **Cuenta Pibank:** Liquidación mensual automática desde el primer peso. Retención del **7%**."],
    ("Davivienda", "CDT"): ["🏠 **CDT Móvil Davivienda:** Apertura 100% digital. Retención del **4%** sobre intereses. Seguro Fogafín."],
    ("Davivienda", "Carteras Colectivas"): ["🏠 **Fondo Superior / Fondo Interés:** Fondos de liquidez administrados por Fiduciaria Davivienda."],
    ("Davivienda", "Fondo de Deuda"): ["📉 **Fondo Renta Fija Plazo 30:** Enfocado en estabilidad a corto plazo."],
    ("Davivienda", "Fondo de Pensión Voluntaria"): ["🎯 **Dafuturo:** Ahorro programado con beneficio tributario en renta si se mantiene a largo plazo."],
    ("Porvenir", "Fondo de Pensión Voluntaria"): ["👴 **Portafolios Porvenir:** Más de 50 alternativas locales e internacionales con beneficio tributario."],
    ("Protección", "Fondo de Pensión Voluntaria"): ["🛡️ **Portafolios Protección:** Estrategias conservadoras o globales para retiro y optimización fiscal."],
    ("eToro", "Criptomonedas"): ["₿ **Criptoactivos reales:** Compra directa con diferencial (spread) incluido en el precio."],
    ("eToro", "Acciones Individuales"): ["🏢 **Acciones y Copy Trading:** Cero comisión en acciones reales; opción de copiar portafolios."],
    ("eToro", "ETFs"): ["📊 **SPY, QQQ, VOO:** Disponibles en dólares."],
    ("eToro", "ETFs Sectoriales"): ["🚀 **ETFs temáticos:** Tecnología, energías renovables y salud."],
    ("Bitso", "Criptomonedas"): ["₿ **BTC, ETH, USDC:** Comisión en el spread (~0,5% - 1%). Debes declarar ganancias en renta."],
    ("Binance", "Criptomonedas"): ["₿ **Mercado Spot y P2P:** Comisión estándar del **0,1%**, la más baja del ecosistema cripto."],
    ("Wenia", "Criptomonedas"): ["🟣 **COPW, BTC, ETH:** Conexión directa con Nequi y Bancolombia. Sin seguro Fogafín."],
    ("Kraken", "Criptomonedas"): ["🐙 **Kraken Pro:** Alta seguridad institucional y comisiones bajas por volumen."],
    ("Buda", "Criptomonedas"): ["🇨🇱 **BTC, ETH, USDC:** Fondeo directo en pesos por PSE."]
}

def formatear_plazo(meses: int) -> str:
    if meses == 1:
        return "1 mes"
    if meses < 12:
        return f"{meses} meses"
    anios = meses // 12
    return f"{meses} meses ({anios} año)" if anios == 1 else f"{meses} meses ({anios} años)"

def main():
    trm_vivo = obtener_trm_actual()
    
    html('<div class="hero"><h1>🤖 Asesor Inteligente de Inversiones</h1><p>Configura tu perfil para obtener opciones de mercado basadas en IA.</p></div>')
    st.subheader("1. Configura tu Inversión")
    
    primera = st.selectbox("¿Es tu primera vez invirtiendo?", ["Sí, es mi primera vez", "No, ya he invertido antes"], index=None, placeholder="Elige una opción")
    objetivo = st.selectbox("¿Para qué quieres invertir?", motor.OBJETIVOS, index=None, placeholder="Elige una opción")
    moneda_txt = st.selectbox("¿En qué moneda prefieres invertir?", ["Pesos Colombianos (COP)", "Dólares (USD)"], index=None, placeholder="Elige una opción")
    plazo_txt = st.selectbox("¿A qué plazo?", options=motor.PLAZOS, format_func=formatear_plazo, index=None, placeholder="Elige una opción")

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
        with st.spinner("Calculando impuestos, comisiones y rentabilidades personalizadas por entidad..."):
            puntos = sum(dict(o)[r] for (_, o), r in zip(motor.PREGUNTAS, resp_actualizadas))
            perfil = motor.perfil_desde_puntos(puntos)
            
            pref_moneda_motor = "Dólares" if moneda == "USD" else "Pesos"
            out = motor.recomendar(
                primera_vez=(primera == "Sí, es mi primera vez"),
                monto=float(monto),
                moneda=moneda,
                trm=trm_vivo, 
                plazo=plazo_txt,
                perfil=perfil,
                pref_moneda=pref_moneda_motor,
                pref_entidad=motor.ENTIDAD_IGUAL,
                aporte_mensual=float(aporte) if aporte is not None else 0.0,
                n=10 
            )
            
            plazo_legible = formatear_plazo(plazo_txt)
            st.markdown(f"### Tu Perfil IA: **{perfil}** (Puntaje: {puntos})")
            
            monto_str = motor.fmt(float(monto), moneda)
            texto_info = f"⏱️ **Parámetros de simulación:** Capital inicial de **{monto_str}** | Plazo elegido: **{plazo_legible}**"
            if aporte:
                aporte_str = motor.fmt(float(aporte), moneda)
                texto_info += f" | Aporte mensual: **{aporte_str}**"
            st.info(texto_info)
            
            monto_usd = motor.a_usd(float(monto), moneda, trm_vivo)
            aporte_val = float(aporte) if aporte is not None else 0.0
            
            activos_solo_cop = [
                "CDT", "Cuenta de Ahorro Remunerada", "Fondo de Deuda",
                "Carteras Colectivas", "Bonos de Gobierno", "Fondo de Pensión Voluntaria"
            ]
            mostro_alguno = False
            
            for i, r in enumerate(out["resultados"]):
                act_tipo = r['tipo']
                
                tasa_base_ea = r['rendimiento_anual_pct']
                com_base_pct = r['comision_pct']
                
                plataformas_completas = []
                for p in motor.PLATAFORMAS:
                    if act_tipo not in p.get('tipos', []):
                        continue
                    if moneda == "USD":
                        if act_tipo in activos_solo_cop and p.get("origen") == "Colombia":
                            continue
                        if "USD" in p.get("moneda", "") or p.get("origen") == "Internacional":
                            plataformas_completas.append(p)
                    else:
                        if "COP" in p.get("moneda", ""):
                            plataformas_completas.append(p)
                
                if not plataformas_completas:
                    continue

                mostro_alguno = True
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
                        nombre_ent = p['nombre']
                        info_ent = PERFIL_ENTIDADES.get(nombre_ent, {
                            "tipo": "Entidad Financiera / Plataforma",
                            "que_es": p.get('regulacion', 'Plataforma de inversión.'),
                            "como_funciona": p.get('nota', 'Permite invertir en este instrumento desde su portal.'),
                            "delta_tasa": 0.0,
                            "delta_com": 0.0,
                        })
                        
                        tasa_ent_ea = max(0.5, tasa_base_ea + info_ent["delta_tasa"])
                        com_ent_pct = max(0.0, com_base_pct + info_ent["delta_com"])
                        tasa_ent_mv = ((1 + tasa_ent_ea / 100) ** (1 / 12) - 1) * 100
                        tasa_ent_diaria = ((1 + tasa_ent_ea / 100) ** (1 / 365) - 1) * 100
                        
                        df_serie = motor.proyeccion(float(monto), aporte_val, tasa_ent_ea, com_ent_pct, plazo_txt)
                        total_aportado = float(monto) + aporte_val * plazo_txt
                        valor_final = float(df_serie["Con tu inversión"].iloc[-1])
                        ganancia_neta = valor_final - total_aportado
                        descuento_total = total_aportado * (com_ent_pct / 100)
                        ganancia_bruta = ganancia_neta + descuento_total

                        if monto_usd < p['min_usd']:
                            st.warning(f"⚠️ **Atención:** El mínimo sugerido aquí es {p['minimo_txt']}. Tu monto actual no alcanza, pero revisa cómo funciona para el futuro.")
                        
                        vigilada_txt = "✅ Vigilada Superfinanciera" if p.get("vigilada_sfc") else "🌐 Regulación Internacional / Sin vigilancia SFC"
                        html(f"""
                        <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-left: 4px solid #0ea5e9; border-radius: 10px; padding: 14px 16px; margin-bottom: 14px;">
                          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 6px; margin-bottom: 6px;">
                            <span style="font-weight: 800; color: #0f172a; font-size: 1.05rem;">🏛️ {nombre_ent} — {info_ent['tipo']}</span>
                            <span style="background: #e0f2fe; color: #0369a1; padding: 3px 10px; border-radius: 999px; font-size: 0.78rem; font-weight: 700;">{vigilada_txt}</span>
                          </div>
                          <p style="margin: 4px 0; font-size: 0.9rem; color: #334155;"><b>¿Qué es?:</b> {info_ent['que_es']}</p>
                          <p style="margin: 4px 0 0 0; font-size: 0.9rem; color: #334155;"><b>¿Cómo funciona?:</b> {info_ent['como_funciona']}</p>
                        </div>
                        """)
                        
                        col_izq, col_der = st.columns([1.3, 1])
                        with col_izq:
                            st.write(f"**💸 Costos/Comisiones (Tarifario):** {p['costos']}")
                            
                            catalogo = CATALOGO_FINANCIERO_DETALLADO.get((nombre_ent, act_tipo), [])
                            if catalogo:
                                st.markdown("---")
                                st.markdown(f"**⚖️ Opciones e Impuestos ({act_tipo} en {nombre_ent}):**")
                                for item in catalogo:
                                    st.markdown(f"- {item}")
                            else:
                                st.info(f"📌 {act_tipo} disponible en {nombre_ent}. Costos e impuestos según política general de la app.")
                            
                        with col_der:
                            with st.container(border=True):
                                st.markdown(f"##### 💰 Proyección en {nombre_ent}")
                                st.write(f"⏱️ **Plazo elegido:** {plazo_legible}")
                                st.write(f"📈 **Tasa Efectiva Anual:** {tasa_ent_ea:.2f}% E.A.")
                                st.write(f"🗓️ **Tasa Mes Vencido:** {tasa_ent_mv:.2f}% M.V. *(~{tasa_ent_diaria:.4f}% diario)*")
                                st.write(f"🏷️ **Comisión/Costo Est.:** {com_ent_pct:.2f}%")
                                st.markdown("---")
                                st.write(f"Capital Aportado: **{motor.fmt(total_aportado, moneda)}**")
                                st.write(f"Ganancia Bruta: **+ {motor.fmt(ganancia_bruta, moneda)}**")
                                st.write(f"Desc./Impuestos Est.: **- {motor.fmt(descuento_total, moneda)}**")
                                st.markdown(f"#### Libre para ti: <span style='color:#059669'>**{motor.fmt(valor_final, moneda)}**</span>", unsafe_allow_html=True)
                            
                            df_serie.rename(columns={
                                "Con tu inversión": f"Crecimiento en {nombre_ent}",
                                "Solo lo que aportas": "Bolsillo"
                            }, inplace=True)
                            st.area_chart(df_serie, color=["#0ea5e9", "#94a3b8"], height=230)
            
            if not mostro_alguno:
                st.warning("No se encontraron entidades disponibles en la moneda seleccionada para el perfil de riesgo actual.")
                
if __name__ == "__main__":
    main()
