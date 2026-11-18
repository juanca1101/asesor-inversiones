import streamlit as st
import pandas as pd
import numpy as np

# ⚠️ IMPORTANTE: Esta línea evita que la app se quede en blanco
from estilos import obtener_estilos

# st.set_page_config DEBE ser el primer comando de Streamlit
st.set_page_config(page_title="Asesor Inversiones", layout="wide", page_icon="📈")

def main():
    # Inyectar CSS
    st.markdown(obtener_estilos(), unsafe_allow_html=True)
    
    st.title("🚀 Haz crecer tu capital")
    st.markdown("Plataforma de inversión inteligente. Rápido, seguro y a tu medida.")

    # Dividir la pantalla en dos columnas para mejor visualización
    col_input, col_grafico = st.columns([1, 1.5])

    with col_input:
        st.subheader("Configura tu Inversión")
        
        moneda = st.radio("Selecciona tu moneda:", ["COP", "USD"])
        
        # Valores por defecto y pasos dinámicos según la moneda
        val_defecto = 50000 if moneda == "COP" else 15
        paso = 10000 if moneda == "COP" else 5
        
        # El input nativo de Streamlit no permite forzar puntos mientras el usuario escribe,
        # por lo que capturamos el número puro y lo mostramos gigante abajo ya formateado.
        monto_input = st.number_input(
            "Ingresa el monto a invertir:", 
            min_value=0, 
            value=val_defecto, 
            step=paso,
            format="%d"
        )
        
        # Lógica para formatear con puntos de miles (ej: 50.000)
        monto_formateado = f"{monto_input:,.0f}".replace(",", ".")
        st.metric(label="Capital a Invertir", value=f"${monto_formateado} {moneda}")

        # Validación de mínimos
        minimo_alcanzado = False
        if moneda == "COP" and monto_input < 50000:
            st.markdown('<div class="alerta-minimo">⚠️ ¡Ups! El monto mínimo para iniciar es de $50.000 COP. ¡Súbele un poco para empezar a invertir!</div>', unsafe_allow_html=True)
        elif moneda == "USD" and monto_input < 15:
            st.markdown('<div class="alerta-minimo">⚠️ ¡Ups! El monto mínimo para iniciar es de $15 USD. ¡Súbele un poco para empezar a invertir!</div>', unsafe_allow_html=True)
        else:
            minimo_alcanzado = True
            st.success("✅ Monto excelente para comenzar.")

        st.button("Calcular Portafolio") # Aquí conectarías tu motor.py

    with col_grafico:
        st.subheader("Proyección de Crecimiento")
        
        if minimo_alcanzado:
            # Generar datos simulados para un gráfico llamativo estilo Trii
            meses = pd.date_range(start="2024-01-01", periods=12, freq="ME")
            
            # Simular un crecimiento positivo con algo de volatilidad
            crecimiento = [monto_input * (1 + (0.015 * i) + np.random.normal(0, 0.02)) for i in range(12)]
            
            df_grafico = pd.DataFrame({"Fecha": meses, "Valor Proyectado": crecimiento}).set_index("Fecha")
            
            # Mostrar gráfico con el color verde/cian del tema
            st.line_chart(df_grafico, use_container_width=True, color="#00d3a2")
        else:
            st.info("Ingresa el monto mínimo requerido para visualizar el potencial de tu dinero.")

if __name__ == "__main__":
    main()