import streamlit as st
import pandas as pd
import base64
import os

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Trazabilidad Barriles Castiza", layout="centered")

# AÑADIR IMAGEN DE FONDO PERSONALIZADA Y ESTILOS GENERALES
if os.path.exists("background.jpg"):
    with open("background.jpg", "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');
        html, body, [class*="st"]  {{
            font-family: 'Roboto', sans-serif;
            color: #fff3aa;
        }}
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stTextInput > div > div > input,
        .stSelectbox > div > div,
        .stTextArea > div > textarea {{
            background-color: #ffffff10 !important;
            color: #fff3aa !important;
            border-radius: 10px;
        }}
        .stButton > button {{
            background-color: #55dcad !important;
            color: #fff3aa !important;
            border: none;
            border-radius: 10px;
            font-weight: bold;
        }}
        .stDataFrame, .stTable {{
            background-color: rgba(0,0,0,0.6);
            border-radius: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# TITULO PRINCIPAL
st.markdown("""
    <h1 style='text-align:center; color:#fff3aa;'>🍺 Sistema de Trazabilidad de Barriles - Castiza</h1>
""", unsafe_allow_html=True)

# ------------------------------
# FORMULARIO DE REGISTRO DE BARRILES
# ------------------------------
st.markdown("""<h2 style='color:#fff3aa;'>📋 Registro Movimiento Barriles</h2>""", unsafe_allow_html=True)

codigo_barril = st.number_input("Código del barril (Debe tener 5 dígitos y empezar por 20, 30 o 58)", format="%05d", step=1)
codigo_barril = str(int(codigo_barril)).zfill(5) if codigo_barril else ""

codigo_valido = False
if codigo_barril and len(codigo_barril) == 5 and codigo_barril[:2] in ["20", "30", "58"]:
    codigo_valido = True

estilos = ["Golden", "Amber", "Vienna Lager", "Brown Ale Cafe", "Stout",
           "Session IPA", "IPA", "Maracuya", "Barley Wine", "Trigo", "Catharina Sour",
           "Gose", "Imperial IPA", "NEIPA", "Imperial Stout", "Otros"]
estilo_cerveza = st.selectbox("Estilo", estilos)

estado_barril = st.selectbox("Estado del barril", ["Despachado", "Lavado en bodega", "Sucio", "En cuarto frío"])

try:
    df_clientes = pd.read_csv("clientes.csv")
    lista_clientes = df_clientes.iloc[:, 0].dropna().astype(str).tolist()
except:
    lista_clientes = []

cliente = "Planta Castiza"
if estado_barril == "Despachado":
    cliente = st.selectbox("Cliente", lista_clientes)

responsables = ["Pepe Vallejo", "Ligia Cajigas", "Erika Martinez", "Marcelo Martinez", "Operario 1", "Operario 2"]
responsable = st.selectbox("Responsable", responsables)

observaciones = st.text_area("Observaciones")

if st.button("Guardar Registro"):
    if codigo_valido:
        st.success("✅ Registro procesado correctamente (almacenamiento desactivado en esta versión)")
    else:
        st.warning("⚠️ Código de barril inválido. Debe tener 5 dígitos y comenzar por 20, 30 o 58.")

# Registrar cliente
st.markdown("---")
st.markdown("""<h2 style='color:#fff3aa;'>➕ Registrar Nuevo Cliente</h2>""", unsafe_allow_html=True)
nuevo_cliente = st.text_input("Nombre del nuevo cliente")
direccion_cliente = st.text_input("Dirección (opcional)")

if st.button("Agregar Cliente"):
    if nuevo_cliente.strip() != "":
        try:
            df_nuevo = pd.DataFrame([[nuevo_cliente, direccion_cliente]])
            if lista_clientes:
                df_clientes = pd.concat([df_clientes, df_nuevo], ignore_index=True)
            else:
                df_clientes = df_nuevo
            df_clientes.drop_duplicates(subset=0, keep="first", inplace=True)
            df_clientes.to_csv("clientes.csv", index=False, header=False)
            st.success("✅ Cliente agregado correctamente")
        except:
            st.error("❌ Error al guardar el nuevo cliente")
    else:
        st.warning("⚠️ El nombre del cliente no puede estar vacío")

# Eliminar cliente
st.markdown("---")
st.markdown("""<h2 style='color:#fff3aa;'>🗑️ Eliminar Cliente</h2>""", unsafe_allow_html=True)
if lista_clientes:
    cliente_eliminar = st.selectbox("Selecciona cliente a eliminar", lista_clientes)
    if st.button("Eliminar Cliente"):
        try:
            df_clientes = df_clientes[df_clientes.iloc[:, 0] != cliente_eliminar]
            df_clientes.to_csv("clientes.csv", index=False, header=False)
            st.success("✅ Cliente eliminado correctamente")
        except:
            st.error("❌ Error al eliminar el cliente")
