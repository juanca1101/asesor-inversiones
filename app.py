import streamlit as st
import pandas as pd
import numpy as np
from estilos import obtener_estilos # Importación obligatoria

# Configuración de página
st.set_page_config(page_title="Asesor Inversiones", layout="wide", page_icon="📈")

def main():
    # Inyectar CSS actualizado (letras blancas)
    st.markdown(obtener_estilos(), unsafe_allow_html=True)
    
    st.title("🚀 Haz crecer tu capital")
    st.markdown("Plataforma de inversión inteligente. Rápido, seguro y a tu medida.")

    col_input, col_grafico = st.columns([1, 1.5])

    with col_input:
        st.subheader("Configura tu Inversión")
        
        moneda = st.radio("Selecciona tu moneda:", ["COP", "USD"])
        
        # Ajuste a promedios de mercado: $30.000 COP y $10 USD
        val_defecto = 30000 if moneda == "COP" else 10
        paso = 10000 if moneda == "COP" else 5
        
        monto_input = st.number_input(
            "Ingresa el monto a invertir:", 
            min_value=0, 
            value=val_defecto, 
            step=paso,
            format="%d"
        )
        
        monto_formateado = f"{monto_input:,.0f}".replace(",", ".")
        st.metric(label="Capital a Invertir", value=f"${monto_formateado} {moneda}")

        minimo_alcanzado = False
        
        # Validaciones con los nuevos mínimos
        if moneda == "COP" and monto_input < 30000:
            st.markdown('<div class="alerta-minimo">⚠️ El monto mínimo sugerido para iniciar por tarifas es de $30.000 COP.</div>', unsafe_allow_html=True)
        elif moneda == "USD" and monto_input < 10:
            st.markdown('<div class="alerta-minimo">⚠️ El monto mínimo sugerido para iniciar es de $10 USD.</div>', unsafe_allow_html=True)
        else:
            minimo_alcanzado = True
            st.success("✅ Monto excelente para comenzar.")

        st.button("Calcular Portafolio") 

    with col_grafico:
        st.subheader("Proyección de Crecimiento")
        
        if minimo_alcanzado:
            meses = pd.date_range(start="2024-01-01", periods=12, freq="ME")
            crecimiento = [monto_input * (1 + (0.015 * i) + np.random.normal(0, 0.02)) for i in range(12)]
            df_grafico = pd.DataFrame({"Fecha": meses, "Valor Proyectado": crecimiento}).set_index("Fecha")
            
            # Gráfico con el azul/cian para que resalte hermoso sobre el negro
            st.line_chart(df_grafico, use_container_width=True, color="#0052cc")
        else:
            st.info("Ingresa el monto mínimo requerido para visualizar el potencial de tu dinero.")

if __name__ == "__main__":
    main()