# Asesor de Inversiones con IA (web) - versión 2

Archivos (todos deben quedar en la raíz del repositorio de GitHub):
- `app.py`: la página web (Streamlit), con asistente de 3 pasos
- `motor.py`: cuestionario de perfil + lógica de recomendación (moneda, entidades, proyección)
- `plataformas.py`: catálogo de 17 entidades colombianas e internacionales (datos aprox. nov-2026)
- `estilos.py`: diseño visual (CSS)
- `entrenar.py`: entrena los modelos y crea `modelo.joblib` (se ejecuta solo si no existe)
- `dataset_asesor_inversiones_2000.csv`: datos de entrenamiento ampliados (500 originales + 1500 simulados)
- `dataset_asesor_inversiones_500.csv`: dataset original (respaldo)
- `generar_dataset.py`: script que genera el dataset de 2000 filas
- `requirements.txt`: librerías
- `.streamlit/config.toml`: colores del tema (carpeta oculta con punto al inicio)
- `.gitignore`: evita subir `modelo.joblib`

## Probarla en tu computador
```bash
pip install -r requirements.txt
streamlit run app.py
```
Se abre en http://localhost:8501

## Publicarla (resumen)
1. Sube los archivos a un repositorio público de GitHub.
2. En https://share.streamlit.io crea la app: repositorio, rama `main`, archivo `app.py`, Deploy.

Para crear `.streamlit/config.toml` en GitHub: Add file > Create new file, escribe como nombre
`.streamlit/config.toml` (al escribir la barra se crea la carpeta) y pega el contenido del archivo.

## Mantenimiento
- Las tasas, mínimos y comisiones de `plataformas.py` cambian con el tiempo: actualízalas.
- La TRM por defecto está en `motor.py` (`TRM_DEFECTO`); el usuario puede cambiarla en "Ajustes avanzados".

## Nota
Proyecto académico con datos sintéticos. No es asesoría financiera.
