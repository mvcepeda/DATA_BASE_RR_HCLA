import streamlit as st
import pandas as pd

st.set_page_config(page_title="Repositorio de Publicaciones", layout="wide")

@st.cache_data
def cargar_datos():
    SHEET_ID = "1DAValP0aAxzk2AxVShNe2uy4yacWX6vBTk0X6w13eKU"
    csv_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    df = pd.read_csv(csv_url)
    df.columns = [c.strip() for c in df.columns]
    if "Año" in df.columns:
        df["Año"] = pd.to_numeric(df["Año"], errors="coerce")
    return df

df = cargar_datos()

st.title("📚 Repositorio de autores y publicaciones")
st.write("Datos obtenidos automáticamente desde Google Sheets ✨")

st.subheader("Vista general de los datos")
st.dataframe(df, use_container_width=True)

st.sidebar.header("Filtros")

# Año
if "Año" in df.columns:
    años = sorted(df["Año"].dropna().unique().tolist())
    años_opciones = ["(Todos)"] + [str(a) for a in años]
    año_sel = st.sidebar.selectbox("Filtrar por Año", años_opciones)
else:
    año_sel = "(Todos)"

# Autor
autores = sorted(df["Autor"].dropna().unique().tolist())
autores_sel = st.sidebar.multiselect("Filtrar por Autor", autores)

# Texto en título
texto_titulo = st.sidebar.text_input("Buscar en Título")

df_filtrado = df.copy()

if año_sel != "(Todos)":
    df_filtrado = df_filtrado[df_filtrado["Año"].astype("Int64").astype(str) == año_sel]

if autores_sel:
    df_filtrado = df_filtrado[df_filtrado["Autor"].isin(autores_sel)]

if texto_titulo:
    df_filtrado = df_filtrado[
        df_filtrado["Título"].str.contains(texto_titulo, case=False, na=False)
    ]

st.subheader("Resultados filtrados")
st.write(f"Total de registros: **{len(df_filtrado)}**")
st.dataframe(df_filtrado, use_container_width=True)

st.subheader("Número de títulos por año")
if not df_filtrado.empty:
    conteo = (
        df_filtrado.groupby("Año")["Título"]
        .count()
        .reset_index(name="Cantidad")
        .sort_values("Año")
    )
    st.bar_chart(conteo.set_index("Año")["Cantidad"])
else:
    st.info("No hay datos para graficar con los filtros actuales.")

