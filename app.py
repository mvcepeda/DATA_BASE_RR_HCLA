import streamlit as st
import pandas as pd
import altair as alt

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
    .main {
        background-color: #f8fafc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .hero-box {
        background: linear-gradient(135deg, #0f172a, #1e3a8a);
        padding: 1.8rem 2rem;
        border-radius: 18px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .hero-subtitle {
        font-size: 1rem;
        opacity: 0.92;
    }

    .metric-card {
        background: white;
        padding: 1rem 1.2rem;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    }

    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        margin-top: 1rem;
        margin-bottom: 0.7rem;
        color: #0f172a;
    }

    .small-note {
        color: #475569;
        font-size: 0.92rem;
    }

    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e7eb;
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

    # limpiar nombres de columnas
    df.columns = [c.strip() for c in df.columns]

    return df

df = cargar_datos()

# ---------------------------------------------------
# Función auxiliar para encontrar columnas posibles
# ---------------------------------------------------
def encontrar_columna(df, opciones):
    columnas = {c.lower().strip(): c for c in df.columns}
    for op in opciones:
        if op.lower() in columnas:
            return columnas[op.lower()]
    return None

col_anio = encontrar_columna(df, ["Año", "Ano", "Year"])
col_autor = encontrar_columna(df, ["Autor", "Author", "Autores"])
col_titulo = encontrar_columna(df, ["Título", "Titulo", "Title"])
col_programa = encontrar_columna(df, ["Programa", "Program"])
col_tema = encontrar_columna(df, ["Tema", "Keywords", "Palabras clave"])
col_link = encontrar_columna(df, ["Link", "URL", "Enlace", "Archivo", "PDF"])

# Convertir año si existe
if col_anio:
    df[col_anio] = pd.to_numeric(df[col_anio], errors="coerce")

# ---------------------------------------------------
# Encabezado
# ---------------------------------------------------
st.markdown("""
<div class="hero-box">
    <div class="hero-title">Repositorio de tesis del M.Sc. Governance of Risk and Resources - HCLA</div>
    <div class="hero-subtitle">
        Explorador de trabajos académicos con filtros dinámicos, búsqueda y visualización resumida.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Sidebar: filtros
# ---------------------------------------------------
st.sidebar.markdown("## Filtros")

df_filtrado = df.copy()

# Año
if col_anio:
    años = sorted([int(a) for a in df[col_anio].dropna().unique().tolist()])
    opciones_anio = ["Todos"] + [str(a) for a in años]
    anio_sel = st.sidebar.selectbox("Filtrar por año", opciones_anio)
else:
    anio_sel = "Todos"

# Autor
if col_autor:
    autores = sorted(df[col_autor].dropna().astype(str).unique().tolist())
    autores_sel = st.sidebar.multiselect("Filtrar por autor", autores)
else:
    autores_sel = []

# Texto de búsqueda
texto_busqueda = st.sidebar.text_input("Buscar por título o texto", placeholder="Escribe una palabra clave")

# Programa
if col_programa:
    programas = sorted(df[col_programa].dropna().astype(str).unique().tolist())
    programa_sel = st.sidebar.multiselect("Filtrar por programa", programas)
else:
    programa_sel = []

# Tema
if col_tema:
    temas = sorted(df[col_tema].dropna().astype(str).unique().tolist())
    tema_sel = st.sidebar.multiselect("Filtrar por tema", temas)
else:
    tema_sel = []

# ---------------------------------------------------
# Aplicar filtros
# ---------------------------------------------------
if col_anio and anio_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado[col_anio].astype("Int64").astype(str) == anio_sel]

if col_autor and autores_sel:
    df_filtrado = df_filtrado[df_filtrado[col_autor].astype(str).isin(autores_sel)]

if col_programa and programa_sel:
    df_filtrado = df_filtrado[df_filtrado[col_programa].astype(str).isin(programa_sel)]

if col_tema and tema_sel:
    df_filtrado = df_filtrado[df_filtrado[col_tema].astype(str).isin(tema_sel)]

if texto_busqueda:
    columnas_busqueda = [c for c in [col_titulo, col_autor, col_tema, col_programa] if c]
    if columnas_busqueda:
        mascara = df_filtrado[columnas_busqueda].fillna("").astype(str).agg(" ".join, axis=1)
        df_filtrado = df_filtrado[mascara.str.contains(texto_busqueda, case=False, na=False)]

# ---------------------------------------------------
# Métricas
# ---------------------------------------------------
total_registros = len(df_filtrado)
total_autores = df_filtrado[col_autor].nunique() if col_autor and not df_filtrado.empty else 0
rango_anios = (
    f"{int(df_filtrado[col_anio].min())} - {int(df_filtrado[col_anio].max())}"
    if col_anio and not df_filtrado[col_anio].dropna().empty
    else "Sin datos"
)

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Registros encontrados", total_registros)
    st.markdown('</div>', unsafe_allow_html=True)

with m2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Autores visibles", total_autores)
    st.markdown('</div>', unsafe_allow_html=True)

with m3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Rango de años", rango_anios)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("")

# ---------------------------------------------------
# Tabs
# ---------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📄 Resultados", "📊 Estadísticas", "🗂 Base completa"])

# ---------------------------------------------------
# TAB 1: Resultados
# ---------------------------------------------------
with tab1:
    st.markdown('<div class="section-title">Resultados filtrados</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="small-note">Se encontraron <b>{len(df_filtrado)}</b> registros según los filtros seleccionados.</div>',
        unsafe_allow_html=True
    )

    st.markdown("")

    if not df_filtrado.empty:
        # Preparar tabla
        columnas_mostrar = [c for c in [col_titulo, col_autor, col_anio, col_programa, col_tema, col_link] if c]
        if not columnas_mostrar:
            columnas_mostrar = df_filtrado.columns.tolist()

        df_mostrar = df_filtrado[columnas_mostrar].copy()

        # Descargar CSV
        csv_descarga = df_filtrado.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇ Descargar resultados en CSV",
            data=csv_descarga,
            file_name="repositorio_filtrado_hcla.csv",
            mime="text/csv",
        )

        if col_link and col_link in df_mostrar.columns:
            st.dataframe(
                df_mostrar,
                use_container_width=True,
                column_config={
                    col_link: st.column_config.LinkColumn("Enlace")
                }
            )
        else:
            st.dataframe(df_mostrar, use_container_width=True)

    else:
        st.info("No hay resultados con los filtros actuales.")

# ---------------------------------------------------
# TAB 2: Estadísticas
# ---------------------------------------------------
with tab2:
    st.markdown('<div class="section-title">Visualización general</div>', unsafe_allow_html=True)

    if not df_filtrado.empty and col_anio and col_titulo:
        conteo = (
            df_filtrado.groupby(col_anio)[col_titulo]
            .count()
            .reset_index(name="Cantidad")
            .sort_values(col_anio)
        )

        grafico = (
            alt.Chart(conteo)
            .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
            .encode(
                x=alt.X(f"{col_anio}:O", title="Año"),
                y=alt.Y("Cantidad:Q", title="Número de títulos"),
                tooltip=[col_anio, "Cantidad"]
            )
            .properties(height=420)
            .interactive()
        )

        st.altair_chart(grafico, use_container_width=True)
    else:
        st.info("No hay datos suficientes para graficar.")

    if not df_filtrado.empty and col_autor:
        st.markdown('<div class="section-title">Autores más frecuentes</div>', unsafe_allow_html=True)
        top_autores = (
            df_filtrado[col_autor]
            .value_counts()
            .reset_index()
        )
        top_autores.columns = ["Autor", "Cantidad"]
        st.dataframe(top_autores.head(10), use_container_width=True)

# ---------------------------------------------------
# TAB 3: Base completa
# ---------------------------------------------------
with tab3:
    st.markdown('<div class="section-title">Vista general de la base</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="small-note">Esta tabla muestra la base original cargada desde Google Sheets.</div>',
        unsafe_allow_html=True
    )
    st.dataframe(df, use_container_width=True)

# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.markdown("---")
st.caption("Repositorio académico HCLA | versión mejorada en Streamlit")
