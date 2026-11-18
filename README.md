# 📈 Asesor Inteligente de Inversiones con IA

Aplicación web interactiva desarrollada en **Python** y **Streamlit** que democratiza el acceso a decisiones financieras informadas en Colombia mediante **Machine Learning**. El sistema perfila al inversionista mediante un test psicométrico, predice los activos más adecuados con modelos de *Gradient Boosting*, consulta la TRM en vivo mediante una API REST y proyecta rendimientos netos descontando comisiones e impuestos locales en 17 entidades reales.

---

## 🚀 Características Principales
- **Perfilamiento Psicométrico:** Cuestionario de 7 preguntas (escala de 7 a 21 puntos) que clasifica la tolerancia al riesgo en **Bajo**, **Medio** o **Alto**.
- **Predicción Multi-Modelo (ML):** Utiliza tres modelos de *Gradient Boosting* entrenados con 2.000 registros para recomendar entre **11 tipos de activos** y estimar tasas y comisiones.
- **Consumo de API REST en Tiempo Real:** Consulta la tasa de cambio oficial **USD/COP** mediante `ExchangeRate-API` con caché de 1 hora (`@st.cache_data`) y sistema de respaldo ante fallos.
- **Filtrado Estricto por Moneda:** Separa automáticamente los instrumentos en **Pesos Colombianos (COP)** de las opciones internacionales en **Dólares (USD)**, mostrando equivalencias aproximadas en pesos para facilitar la lectura.
- **Desglose Financiero y Tributario:** Calcula tasas **Efectiva Anual (E.A.)**, **Mes Vencido (M.V.)** y **Diaria**, retenciones en la fuente (4% en CDTs, 7% en cuentas remuneradas y fondos, 10% a 30% en dividendos) y redirige al sitio oficial de cada entidad.

---

## 🧠 Arquitectura y Modelos de Machine Learning (`entrenar.py`)
El sistema entrena tres algoritmos independientes de *Gradient Boosting* (`scikit-learn`) validados mediante **Validación Cruzada de 5 particiones (`5-Fold Cross-Validation`)** sobre 2.000 registros:

1. **`clf_tipo` (`GradientBoostingClassifier`):** Clasifica y ordena los 11 tipos de activos compatibles con el perfil del usuario (60 árboles, profundidad 2).
   - *Efectividad:* **89.8% Top-3 Accuracy** (74.5% Top-2 / 42.7% Top-1).
2. **`reg_rend` (`GradientBoostingRegressor`):** Predice la tasa de rendimiento anual esperada en porcentaje E.A. (150 árboles, profundidad 3).
   - *Efectividad:* **$R^2 = 0.87$ (86.5% de varianza explicada)** | MAE: $\pm 1.64\%$.
3. **`reg_com` (`GradientBoostingRegressor`):** Estima el porcentaje de comisión asociada al instrumento (150 árboles, profundidad 3).
   - *Efectividad:* **$R^2 = 0.83$ (82.9% de varianza explicada)** | MAE: $\pm 0.22\%$.

*Nota: El archivo binario `modelo.joblib` está excluido en `.gitignore` como buena práctica de control de versiones; al iniciar la aplicación por primera vez, `motor.py` ejecuta `entrenar.py` automáticamente para generarlo en el servidor.*

---

## 📁 Estructura del Repositorio
```text
├── app.py                              # Interfaz web (Streamlit), consumo de API TRM y desglose tributario
├── motor.py                            # Test psicométrico (7 preguntas), inferencia ML y proyección compuesta
├── entrenar.py                         # Ingeniería de características (One-Hot, np.log), 5-Fold CV y entrenamiento
├── plataformas.py                      # Catálogo de 17 entidades financieras (10 colombianas y 7 internacionales)
├── estilos.py                          # Estilos CSS personalizados para la interfaz
├── generar_dataset.py                  # Ampliación estadística de 500 registros base a 2.000 registros
├── dataset_asesor_inversiones_2000.csv # Dataset de entrenamiento (2.000 registros, 11 activos, 17 entidades)
├── requirements.txt                    # Dependencias del proyecto[cite: 2]
├── .streamlit/config.toml              # Configuración visual del tema en Streamlit[cite: 2]
└── .gitignore                          # Exclusión de archivos temporales y modelo.joblib[cite: 2, 5]
