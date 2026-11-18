import streamlit as st
import pandas as pd
from estilos import obtener_estilos # Asegúrate de mantener tu archivo estilos.py

st.set_page_config(page_title="Asesor de Inversiones", layout="wide", page_icon="🏦")

def calcular_rendimiento_neto(monto, tasa_ea, dias, porcentaje_comision_impuesto):
    """Calcula el rendimiento restando el % de retención o comisión"""
    rendimiento_bruto = monto * (((1 + tasa_ea)**(dias/360)) - 1)
    descuento = rendimiento_bruto * porcentaje_comision_impuesto
    rendimiento_neto = rendimiento_bruto - descuento
    return rendimiento_bruto, descuento, rendimiento_neto

def main():
    st.markdown(obtener_estilos(), unsafe_allow_html=True)
    st.title("🏦 Tu Asesor de Inversiones Personal")
    
    # -----------------------------------------
    # PASO 1: CÁLCULO DE PERFIL DE RIESGO
    # -----------------------------------------
    st.subheader("1. Descubre tu Perfil de Inversionista")
    col1, col2 = st.columns(2)
    
    with col1:
        q1 = st.selectbox("¿Cuál es tu objetivo principal al invertir?", 
                          ["Preservar mi capital (No quiero perder nada)", 
                           "Crecimiento moderado a mediano plazo", 
                           "Maximizar ganancias a largo plazo asumiendo riesgos"])
        
        q2 = st.selectbox("¿En cuánto tiempo planeas usar este dinero?", 
                          ["Menos de 1 año", "De 1 a 3 años", "Más de 3 años"])
    
    with col2:
        q3 = st.selectbox("Si tu inversión cae un 10% en un mes, ¿qué harías?", 
                          ["Vender todo inmediatamente para no perder más", 
                           "Esperar a que se recupere sin comprar más", 
                           "Comprar más porque está barato"])
        
        q4 = st.selectbox("¿Qué porcentaje de tus ahorros totales representa esta inversión?", 
                          ["Más del 50%", "Entre el 20% y 50%", "Menos del 20%"])

    # Lógica simple para determinar el perfil
    puntuacion = 0
    if q1 == "Crecimiento moderado a mediano plazo": puntuacion += 1
    elif q1 == "Maximizar ganancias a largo plazo asumiendo riesgos": puntuacion += 2
    if q3 == "Esperar a que se recupere sin comprar más": puntuacion += 1
    elif q3 == "Comprar más porque está barato": puntuacion += 2
    if q4 == "Menos del 20%": puntuacion += 1

    perfil = "Conservador 🛡️"
    if puntuacion >= 2 and puntuacion <= 3: perfil = "Moderado ⚖️"
    elif puntuacion > 3: perfil = "Arriesgado 🚀"

    st.info(f"**Tu perfil de riesgo estimado es: {perfil}**")
    st.markdown("---")

    # -----------------------------------------
    # PASO 2: CONFIGURACIÓN DEL MONTO
    # -----------------------------------------
    st.subheader("2. Simulación de Plataformas")
    
    col_moneda, col_monto = st.columns(2)
    with col_moneda:
        moneda = st.radio("¿En qué moneda deseas invertir?", ["COP (Pesos Colombianos)", "USD (Dólares)"])
    
    with col_monto:
        if "COP" in moneda:
            monto_input = st.number_input("Monto a invertir (Mín. sugerido $30.000)", min_value=0, value=1000000, step=50000, format="%d")
            st.metric(label="Capital (COP)", value=f"${monto_input:,.0f}".replace(",", "."))
            valido = monto_input >= 30000
        else:
            monto_input = st.number_input("Monto a invertir (Mín. sugerido $10)", min_value=0, value=100, step=10, format="%d")
            st.metric(label="Capital (USD)", value=f"${monto_input:,.0f}".replace(",", "."))
            valido = monto_input >= 10

    if not valido:
        st.markdown('<div class="alerta-minimo">⚠️ El monto ingresado está por debajo del mínimo sugerido para cubrir tarifas.</div>', unsafe_allow_html=True)
        return

    st.markdown("---")

    # -----------------------------------------
    # PASO 3: GRÁFICOS Y COMISIONES POR PLATAFORMA
    # -----------------------------------------
    if st.button("Ver Opciones del Mercado"):
        st.subheader("Resultados de Inversión a 1 Año (Estimado)")
        
        if "COP" in moneda:
            # Datos de plataformas en Colombia
            st.markdown("Cálculo basado en CDT/Cuentas de Ahorro. Se asume un **4% de Retención en la Fuente** sobre las ganancias.")
            plataformas = {
                "Lulo Bank (CDT/Bolsillos)": 0.13,  # 13% EA
                "Nu Bank (Cajitas)": 0.124,         # 12.4% EA
                "Banco AV Villas (CDT Digital)": 0.12, # 12% EA
                "Davivienda (CDT)": 0.1176          # 11.76% EA
            }
            impuesto = 0.04 # 4% de retención en la fuente sobre rendimientos
        else:
            # Datos de brokers internacionales para USD
            st.markdown("Cálculo basado en Brokers Internacionales invirtiendo en fondos conservadores (aprox. 5% EA). Se asumen **comisiones de gestión o conversión**.")
            plataformas = {
                "Interactive Brokers": {"tasa": 0.05, "comision": 0.01}, # 1% de costos de conversión/gestión
                "Trading 212": {"tasa": 0.05, "comision": 0.005},        # 0.5% conversión
                "Hapi": {"tasa": 0.05, "comision": 0.015}                # 1.5% costos de fondeo/retiro
            }

        # Generar las tarjetas y gráficos por plataforma
        tabs = st.tabs(list(plataformas.keys()))
        
        for i, (nombre_plat, datos) in enumerate(plataformas.items()):
            with tabs[i]:
                if "COP" in moneda:
                    tasa = datos
                    comision_pct = impuesto
                    label_descuento = "Retención en la Fuente (4%)"
                else:
                    tasa = datos["tasa"]
                    comision_pct = datos["comision"]
                    label_descuento = f"Comisiones/Costos ({(comision_pct*100):.1f}%)"

                # Cálculo financiero
                bruto, descuento, neto = calcular_rendimiento_neto(monto_input, tasa, 360, comision_pct)
                
                c1, c2 = st.columns([1, 1.5])
                with c1:
                    st.markdown(f"### {nombre_plat}")
                    st.write(f"**Tasa Efectiva Anual (E.A):** {tasa*100:.2f}%")
                    st.write(f"**Tu capital inicial:** ${monto_input:,.0f}".replace(",", "."))
                    st.write(f"**Ganancia bruta:** ${bruto:,.0f}".replace(",", "."))
                    st.write(f"**{label_descuento}:** -${descuento:,.0f}".replace(",", "."))
                    st.markdown(f"#### **Dinero Libre de Ganancia:** <span style='color:#00d3a2'>${neto:,.0f}</span>".replace(",", "."), unsafe_allow_html=True)
                    st.markdown(f"#### **Total a Retirar:** ${monto_input + neto:,.0f}".replace(",", "."), unsafe_allow_html=True)
                
                with c2:
                    # Gráfico de pastel para ver visualmente qué te queda vs qué pagas
                    df_grafico = pd.DataFrame({
                        "Concepto": ["Ganancia Libre para Ti", "Impuestos / Comisiones"],
                        "Valor": [neto, descuento]
                    })
                    
                    st.markdown("**Distribución de tus Rendimientos**")
                    # Usamos un gráfico de barras apiladas de streamlit para representar la división del rendimiento
                    st.bar_chart(df_grafico.set_index("Concepto"), use_container_width=True, color=["#00d3a2"])

if __name__ == "__main__":
    main()