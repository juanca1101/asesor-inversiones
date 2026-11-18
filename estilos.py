def obtener_estilos():
    return """
    <style>
        /* Fondo base oscuro estilo Trii */
        .stApp {
            background-color: #0b0e14;
            color: #ffffff; /* Texto principal en blanco */
        }
        
        /* Títulos en blanco para que resalten más y se vean serios */
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff !important;
            font-weight: 800 !important;
        }
        
        /* Etiquetas de los inputs y campos de texto */
        label {
            color: #d1d5db !important; /* Gris muy claro/casi blanco */
            font-weight: 500 !important;
            font-size: 1.1rem !important;
        }
        
        /* Ajustar el color dentro de las cajas de texto a blanco */
        input {
            color: #ffffff !important;
            background-color: #1e293b !important;
        }
        
        /* Botones de acción principales (mantienen el azul Trii) */
        div[data-testid="stButton"] > button {
            background-color: #0052cc;
            color: white; /* Texto del botón en blanco */
            border: none;
            border-radius: 8px;
            padding: 0.75rem 2rem;
            font-weight: bold;
            width: 100%;
            transition: all 0.3s ease;
        }
        
        div[data-testid="stButton"] > button:hover {
            background-color: #0040a8;
            color: white;
            transform: scale(1.02);
        }
        
        /* Números gigantes y métricas en blanco puro */
        div[data-testid="stMetricValue"] {
            color: #ffffff !important;
            font-size: 2.5rem !important;
            font-weight: 700 !important;
        }
        
        /* Alerta dinámica para montos inválidos (rojo suave con letras blancas) */
        .alerta-minimo {
            background-color: #e11d48;
            color: #ffffff; /* Letras blancas para el error */
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