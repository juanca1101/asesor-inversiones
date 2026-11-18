CSS = """
<style>
/* Modern Light Mode - Fondo Blanco */
#MainMenu, footer {visibility: hidden;}
.stApp {background-color: #f8fafc; color: #1e293b; font-family: 'Inter', sans-serif;}
.block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 900px;}

/* Títulos Limpios */
h1, h2, h3, h4, h5 {color: #0f172a !important; font-weight: 800; letter-spacing: -0.02em;}

/* Tarjeta Principal Hero (Degradado Suave) */
.hero {background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%); color: #fff; border-radius: 20px; padding: 32px 30px; margin-bottom: 24px; box-shadow: 0 10px 25px rgba(59,130,246,.25);}
.hero h1 {color: #fff !important; margin: 0 0 8px 0; font-size: 2.2rem;}
.hero p {color: rgba(255,255,255,.9); font-size: 1.1rem; margin: 0;}

/* Tarjetas de Resultados (Blanco puro con sombra) */
.card {background: #ffffff; border-radius: 16px; padding: 24px; margin-bottom: 16px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,.05), 0 2px 4px -1px rgba(0,0,0,.03); transition: all 0.2s ease;}
.card:hover {transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0,0,0,.1);}
.card-header {display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px;}
.card-title {font-size: 1.4rem; font-weight: 700; color: #1e293b; margin: 0;}

/* Insignias (Badges) */
.badge {padding: 6px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;}
.b-cop {background: #fef3c7; color: #b45309;}
.b-usd {background: #dcfce7; color: #166534;}
.b-mix {background: #f1f5f9; color: #475569;}

/* Grid de Métricas con diseño limpio */
.metric-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 16px;}
.metric {background: #f1f5f9; padding: 16px; border-radius: 12px; text-align: center; border: 1px solid #e2e8f0;}
.lbl {font-size: 0.85rem; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;}
.val {font-size: 1.4rem; font-weight: 800; color: #0f172a;}
.val.pos {color: #059669;}
.small {font-size: 0.95rem; color: #64748b; line-height: 1.5; margin-top: 16px; padding-top: 16px; border-top: 1px solid #e2e8f0;}

/* Forzar que los inputs vacíos se vean bien */
div[data-testid="stNumberInput"] input, div[data-testid="stSelectbox"] > div > div {background-color: #ffffff; color: #1e293b; border: 1px solid #cbd5e1; border-radius: 8px;}
div[data-testid="stButton"] > button {background-color: #3b82f6; color: white; border-radius: 8px; font-weight: 600; padding: 0.75rem 1.5rem; border: none; width: 100%;}
div[data-testid="stButton"] > button:hover {background-color: #2563eb; transform: scale(1.02);}
</style>
"""