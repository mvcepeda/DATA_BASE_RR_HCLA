import streamlit as st
import pandas as pd
import altair as alt
import html

# ---------------------------------------------------
# Configuración general
# ---------------------------------------------------
st.set_page_config(
    page_title="Repositorio de Tesis | HCLA",
    layout="wide",
)

# ---------------------------------------------------
# Estilos visuales
# ---------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #f7f7f8;
        color: #1f2937;
    }

    .main .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
        max-width: 1180px;
    }

    .hero-box {
        background: linear-gradient(135deg, #8e1b2f, #b22222);
        padding: 1.6rem 1.8rem;
        border-radius: 18px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 18px rgba(0,0,0,0.08);
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
        line-height: 1.2;
    }

    .hero-subtitle {
        font-size: 1rem;
        opacity: 0.96;
    }

    .sidebar-box {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1rem 1rem 0.8rem 1rem;
        margin-bottom: 1rem;
    }

    .sidebar-title {
        font-size: 1.08rem;
        font-weight: 700;
        color: #8e1b2f;
        margin-bottom: 0.35rem;
    }

    .sidebar-text {
        font-size: 0.92rem;
        color: #4b5563;
        line-height: 1.45;
    }

    .metric-box {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1rem 1.1rem;
        box-shadow: 0 3px 10px rgba(0,0,0,0.04);
        margin-bottom: 0.75rem;
    }

    .metric-label {
        font-size: 0.92rem;
        color: #6b7280;
        margin-bottom: 0.35rem;
        font-weight: 600;
    }

    .metric-value {
        font-size: 2.05rem;
        font-weight: 700;
        color: #8e1b2f;
        line-height: 1.1;
    }

    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #8e1b2f;
        margin-top: 1rem;
        margin-bottom: 0.35rem;
    }

    .section-note {
        color: #4b5563;
        font-size: 0.95rem;
        margin-bottom: 1rem;
    }

    .thesis-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-left: 6px solid #8e1b2f;
        border-radius: 14px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.9rem;
        box-shadow: 0 3px 10px rgba(0,0,0,0.04);
    }

    .thesis-title {
        font-size: 1.08rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0.65rem;
        line-height: 1.35;
    }

    .thesis-meta {
        font-size: 0.95rem;
        color: #374151;
        margin-bottom: 0.25rem;
        line-height: 1.45;
    }

    .thesis-meta strong {
        color: #8e1b2f;
    }

    .thesis-email a {
        color: #8e1b2f;
        text-decoration: none;
        font-weight: 600;
    }

    .thesis-email a:hover {
        text-decoration: underline;
    }

    .empty-box {
        background: #ffffff;
        border: 1px dashed #d1d5db;
        border-radius: 14px;
        padding: 1rem;
        color: #4b5563;
    }

    section[data-testid="stSidebar"] {
        background-color: #f3f4f6;
        border-right: 1px solid #e5e7eb;
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p {
        color: #1f2937 !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] > div,
    section[data-testid="stSidebar"] [data-baseweb="input"] > div {
        background-color: #ffffff !important;
        border-radius: 10px !important;
        border-color: #d1d5db !important;
    }

    section[data-testid="stSidebar"] input {
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
        caret-color: #8e1b2f !important;
        font-weight: 500 !important;
    }

    section[data-testid="stSidebar"] input::placeholder {
        color: #9ca3af !important;
        -webkit-text-fill-color: #9ca3af !important;
        opacity: 1 !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] span {
        color: #111827 !important;
    }

    section[data-testid="stSidebar"] svg {
        fill: #6b7280 !important;
    }

    footer {
        visibility: visible;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Carga de datos
# ---------------------------------------------------
@st.cache_data
def cargar_datos():
    SHEET_ID = "1DAValP0aAxzk2AxVShNe2uy4yacWX6vBTk0X6w13eKU"
    csv_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    df = pd.read_csv(csv_url)
    df.columns = [c.strip() for c in df.columns]
    return df

df = cargar_datos()

# ---------------------------------------------------
# Función para detectar columnas equivalentes
# ---------------------------------------------------
def encontrar_columna(df, opciones):
    columnas = {c.lower().strip(): c for c in df.columns}
    for op in opciones:
        if op.lower() in columnas:
            return columnas[op.lower()]
    return None

col_anio = encontrar_columna(df, ["Año", "Ano", "Year"])
col_autor = encontrar_columna(df, ["Autor", "Autores", "Author"])
col_titulo = encontrar_columna(df, ["Título", "Titulo", "Title"])
col_correo = encontrar_columna(df, ["Correo", "Correo electrónico", "Email", "E-mail", "Mail"])
col_programa = encontrar_columna(df, ["Programa", "Program"])
col_tema = encontrar_columna(df, ["Tema", "Temas", "Keywords", "Palabras clave"])
col_resumen = encontrar_columna(df, ["Resumen", "Abstract", "Descripción", "Descripcion"])

if col_anio:
    df[col_anio] = pd.to_numeric(df[col_anio], errors="coerce")

# ---------------------------------------------------
# Encabezado principal
# ---------------------------------------------------
st.markdown("""
<div class="hero-box">
    <div class="hero-title">Repositorio de tesis del M.Sc. Governance of Risk and Resources - HCLA</div>
    <div class="hero-subtitle">
        Primera versión de consulta para revisar tesis del programa y facilitar el contacto con sus autoras y autores.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------
st.sidebar.markdown("""
<div class="sidebar-box">
    <div class="sidebar-title">Consulta del repositorio</div>
    <div class="sidebar-text">
        Usa estos filtros para buscar tesis por año, autor o palabras del título.
    </div>
</div>
""", unsafe_allow_html=True)

df_filtrado = df.copy()

if col_anio:
    años = sorted([int(a) for a in df[col_anio].dropna().unique().tolist()])
    opciones_anio = ["Todos"] + [str(a) for a in años]
    anio_sel = st.sidebar.selectbox("Filtrar por año", opciones_anio)
else:
    anio_sel = "Todos"

if col_autor:
    autores = sorted(df[col_autor].dropna().astype(str).unique().tolist())
    autores_sel = st.sidebar.multiselect("Filtrar por autor", autores)
else:
    autores_sel = []

texto_busqueda = st.sidebar.text_input(
    "Buscar por título",
    placeholder="Escribe una palabra clave"
)

# ---------------------------------------------------
# Aplicar filtros
# ---------------------------------------------------
if col_anio and anio_sel != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado[col_anio].astype("Int64").astype(str) == anio_sel
    ]

if col_autor and autores_sel:
    df_filtrado = df_filtrado[
        df_filtrado[col_autor].astype(str).isin(autores_sel)
    ]

if texto_busqueda and col_titulo:
    df_filtrado = df_filtrado[
        df_filtrado[col_titulo].astype(str).str.contains(texto_busqueda, case=False, na=False)
    ]

# ---------------------------------------------------
# Ordenar resultados
# ---------------------------------------------------
columnas_sort = []
ascending_sort = []

if col_anio:
    columnas_sort.append(col_anio)
    ascending_sort.append(False)

if col_titulo:
    columnas_sort.append(col_titulo)
    ascending_sort.append(True)

if columnas_sort:
    df_filtrado = df_filtrado.sort_values(columnas_sort, ascending=ascending_sort, na_position="last")

# ---------------------------------------------------
# Métricas superiores
# ---------------------------------------------------
total_registros = len(df_filtrado)
total_autores = df_filtrado[col_autor].nunique() if col_autor and not df_filtrado.empty else 0

if col_anio and not df_filtrado.empty and not df_filtrado[col_anio].dropna().empty:
    rango_anios = f"{int(df_filtrado[col_anio].min())} - {int(df_filtrado[col_anio].max())}"
else:
    rango_anios = "Sin datos"

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Tesis visibles</div>
        <div class="metric-value">{total_registros}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Autores visibles</div>
        <div class="metric-value">{total_autores}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Rango de años</div>
        <div class="metric-value">{html.escape(str(rango_anios))}</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# Resultados
# ---------------------------------------------------
st.markdown('<div class="section-title">Tesis disponibles</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="section-note">Se encontraron <strong>{len(df_filtrado)}</strong> registros según los filtros seleccionados.</div>',
    unsafe_allow_html=True
)

if df_filtrado.empty:
    st.markdown("""
    <div class="empty-box">
        No se encontraron tesis con los filtros actuales. Prueba con otro año, otro autor o una búsqueda más general.
    </div>
    """, unsafe_allow_html=True)
else:
    for _, fila in df_filtrado.iterrows():
        titulo = html.escape(str(fila[col_titulo])) if col_titulo and pd.notna(fila[col_titulo]) else "Título no disponible"
        autor = html.escape(str(fila[col_autor])) if col_autor and pd.notna(fila[col_autor]) else "Autor no disponible"

        if col_anio and pd.notna(fila[col_anio]):
            anio = str(int(fila[col_anio]))
        else:
            anio = "No disponible"

        correo_raw = ""
        if col_correo and pd.notna(fila[col_correo]):
            correo_raw = str(fila[col_correo]).strip()

        correo_html = "No disponible"
        if correo_raw and correo_raw.lower() != "nan":
            correo_seguro = html.escape(correo_raw)
            correo_html = f'<a href="mailto:{correo_seguro}">{correo_seguro}</a>'

        resumen_html = ""
        if col_resumen and pd.notna(fila[col_resumen]):
            resumen = str(fila[col_resumen]).strip()
            if resumen and resumen.lower() != "nan":
                resumen_html = f'''
                <div class="thesis-meta" style="margin-top:0.55rem;">
                    <strong>Resumen:</strong> {html.escape(resumen)}
                </div>
                '''

        programa_html = ""
        if col_programa and pd.notna(fila[col_programa]):
            programa = str(fila[col_programa]).strip()
            if programa and programa.lower() != "nan":
                programa_html = f'''
                <div class="thesis-meta"><strong>Programa:</strong> {html.escape(programa)}</div>
                '''

        tema_html = ""
        if col_tema and pd.notna(fila[col_tema]):
            tema = str(fila[col_tema]).strip()
            if tema and tema.lower() != "nan":
                tema_html = f'''
                <div class="thesis-meta"><strong>Tema:</strong> {html.escape(tema)}</div>
                '''

        st.markdown(f"""
        <div class="thesis-card">
            <div class="thesis-title">{titulo}</div>
            <div class="thesis-meta"><strong>Autor/a:</strong> {autor}</div>
            <div class="thesis-meta"><strong>Año:</strong> {anio}</div>
            <div class="thesis-meta thesis-email"><strong>Correo de contacto:</strong> {correo_html}</div>
            {programa_html}
            {tema_html}
            {resumen_html}
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------
# Resumen visual
# ---------------------------------------------------
st.markdown('<div class="section-title">Resumen del repositorio</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-note">Vista general del número de tesis registradas por año.</div>',
    unsafe_allow_html=True
)

if not df_filtrado.empty and col_anio and col_titulo:
    conteo = (
        df_filtrado.groupby(col_anio)[col_titulo]
        .count()
        .reset_index(name="Cantidad")
        .sort_values(col_anio)
    )

    grafico = (
        alt.Chart(conteo)
        .mark_bar(color="#b22222", cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X(
                f"{col_anio}:O",
                title="Año",
                axis=alt.Axis(labelAngle=0, labelColor="#374151", titleColor="#374151")
            ),
            y=alt.Y(
                "Cantidad:Q",
                title="Número de tesis",
                axis=alt.Axis(labelColor="#374151", titleColor="#374151", gridColor="#e5e7eb")
            ),
            tooltip=[
                alt.Tooltip(f"{col_anio}:O", title="Año"),
                alt.Tooltip("Cantidad:Q", title="Cantidad")
            ]
        )
        .properties(
            height=340,
            background="white"
        )
        .configure_view(
            stroke=None,
            fill="white"
        )
        .configure_axis(
            domainColor="#d1d5db",
            tickColor="#d1d5db"
        )
    )

    st.altair_chart(grafico, use_container_width=True, theme=None)
else:
    st.info("No hay datos suficientes para generar el resumen visual.")

# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.markdown("---")
st.caption("Repositorio académico HCLA | versión inicial de consulta")
