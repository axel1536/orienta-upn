from pathlib import Path
import sys

import streamlit as st

CARPETA = Path(__file__).resolve().parents[1]
if str(CARPETA) not in sys.path:
    sys.path.insert(0, str(CARPETA))

from agente import TEMAS
from retroalimentacion import confirmadas_csv, listar_registros, revisar_registro


st.set_page_config(page_title="Revisar consultas", layout="centered")
st.title("Revisar consultas")
st.write("Confirma, corrige o descarta cada ejemplo antes de usarlo para entrenar.")

pendientes = list(reversed(listar_registros("pendiente")))
confirmadas = listar_registros("confirmada")
st.metric("Pendientes", len(pendientes))

if confirmadas:
    st.download_button(
        "Descargar consultas confirmadas",
        data=confirmadas_csv().encode("utf-8-sig"),
        file_name="consultas_confirmadas.csv",
        mime="text/csv",
        width="stretch",
    )

if not pendientes:
    st.info("No hay consultas pendientes de revisión.")

for registro in pendientes:
    titulo = registro["consulta"][:80]
    with st.expander(titulo):
        st.markdown("**Pregunta**")
        st.write(registro["consulta"])
        st.markdown("**Respuesta mostrada**")
        st.write(registro["respuesta"])
        predicha = registro.get("intencion_predicha")
        st.caption(f"Predicción: {TEMAS.get(predicha, predicha)}")
        if registro.get("confianza") is not None:
            st.caption(f"Confianza del modelo: {registro['confianza']:.1%}")

        claves = list(TEMAS)
        indice = claves.index(predicha) if predicha in claves else 0
        correcta = st.selectbox(
            "Intención correcta",
            claves,
            index=indice,
            format_func=lambda clave: TEMAS[clave],
            key="tema_" + registro["id"],
        )
        col_confirmar, col_descartar = st.columns(2)
        if col_confirmar.button(
            "Confirmar", key="confirmar_" + registro["id"], width="stretch"
        ):
            revisar_registro(registro["id"], "confirmada", correcta)
            st.rerun()
        if col_descartar.button(
            "Descartar", key="descartar_" + registro["id"], width="stretch"
        ):
            revisar_registro(registro["id"], "descartada")
            st.rerun()
