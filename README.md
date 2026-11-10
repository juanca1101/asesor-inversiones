# Asesor de Inversiones con IA (web)

Archivos:
- `dataset_asesor_inversiones_500.csv`: datos de entrenamiento
- `entrenar.py`: entrena los modelos y guarda `modelo.joblib` (se ejecuta solo si no existe)
- `motor.py`: cuestionario de perfil + lógica de recomendación
- `app.py`: la página web (Streamlit)
- `requirements.txt`: librerías

## Probarla en tu computador
```bash
pip install -r requirements.txt
streamlit run app.py
```
Se abre en http://localhost:8501

## Publicarla gratis con un link público (Streamlit Community Cloud)
1. Crea una cuenta en https://github.com y un repositorio **público** nuevo (ej. `asesor-inversiones`).
2. Sube TODOS los archivos de esta carpeta al repositorio (botón "Add file > Upload files").
   No subas `modelo.joblib`: la app lo crea sola al arrancar.
3. Entra a https://share.streamlit.io e inicia sesión con GitHub.
4. Clic en **Create app** > elige tu repositorio, rama `main`, archivo principal `app.py`.
5. Clic en **Deploy**. En 2-3 minutos tienes un link tipo `https://tu-app.streamlit.app` para compartir.

Cada vez que cambies algo en GitHub, la página se actualiza sola.

## Alternativas
- **Hugging Face Spaces** (gratis): New Space > SDK Streamlit > sube los archivos.
- **Render.com**: Web Service con comando de inicio
  `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
- **Dominio propio** (ej. miasesor.com): se compra aparte y se apunta a Render/Hugging Face;
  Streamlit Community Cloud gratis solo da el subdominio `.streamlit.app`.

## Nota
Proyecto académico con datos sintéticos. No es asesoría financiera.
