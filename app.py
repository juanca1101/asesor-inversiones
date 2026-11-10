import streamlit as st

import motor
from estilos import CSS
from plataformas import ACTUALIZADO, PLATAFORMAS

st.set_page_config(
    page_title="Asesor de Inversiones IA",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.markdown(CSS, unsafe_allow_html=True)


# ------------------------------------------------------------------ utilidades
def H(texto: str) -> str:
    """Compacta el HTML (sin saltos de linea) y protege el signo $ para que no se lea como formula."""
    return " ".join(linea.strip() for linea in texto.splitlines() if linea.strip()).replace("$", "&#36;")


def html(texto: str) -> None:
    st.markdown(H(texto), unsafe_allow_html=True)


def badge_moneda(m: str) -> str:
    clase = {"COP": "b-cop", "USD": "b-usd"}.get(m, "b-mix")
    nombre = {"COP": "En pesos", "USD": "En dólares", "Mixta": "Pesos o dólares"}[m]
    return f'<span class="badge {clase}">{nombre}</span>'


# ------------------------------------------------------------------ estado
ESTADO_INICIAL = {
    "primera": "Sí",
    "objetivo": motor.OBJETIVOS[0],
    "moneda": "COP",
    "monto_COP": 3_000_000,
    "monto_USD": 1_000,
    "plazo": 24,
    "aporte_COP": 0,
    "aporte_USD": 0,
    "resp": [None] * len(motor.PREGUNTAS),
    "fondo": "Sí",
    "deudas": "No",
    "pref_moneda": "Me da igual",
    "pref_entidad": motor.ENTIDAD_IGUAL,
    "trm": motor.TRM_DEFECTO,
}
if "step" not in st.session_state:
    st.session_state.step = 1
if "d" not in st.session_state:
    st.session_state.d = {k: (list(v) if isinstance(v, list) else v) for k, v in ESTADO_INICIAL.items()}
d = st.session_state.d


def ir(paso: int) -> None:
    st.session_state.step = paso
    st.rerun()


def reiniciar() -> None:
    st.session_state.d = {k: (list(v) if isinstance(v, list) else v) for k, v in ESTADO_INICIAL.items()}
    ir(1)


# ------------------------------------------------------------------ encabezado
def encabezado(compacto: bool = False) -> None:
    if compacto:
        html('<div class="hero compact"><h1>📈 Tu recomendación de inversión</h1></div>')
    else:
        html(
            """
            <div class="hero">
              <h1>📈 Asesor de Inversiones con IA</h1>
              <p>Responde unas preguntas rápidas y descubre dónde invertir según tu perfil, tu moneda y tu plazo.</p>
            </div>
            """
        )


def stepper(actual: int) -> None:
    nombres = ["Tu inversión", "Tu perfil", "Tu situación"]
    partes = []
    for i, n in enumerate(nombres, start=1):
        clase = "on" if i == actual else ("done" if i < actual else "")
        marca = "✓" if i < actual else str(i)
        partes.append(f'<div class="step {clase}"><div class="dot">{marca}</div><span class="t">{n}</span></div>')
    html('<div class="stepper">' + "".join(partes) + "</div>")


def titulo(t: str, sub: str) -> None:
    html(f'<div class="sec-title">{t}</div><div class="sec-sub">{sub}</div>')


# ------------------------------------------------------------------ paso 1
def paso_1() -> None:
    encabezado()
    stepper(1)
    titulo("Cuéntanos sobre tu inversión", "Con esto calculamos montos, plazos y comisiones.")

    primera = st.radio(
        "¿Es tu primera vez invirtiendo?", ["Sí", "No"], index=0 if d["primera"] == "Sí" else 1, horizontal=True, key="w_primera"
    )
    objetivo = st.selectbox(
        "¿Para qué quieres invertir?", motor.OBJETIVOS, index=motor.OBJETIVOS.index(d["objetivo"]), key="w_objetivo"
    )

    moneda_txt = st.radio(
        "¿En qué moneda vas a ingresar tu monto?",
        ["Pesos colombianos (COP)", "Dólares (USD)"],
        index=0 if d["moneda"] == "COP" else 1,
        horizontal=True,
        key="w_moneda",
    )
    moneda = "COP" if moneda_txt.startswith("Pesos") else "USD"

    if moneda == "COP":
        monto = st.number_input(
            "¿Cuánto vas a invertir? (COP)", min_value=100_000, max_value=200_000_000,
            value=int(d["monto_COP"]), step=100_000, key="w_monto_COP",
        )
        aporte = st.number_input(
            "¿Piensas aportar cada mes? (COP, opcional)", min_value=0, max_value=20_000_000,
            value=int(d["aporte_COP"]), step=50_000, key="w_aporte_COP",
        )
    else:
        monto = st.number_input(
            "¿Cuánto vas a invertir? (USD)", min_value=50, max_value=50_000,
            value=int(d["monto_USD"]), step=50, key="w_monto_USD",
        )
        aporte = st.number_input(
            "¿Piensas aportar cada mes? (USD, opcional)", min_value=0, max_value=10_000,
            value=int(d["aporte_USD"]), step=25, key="w_aporte_USD",
        )

    def etiqueta_plazo(m: int) -> str:
        if m < 12:
            return f"{m} mes" if m == 1 else f"{m} meses"
        return f"{m // 12} año" if m == 12 else f"{m // 12} años"

    plazo = st.select_slider(
        "¿A qué plazo?", options=motor.PLAZOS, value=d["plazo"], format_func=etiqueta_plazo, key="w_plazo"
    )

    st.write("")
    if st.button("Continuar →", type="primary", key="b1"):
        d.update(primera=primera, objetivo=objetivo, moneda=moneda, plazo=plazo)
        d[f"monto_{moneda}"] = int(monto)
        d[f"aporte_{moneda}"] = int(aporte)
        ir(2)


# ------------------------------------------------------------------ paso 2
def paso_2() -> None:
    encabezado()
    stepper(2)
    titulo("¿Cómo reaccionas ante el riesgo?", "No hay respuestas buenas o malas: con esto definimos tu perfil de inversionista.")

    respuestas = []
    for i, (pregunta, opciones) in enumerate(motor.PREGUNTAS):
        textos = [o[0] for o in opciones]
        previa = d["resp"][i]
        idx = textos.index(previa) if previa in textos else None
        r = st.radio(pregunta, textos, index=idx, key=f"w_p{i}")
        respuestas.append(r)

    st.write("")
    c1, c2 = st.columns(2)
    if c1.button("← Atrás", key="a2"):
        d["resp"] = respuestas
        ir(1)
    if c2.button("Continuar →", type="primary", key="b2"):
        d["resp"] = respuestas
        if any(r is None for r in respuestas):
            st.warning("Responde todas las preguntas para continuar.")
        else:
            ir(3)


# ------------------------------------------------------------------ paso 3
def paso_3() -> None:
    encabezado()
    stepper(3)
    titulo("Tu situación y preferencias", "Así filtramos las entidades y las monedas que mejor te encajan.")

    fondo = st.radio(
        "¿Tienes un fondo de emergencia (3 meses de gastos o más)?", ["Sí", "No"],
        index=0 if d["fondo"] == "Sí" else 1, horizontal=True, key="w_fondo",
    )
    deudas = st.radio(
        "¿Tienes deudas con intereses altos (tarjeta de crédito, préstamos de consumo)?", ["No", "Sí"],
        index=0 if d["deudas"] == "No" else 1, horizontal=True, key="w_deudas",
    )
    opciones_moneda = ["Pesos", "Dólares", "Me da igual"]
    pref_moneda = st.radio(
        "¿En qué moneda prefieres que esté tu inversión?", opciones_moneda,
        index=opciones_moneda.index(d["pref_moneda"]), horizontal=True, key="w_pref_moneda",
    )
    opciones_entidad = [motor.ENTIDAD_LOCAL, motor.ENTIDAD_INTERNACIONAL, motor.ENTIDAD_IGUAL]
    pref_entidad = st.radio(
        "¿Dónde te sientes más cómodo invirtiendo?", opciones_entidad,
        index=opciones_entidad.index(d["pref_entidad"]), key="w_pref_entidad",
        help="Las entidades vigiladas por la Superfinanciera tienen supervisión del Estado colombiano. Las plataformas internacionales suelen dar más variedad, pero tú asumes más trámites (y declarar ante la DIAN).",
    )

    with st.expander("Ajustes avanzados"):
        trm = st.number_input(
            "Tasa de cambio (pesos por 1 dólar)", min_value=1000.0, max_value=10000.0,
            value=float(d["trm"]), step=10.0, key="w_trm",
            help="Por defecto usamos la TRM aproximada del 10 de noviembre de 2026. Cámbiala si el dólar cambió.",
        )

    st.write("")
    c1, c2 = st.columns(2)
    if c1.button("← Atrás", key="a3"):
        ir(2)
    if c2.button("Ver mi recomendación ✨", type="primary", key="b3"):
        d.update(fondo=fondo, deudas=deudas, pref_moneda=pref_moneda, pref_entidad=pref_entidad, trm=float(trm))
        ir(4)


# ------------------------------------------------------------------ tarjetas
def tarjeta_plataforma(p: dict, mostrar_minimo_alerta: bool = False, compacto: bool = False) -> str:
    origen = (
        '<span class="badge b-co">Colombia</span>' if p["origen"] == "Colombia" else '<span class="badge b-int">Internacional</span>'
    )
    sfc = '<span class="badge b-sfc">Vigilada por la Superfinanciera</span>' if p["vigilada_sfc"] else ""
    alerta = ""
    if mostrar_minimo_alerta and not p.get("alcanza_minimo", True):
        alerta = '<span class="badge b-warn">Tu monto podría no alcanzar el mínimo</span>'
    if compacto:
        reg = "" if p["vigilada_sfc"] else f'<div class="small" style="margin-top:8px"><b>Regulación:</b> {p["regulacion"]}</div>'
        return H(
            f"""
            <div class="plat">
              <div class="plat-head"><span class="plat-name">{p['nombre']}</span>{origen}{sfc}{alerta}</div>
              <div class="plat-grid">
                <div><b>Mínimo:</b> {p['minimo_txt']}</div>
                <div><b>Costos:</b> {p['costos']}</div>
              </div>
              {reg}
              <div class="note">{p['nota']}</div>
              <a class="btn-link" href="{p['url']}" target="_blank" rel="noopener noreferrer">Ir al sitio oficial ↗</a>
            </div>
            """
        )
    return H(
        f"""
        <div class="plat">
          <div class="plat-head"><span class="plat-name">{p['nombre']}</span>{origen}{sfc}{alerta}</div>
          <div class="plat-grid">
            <div><b>Qué ofrece:</b> {p['ofrece']}</div>
            <div><b>Moneda:</b> {p['moneda']}</div>
            <div><b>Mínimo:</b> {p['minimo_txt']}</div>
            <div><b>Costos:</b> {p['costos']}</div>
          </div>
          <div class="small" style="margin-top:8px"><b>Regulación:</b> {p['regulacion']}</div>
          <div class="note">{p['nota']}</div>
          <a class="btn-link" href="{p['url']}" target="_blank" rel="noopener noreferrer">Ir al sitio oficial ↗</a>
        </div>
        """
    )


def tarjeta_opcion(n: int, r: dict, moneda: str) -> str:
    pct = int(round(r["afinidad"] * 100))
    ref = f'<div class="note">{r["referencia_cop"]}</div>' if r["referencia_cop"] else ""
    cambiario = ""
    if r["moneda_activo"] == "USD" and moneda == "COP":
        cambiario = '<div class="small">Este activo está en dólares: si el dólar baja frente al peso, tu ganancia en pesos baja.</div>'
    clase = "card top" if n == 1 else "card"
    mejor = '<span class="badge b-sfc">Mejor opción para ti</span>' if n == 1 else ""
    pos = "pos" if r["ganancia"] >= 0 else ""
    return H(
        f"""
        <div class="{clase}">
          <div class="card-head"><span class="rank">{n}</span><span class="card-title">{r['tipo']}</span>{badge_moneda(r['moneda_activo'])}{mejor}</div>
          <div class="desc">{r['descripcion']}</div>
          <div class="small">Afinidad con tu caso: <b>{pct}%</b></div>
          <div class="bar"><span style="width:{max(pct, 3)}%"></span></div>
          <div class="metrics">
            <div class="metric"><div class="lbl">Rendimiento anual esperado (modelo)</div><div class="val">{motor.fmt_pct(r['rendimiento_anual_pct'])}</div></div>
            <div class="metric"><div class="lbl">Comisión estimada</div><div class="val">{motor.fmt_pct(r['comision_pct'], 2)}</div></div>
            <div class="metric"><div class="lbl">Valor estimado al final</div><div class="val {pos}">{motor.fmt(r['valor_final'], moneda)}</div></div>
          </div>
          <div class="small">Aportarías en total {motor.fmt(r['total_aportado'], moneda)} y ganarías aprox. <b>{motor.fmt(r['ganancia'], moneda)}</b> (ya descontada la comisión).</div>
          {ref}{cambiario}
        </div>
        """
    )


# ------------------------------------------------------------------ resultados
def paso_resultados() -> None:
    encabezado(compacto=True)
    moneda = d["moneda"]
    monto = d[f"monto_{moneda}"]
    aporte = d[f"aporte_{moneda}"]
    puntos = sum(dict(o)[r] for (_, o), r in zip(motor.PREGUNTAS, d["resp"]))
    perfil = motor.perfil_desde_puntos(puntos)

    out = motor.recomendar(
        primera_vez=(d["primera"] == "Sí"),
        monto=monto,
        moneda=moneda,
        trm=d["trm"],
        plazo=d["plazo"],
        perfil=perfil,
        pref_moneda=d["pref_moneda"],
        pref_entidad=d["pref_entidad"],
        aporte_mensual=aporte,
    )

    # Resumen del perfil
    pos_pin = (puntos - motor.PUNTOS_MIN) / (motor.PUNTOS_MAX - motor.PUNTOS_MIN) * 100
    if d["plazo"] < 12:
        plazo_txt = "1 mes" if d["plazo"] == 1 else f"{d['plazo']} meses"
    else:
        plazo_txt = "1 año" if d["plazo"] == 12 else f"{d['plazo'] // 12} años"
    equivalente = (
        f"≈ US${out['monto_usd']:,.0f}" if moneda == "COP" else f"≈ {motor.fmt(monto * d['trm'], 'COP')}"
    )
    html(
        f"""
        <div class="card">
          <div class="small">Tu perfil de inversionista</div>
          <div class="card-title" style="font-size:1.6rem">{perfil}</div>
          <div class="desc">{motor.DESCRIPCION_PERFIL[perfil]}</div>
          <div class="gauge"><div class="pin" style="left:{pos_pin:.0f}%"></div></div>
          <div class="gauge-lbl"><span>Conservador</span><span>Moderado</span><span>Agresivo</span></div>
          <div class="small" style="margin-top:10px">Invertirías {motor.fmt(monto, moneda)} ({equivalente}) durante {plazo_txt}{' y aportarías ' + motor.fmt(aporte, moneda) + ' cada mes' if aporte else ''}.</div>
        </div>
        """
    )

    for nivel, msg in motor.advertencias(
        perfil, d["plazo"], out["monto_usd"], d["objetivo"], d["fondo"] == "Sí", d["deudas"] == "Sí", moneda, d["pref_moneda"]
    ):
        html(f'<div class="alert {nivel}">{msg}</div>')
    if out["monto_ajustado"]:
        html('<div class="alert info">El modelo se entrenó con montos entre US$50 y US$50.000; para tu monto las estimaciones son aproximadas.</div>')
    if out["omitidos"]:
        html(
            '<div class="alert info">Dejamos fuera: <b>' + ", ".join(out["omitidos"]) +
            "</b>, porque ninguna plataforma de ese tipo es una entidad colombiana vigilada por la Superfinanciera.</div>"
        )

    tab1, tab2 = st.tabs(["⭐ Mis recomendaciones", "🏦 Todas las entidades"])

    with tab1:
        for n, r in enumerate(out["resultados"], start=1):
            html(tarjeta_opcion(n, r, moneda))
            st.markdown(f"**¿Dónde hacerlo?** Entidades sugeridas para *{r['tipo']}*:")
            for p in r["plataformas"]:
                st.markdown(tarjeta_plataforma(p, mostrar_minimo_alerta=True, compacto=True), unsafe_allow_html=True)
            with st.expander("📈 Ver proyección mes a mes"):
                st.line_chart(r["serie"])
                st.caption("Proyección educativa con el rendimiento que estima el modelo; no es una promesa de resultados.")
            st.write("")

        with st.expander("¿Cómo se calculó esto?"):
            m = motor.BUNDLE["metricas"]
            st.markdown(
                f"""
- Tu **perfil** sale del cuestionario ({puntos} de {motor.PUNTOS_MAX} puntos), no se adivina con el monto.
- Un modelo de IA (Gradient Boosting) ordena los activos posibles para tu perfil. La opción correcta queda entre las **2 primeras** el **{m['tipo_top2']:.0%}** de las veces y entre las **3 primeras** el **{m['tipo_top3']:.0%}**.
- Otro modelo estima rendimiento y comisión (R² de {m['rend_r2']:.2f} y {m['com_r2']:.2f}; error promedio de {m['rend_mae']:.1f} puntos en rendimiento).
- Tu preferencia de moneda y de entidades reordena o filtra las opciones con reglas, no con el modelo.
- Valor final = monto × (1 + rendimiento)^(años) + aportes con interés − comisión.
- El dataset de entrenamiento es sintético (500 registros), por eso los rendimientos del modelo son de referencia. En pesos, las tasas reales de CDT y fondos pueden ser distintas: revisa la tasa vigente.
"""
            )

    with tab2:
        st.markdown("Entidades donde puedes invertir desde Colombia, con datos aproximados a " + ACTUALIZADO + ".")
        filtro = st.radio("Mostrar", ["Todas", "Colombianas", "Internacionales"], horizontal=True, key="w_filtro")
        for p in PLATAFORMAS:
            if filtro == "Colombianas" and p["origen"] != "Colombia":
                continue
            if filtro == "Internacionales" and p["origen"] == "Colombia":
                continue
            st.markdown(tarjeta_plataforma(p), unsafe_allow_html=True)

    st.write("")
    c1, c2 = st.columns(2)
    if c1.button("← Cambiar mis respuestas", key="r1"):
        ir(1)
    if c2.button("Empezar de nuevo", key="r2"):
        reiniciar()


# ------------------------------------------------------------------ enrutador
paso = st.session_state.step
if paso == 1:
    paso_1()
elif paso == 2:
    paso_2()
elif paso == 3:
    paso_3()
else:
    paso_resultados()

html(
    f"""
    <div class="disclaimer">
      Herramienta educativa de un proyecto académico de Inteligencia Artificial. Los datos de entrenamiento son sintéticos y la información de entidades es aproximada ({ACTUALIZADO}):
      verifica siempre costos, mínimos y tasas en el sitio oficial. Esto no constituye asesoría financiera; consulta a un profesional antes de invertir.
    </div>
    """
)
