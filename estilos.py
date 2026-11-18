def obtener_estilos():
    return """
    <style>
        /* Fondo general oscuro */
        .stApp {
            background-color: #0f172a;
            color: #f8fafc;
            font-family: 'Inter', sans-serif;
        }
        
        /* Títulos */
        h1, h2, h3 {
            color: #f8fafc !important;
            font-weight: 700 !important;
        }
        
        /* Contenedores de inputs */
        div[data-testid="stNumberInput"] > div > div > input,
        div[data-testid="stSelectbox"] > div > div {
            background-color: #1e293b;
            color: #f8fafc;
            border: 1px solid #334155;
            border-radius: 8px;
        }
        
        /* Color del texto dentro de los inputs */
        input {
            color: #f8fafc !important;
        }
        
        /* Botones principales */
        div[data-testid="stButton"] > button {
            background-color: #0ea5e9;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 2rem;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        div[data-testid="stButton"] > button:hover {
            background-color: #38bdf8;
            transform: translateY(-2px);
        }
        
        /* Cajas de alerta / Info (Donde mostramos el monto formateado) */
        div[data-testid="stAlert"] {
            background-color: rgba(14, 165, 233, 0.1);
            border-left: 4px solid #0ea5e9;
            color: #e2e8f0;
        }
        
        /* Etiquetas de los campos */
        label {
            color: #94a3b8 !important;
            font-weight: 500;
        }
        
        /* Estilizar las tarjetas de recomendación (si usas st.metric o similares) */
        div[data-testid="stMetricValue"] {
            color: #38bdf8;
        }
    </style>
    """