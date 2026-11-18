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
# DICCIONARIO MAESTRO: 100% DE LAS COMBINACIONES MAPEADAS
# ==============================================================================
EJEMPLOS_ESPECIFICOS = {
    # TRII
    ("Trii", "Acciones Individuales"): "Acciones locales: Ecopetrol, Bancolombia, Celsia, ISA, Grupo Argos. Globales: Nu Holdings, Apple.",
    ("Trii", "ETFs"): "iShares COLCAP (Bolsa colombiana), ETF S&P 500 (Bolsa de EE.UU.).",
    ("Trii", "ETFs Sectoriales"): "ETFs de tecnología, energía o financieros disponibles en el MGC.",
    ("Trii", "Carteras Colectivas"): "Fondo Acciones & Valores Vista (Bajo riesgo, liquidez inmediata).",
    ("Trii", "Fondo de Deuda"): "Fondo Renta Fija Acciones & Valores.",
    ("Trii", "CDT"): "CDT Digital Acciones & Valores (Lo abres directamente en la app).",
    ("Trii", "Fondos Indexados"): "Fondo Indexado Global (Búscalo en la sección de fondos).",
    ("Trii", "Bonos de Gobierno"): "Fondo mutuo enfocado en TES colombianos.",
    
    # TYBA
    ("tyba", "Carteras Colectivas"): "Fondo tyba Pocket (Bajo riesgo), Fondo Acciones Globales (Alto riesgo).",
    ("tyba", "Fondo de Deuda"): "Fondo Renta Fija Credicorp Capital.",
    ("tyba", "CDT"): "CDT Digital Mibanco (Contratado directo en tyba sin papeleo).",
    ("tyba", "Fondos Indexados"): "Fondos indexados Credicorp atados al S&P 500.",
    ("tyba", "Fondo de Pensión Voluntaria"): "Portafolio de Pensión Voluntaria (Beneficios tributarios).",
    ("tyba", "Bonos de Gobierno"): "Fondo de inversión enfocado en deuda pública (TES).",

    # LULO BANK & NU COLOMBIA & PIBANK
    ("Lulo Bank", "Cuenta de Ahorro Remunerada"): "Bolsillos Lulo (Crea una meta y guarda ahí el dinero con rentabilidad).",
    ("Lulo Bank", "CDT"): "CDT Lulo Bank (Se abre en 2 clics desde la app, tasa fija).",
    ("Nu Colombia", "Cuenta de Ahorro Remunerada"): "Cajitas Nu (Mueve tu plata a la cajita para generar rendimiento diario).",
    ("Nu Colombia", "CDT"): "CDT Digital Nu (Plazos desde 60 días, sin 4x1000 al fondear desde Cajitas).",
    ("Pibank", "Cuenta de Ahorro Remunerada"): "Cuenta Pibank (Liquidación mensual automática).",
    ("Pibank", "CDT"): "CDT Pibank (Con pago de intereses al vencimiento o mensuales).",

    # DAVIVIENDA
    ("Davivienda", "CDT"): "CDT Móvil Davivienda (Desde la app transaccional).",
    ("Davivienda", "Carteras Colectivas"): "Fondo Superior, Fondo Interés.",
    ("Davivienda", "Fondo de Deuda"): "Fondo Renta Fija Plazo 30.",
    ("Davivienda", "Fondo de Pensión Voluntaria"): "Dafuturo (Elige el portafolio Conservador o Moderado).",

    # BANCOLOMBIA ETRADING
    ("Bancolombia eTrading", "Acciones Individuales"): "Acciones locales del COLCAP y Mercado Global Colombiano (MGC).",
    ("Bancolombia eTrading", "ETFs"): "iShares COLCAP, ETFs globales a través de MGC.",
    ("Bancolombia eTrading", "Carteras Colectivas"): "Fiducuenta o Plan Semilla (En la App principal de Bancolombia).",
    ("Bancolombia eTrading", "Fondo de Deuda"): "Fidurenta Bancolombia.",
    ("Bancolombia eTrading", "CDT"): "CDT Físico o Virtual Bancolombia.",
    ("Bancolombia eTrading", "Bonos de Gobierno"): "Participación en subastas de TES o fondos de renta fija pública.",

    # HAPI
    ("Hapi", "Fondos Indexados"): "Busca los tickers indexados: VOO (S&P 500) o QQQ (Nasdaq 100).",
    ("Hapi", "ETFs"): "VOO, QQQ, DIA (Dow Jones), VTI.",
    ("Hapi", "ETFs Sectoriales"): "XLK (Tecnología), XLV (Salud), XLE (Energía).",
    ("Hapi", "Acciones Individuales"): "Fracciones desde $5 USD (Tesla, Apple, Amazon, Nvidia).",
    ("Hapi", "Carteras Colectivas"): "Portafolios temáticos o fondos mutuos disponibles en la plataforma.",
    ("Hapi", "Criptomonedas"): "Puedes comprar Bitcoin o Ethereum directamente con tu saldo en USD.",

    # INTERACTIVE BROKERS
    ("Interactive Brokers", "Fondos Indexados"): "Fondos mutuos indexados de Vanguard (VFIAX) o ETFs equivalentes (VOO, IVV).",
    ("Interactive Brokers", "ETFs"): "VOO, QQQ, VT (Vanguard Total World).",
    ("Interactive Brokers", "ETFs Sectoriales"): "Cualquier ETF global (XLF, XLK, ICLN).",
    ("Interactive Brokers", "Acciones Individuales"): "Cualquier acción listada en NYSE o NASDAQ (AAPL, MSFT, TSLA).",
    ("Interactive Brokers", "Carteras Colectivas"): "Miles de Mutual Funds (Fondos Mutuos) de BlackRock, Vanguard, Fidelity.",
    ("Interactive Brokers", "Bonos de Gobierno"): "Bonos del tesoro de EE.UU. (T-Bills, T-Bonds).",

    # ETORO
    ("eToro", "Acciones Individuales"): "Apple, Microsoft, y copy-trading de inversores reales.",
    ("eToro", "ETFs"): "VOO, SPY, QQQ.",
    ("eToro", "ETFs Sectoriales"): "ETFs de tecnología, cannabis, energías limpias.",
    ("eToro", "Criptomonedas"): "Bitcoin, Cardano, Solana (Compra el activo subyacente).",

    # FONDOS DE PENSIÓN (PORVENIR & PROTECCIÓN)
    ("Porvenir", "Fondo de Pensión Voluntaria"): "Portafolio Conservador, Moderado o Crecimiento.",
    ("Protección", "Fondo de Pensión Voluntaria"): "Portafolio Liquidez, Portafolio Acciones Globales.",

    # CRIPTOMONEDAS BÁSICAS
    ("Wenia", "Criptomonedas"): "COPW (Criptopeso para evitar volatilidad), Bitcoin (BTC), Ethereum (ETH).",
    ("Bitso", "Criptomonedas"): "Bitcoin (BTC), Ethereum (ETH), USDC (Dólar digital estable).",
    ("Binance", "Criptomonedas"): "Bitcoin (BTC), Ethereum (ETH), USDT, y cientos de altcoins (Alto riesgo).",
    ("Kraken", "Criptomonedas"): "Bitcoin (BTC), Ethereum (ETH), USDC.",
    ("Buda", "Criptomonedas"): "Bitcoin (BTC), Ethereum (ETH), USDC (Depósito fácil por PSE)."
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
        with st.spinner("Desbloqueando todo el catálogo de entidades (Procesando 100% de la base)..."):
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
                
                # REGLA FORZADA: Buscar en el 100% de la base (Si aquí no sale Davivienda o Tyba, es porque no estabas seleccionando un activo que ellos tengan)
                plataformas_completas = []
                for p in motor.PLATAFORMAS:
                    if act_tipo in p.get('tipos', []):
                        plataformas_completas.append(p)
                
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
                        # AVISO de montos
                        if monto_usd < p['min_usd']:
                            st.warning(f"⚠️ **Atención:** El mínimo sugerido aquí es {p['minimo_txt']}. Tu monto actual no alcanza, pero te mostramos la opción para que la conozcas a futuro.")
                        
                        col_izq, col_der = st.columns([1, 1.2])
                        with col_izq:
                            st.write(f"**📱 App/Banco:** {p['nombre']}")
                            st.write(f"**💸 Costos/Comisiones reales:** {p['costos']}")
                            
                            # AQUÍ INYECTA EL DICCIONARIO COMPLETO
                            sugerencia = EJEMPLOS_ESPECIFICOS.get((p['nombre'], act_tipo), f"Búscalo como '{act_tipo}' en la barra de búsqueda de la app.")
                            st.info(f"**📌 ¿Qué debes buscar exactamente?:**\n\n{sugerencia}")
                            
                            st.markdown("---")
                            st.markdown("**💰 Tus números exactos:**")
                            st.write(f"Capital Aportado: **{motor.fmt(r['total_aportado'], moneda)}**")
                            st.write(f"Ganancia Bruta: **+ {motor.fmt(r['ganancia'] + (r['total_aportado'] * (r['comision_pct'] / 100)), moneda)}**")
                            st.write(f"Descuento/Comisión: **- {motor.fmt(r['total_aportado'] * (r['comision_pct'] / 100), moneda)}**")
                            st.markdown(f"#### Libre para ti: <span style='color:#059669'>**{motor.fmt(r['valor_final'], moneda)}**</span>", unsafe_allow_html=True)

                        with col_der:
                            df_serie = r['serie'].copy()
                            df_serie.rename(columns={
                                "Con tu inversión": f"Proyección en {p['nombre']}",
                                "Solo lo que aportas": "Bolsillo"
                            }, inplace=True)
                            st.area_chart(df_serie, color=["#0ea5e9", "#94a3b8"])
                
                st.markdown("<br><hr><br>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()