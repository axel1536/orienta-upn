from datetime import datetime
from io import StringIO
import csv
import json
from pathlib import Path
from threading import Lock
from uuid import uuid4

import pandas as pd


ARCHIVO = Path(__file__).resolve().parent / "datos" / "consultas_por_revisar.json"
HOJA = "consultas"
COLUMNAS = [
    "id", "fecha", "consulta", "respuesta", "intencion_predicha",
    "confianza", "origen", "estado", "intencion_confirmada",
    "fecha_revision",
]
_BLOQUEO = Lock()


def _conexion_remota():
    try:
        import streamlit as st
        conexiones = st.secrets.get("connections", {})
        if "gsheets" not in conexiones:
            return None
    except Exception:
        return None

    from streamlit_gsheets import GSheetsConnection
    return st.connection("gsheets", type=GSheetsConnection)


def _leer_local():
    if not ARCHIVO.exists():
        return []
    with ARCHIVO.open(encoding="utf-8") as archivo:
        contenido = json.load(archivo)
    return contenido if isinstance(contenido, list) else []


def _leer():
    conexion = _conexion_remota()
    if conexion is None:
        return _leer_local()

    datos = conexion.read(worksheet=HOJA, ttl=0)
    if datos is None or datos.empty:
        return []
    for columna in COLUMNAS:
        if columna not in datos.columns:
            datos[columna] = ""
    registros = datos[COLUMNAS].fillna("").to_dict("records")
    for registro in registros:
        if registro["confianza"] == "":
            registro["confianza"] = (
                "No aplica (regla)" if registro.get("origen") == "regla"
                else "No disponible"
            )
        if registro["intencion_confirmada"] == "":
            registro["intencion_confirmada"] = (
                "Pendiente" if registro.get("estado") == "pendiente"
                else "Descartada" if registro.get("estado") == "descartada"
                else None
            )
        if registro["fecha_revision"] == "":
            registro["fecha_revision"] = (
                "Pendiente" if registro.get("estado") == "pendiente" else None
            )
    return registros


def _escribir_local(registros):
    ARCHIVO.parent.mkdir(parents=True, exist_ok=True)
    temporal = ARCHIVO.with_suffix(".tmp")
    with temporal.open("w", encoding="utf-8") as archivo:
        json.dump(registros, archivo, ensure_ascii=False, indent=2)
    temporal.replace(ARCHIVO)


def _escribir(registros):
    conexion = _conexion_remota()
    if conexion is None:
        _escribir_local(registros)
        return
    datos = pd.DataFrame(registros, columns=COLUMNAS).fillna("")
    conexion.update(worksheet=HOJA, data=datos)


def guardar_pendiente(consulta, respuesta, intencion_predicha,
                      confianza=None, origen="dialogo"):
    confianza_mostrada = (
        round(float(confianza), 4) if confianza is not None
        else "No aplica (regla)" if origen == "regla"
        else "No disponible"
    )
    registro = {
        "id": uuid4().hex,
        "fecha": datetime.now().astimezone().isoformat(timespec="seconds"),
        "consulta": consulta.strip(),
        "respuesta": respuesta.strip(),
        "intencion_predicha": intencion_predicha,
        "confianza": confianza_mostrada,
        "origen": origen,
        "estado": "pendiente",
        "intencion_confirmada": "Pendiente",
        "fecha_revision": "Pendiente",
    }
    with _BLOQUEO:
        registros = _leer()
        registros.append(registro)
        _escribir(registros)
    return registro


def listar_registros(estado=None):
    with _BLOQUEO:
        registros = _leer()
    if estado is None:
        return registros
    return [registro for registro in registros if registro.get("estado") == estado]


def revisar_registro(identificador, estado, intencion_confirmada=None):
    if estado not in {"confirmada", "descartada"}:
        raise ValueError("Estado de revisión no permitido.")
    with _BLOQUEO:
        registros = _leer()
        encontrado = None
        for registro in registros:
            if registro.get("id") == identificador:
                registro["estado"] = estado
                registro["intencion_confirmada"] = (
                    intencion_confirmada if estado == "confirmada" else "Descartada"
                )
                registro["fecha_revision"] = datetime.now().astimezone().isoformat(timespec="seconds")
                encontrado = registro
                break
        if encontrado is None:
            raise KeyError("No se encontró la consulta.")
        _escribir(registros)
    return encontrado


def confirmadas_csv():
    salida = StringIO()
    escritor = csv.DictWriter(
        salida,
        fieldnames=["consulta", "intencion", "origen", "fecha_revision"],
        lineterminator="\n",
    )
    escritor.writeheader()
    for registro in listar_registros("confirmada"):
        escritor.writerow({
            "consulta": registro["consulta"],
            "intencion": registro["intencion_confirmada"],
            "origen": "streamlit_confirmada",
            "fecha_revision": registro["fecha_revision"],
        })
    return salida.getvalue()
