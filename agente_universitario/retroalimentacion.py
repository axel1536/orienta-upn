from datetime import datetime
from io import StringIO
import csv
import json
from pathlib import Path
from threading import Lock
from uuid import uuid4


ARCHIVO = Path(__file__).resolve().parent / "datos" / "consultas_por_revisar.json"
_BLOQUEO = Lock()


def _leer():
    if not ARCHIVO.exists():
        return []
    with ARCHIVO.open(encoding="utf-8") as archivo:
        contenido = json.load(archivo)
    return contenido if isinstance(contenido, list) else []


def _escribir(registros):
    ARCHIVO.parent.mkdir(parents=True, exist_ok=True)
    temporal = ARCHIVO.with_suffix(".tmp")
    with temporal.open("w", encoding="utf-8") as archivo:
        json.dump(registros, archivo, ensure_ascii=False, indent=2)
    temporal.replace(ARCHIVO)


def guardar_pendiente(consulta, respuesta, intencion_predicha,
                      confianza=None, origen="dialogo"):
    registro = {
        "id": uuid4().hex,
        "fecha": datetime.now().astimezone().isoformat(timespec="seconds"),
        "consulta": consulta.strip(),
        "respuesta": respuesta.strip(),
        "intencion_predicha": intencion_predicha,
        "confianza": None if confianza is None else round(float(confianza), 4),
        "origen": origen,
        "estado": "pendiente",
        "intencion_confirmada": None,
        "fecha_revision": None,
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
                    intencion_confirmada if estado == "confirmada" else None
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
