def obtener_estilos():
    return """
    <style>
        /* Fondo base oscuro estilo Trii */
        .stApp {
            background-color: #0b0e14;
            color: #ffffff;
        }
        
        /* Títulos llamativos en Cian/Azul neón */
        h1, h2, h3 {
            color: #00d3a2 !important;
            font-weight: 800 !important;
        }
        
        /* Botones de acción principales */
        div[data-testid="stButton"] > button {
            background-color: #0052cc;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 2rem;
            font-weight: bold;
            width: 100%;
            transition: all 0.3s ease;
        }
        
        div[data-testid="stButton"] > button:hover {
            background-color: #00d3a2;
            color: #0b0e14;
            transform: scale(1.02);
        }
        
        /* Números grandes y métricas */
        div[data-testid="stMetricValue"] {
            color: #00d3a2 !important;
            font-size: 2.5rem !important;
        }
        
        /* Alerta dinámica y pulsante para montos inválidos */
        .alerta-minimo {
            background-color: #ff3366;
            color: white;
            padding: 15px;
            border-radius: 8px;
            font-weight: bold;
            text-align: center;
            animation: pulse 1.5s infinite;
            margin-top: 10px;
            margin-bottom: 20px;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.03); }
            100% { transform: scale(1); }
        }
    </style>
    """