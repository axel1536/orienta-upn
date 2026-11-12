import re
import time

import streamlit as st

st.set_page_config(page_title="Orienta UPN", layout="centered")

try:
    from dialogo import conversar, crear_conversacion
    from retroalimentacion import guardar_pendiente
except (ImportError, FileNotFoundError, ValueError, KeyError) as error:
    st.error("No se pudieron cargar los archivos del proyecto.")
    st.text(str(error))
    st.stop()

CLAVE_SESION = "orienta_v3"
CLAVE_CONVERSACION = "orienta_conversacion"
CLAVE_ANIMACION = "orienta_animacion"


def escribir_progresivamente(texto):
    for fragmento in re.split(r"(\s+)", texto):
        if fragmento:
            yield fragmento
            if fragmento.strip():
                time.sleep(0.012)


def registrar(texto, accion=None):
    with st.spinner("OrientaUPN está revisando tu consulta..."):
        nueva_sesion = conversar(st.session_state[CLAVE_SESION], texto, accion)
    st.session_state[CLAVE_SESION] = nueva_sesion
    st.session_state[CLAVE_ANIMACION] = len(nueva_sesion["historial"])


if CLAVE_SESION not in st.session_state:
    st.session_state[CLAVE_SESION] = crear_conversacion()
if CLAVE_CONVERSACION not in st.session_state:
    st.session_state[CLAVE_CONVERSACION] = 1

with st.sidebar:
    st.header("Tu orientación")
    if st.button("Nueva conversación", key="reiniciar_v3"):
        st.session_state[CLAVE_SESION] = crear_conversacion()
        st.session_state[CLAVE_CONVERSACION] += 1
        st.session_state.pop(CLAVE_ANIMACION, None)
        st.rerun()

st.title("Orienta UPN")
st.write("Orientación académica, paso a paso")

sesion = st.session_state[CLAVE_SESION]
if not sesion["historial"]:
    st.info("Escribe tu primera consulta para comenzar.")

mensaje_animado = st.session_state.get(CLAVE_ANIMACION)
for posicion, mensaje in enumerate(sesion["historial"], 1):
    with st.chat_message(mensaje["role"]):
        if mensaje["role"] == "user":
            st.write(mensaje["texto"])
            continue
        resultado = mensaje["resultado"]
        if resultado.get("tema"):
            st.caption(resultado["tema"])
        if posicion == mensaje_animado:
            st.write_stream(escribir_progresivamente(resultado["respuesta"]))
        else:
            st.write(resultado["respuesta"])
        if resultado.get("fuente"):
            st.markdown(f"[Consultar fuente de UPN]({resultado['fuente']})")

if mensaje_animado:
    st.session_state.pop(CLAVE_ANIMACION, None)

if sesion["historial"]:
    ultimo = sesion["historial"][-1]["resultado"]
    intencion = ultimo.get("intencion")
    consulta = sesion.get("consulta_actual")
    if intencion and consulta:
        id_respuesta = f"{st.session_state[CLAVE_CONVERSACION]}_{len(sesion['historial'])}"
        clave_guardada = "consulta_guardada_" + id_respuesta
        if not st.session_state.get(clave_guardada):
            try:
                guardar_pendiente(
                    consulta, ultimo["respuesta"], intencion,
                    ultimo.get("confianza"), ultimo.get("origen", "dialogo")
                )
                st.session_state[clave_guardada] = True
            except Exception:
                st.warning("La respuesta funcionó, pero no se pudo guardar para revisión.")

opciones = sesion["historial"][-1]["resultado"].get("opciones", []) if sesion["historial"] else []
if opciones:
    if len(opciones) > 1:
        st.caption("Puedes elegir una opción o escribir tu respuesta.")
    columnas = st.columns(min(2, len(opciones)))
    for numero, opcion in enumerate(opciones, 1):
        with columnas[(numero - 1) % len(columnas)]:
            etiqueta = f"{numero}. {opcion['texto']}" if len(opciones) > 1 else opcion["texto"]
            if st.button(etiqueta, key=f"v3_{len(sesion['historial'])}_{numero}", width="stretch"):
                registrar(opcion["texto"], opcion["accion"])
                st.rerun()

pregunta = st.chat_input("Escribe tu consulta o el número de una opción", max_chars=1500)
if pregunta and pregunta.strip():
    registrar(pregunta)
    st.rerun()
