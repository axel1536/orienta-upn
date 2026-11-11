from pathlib import Path
import json
import joblib

CARPETA = Path(__file__).resolve().parent


def cargar_recursos(carpeta):
    modelo = joblib.load(
        carpeta / "modelos" / "clasificador.joblib"
    )

    with (carpeta / "datos" / "conocimiento.json").open(
        encoding="utf-8-sig"
    ) as archivo:
        registros = json.load(archivo)

    conocimiento = {
        registro["intencion"]: registro
        for registro in registros
    }

    clases = modelo.named_steps["clasificador"].classes_
    faltantes = set(clases) - set(conocimiento)

    if faltantes:
        raise ValueError(
            f"Faltan respuestas para estas intenciones: {faltantes}"
        )

    return modelo, conocimiento


TEMAS = {
    "matricula_requisitos": "Requisitos de matrícula",
    "matricula_fechas": "Fechas de matrícula",
    "horarios_consulta": "Consulta de horarios",
    "becas_requisitos": "Requisitos de becas",
    "pagos_consulta": "Consulta de pagos",
    "constancia_solicitud": "Constancia de estudios",
    "acceso_recuperacion": "Recuperación de acceso",
    "retiro_curso": "Retiro de un curso",
    "carne_solicitud": "Carné universitario",
    "certificado_estudios": "Certificado de estudios",
    "retiro_ciclo": "Retiro del ciclo",
    "traslado_carrera": "Traslado de carrera",
    "traslado_campus": "Traslado de campus",
    "contacto_atencion": "Contacto UPN"
}


def responder(consulta):
    texto = consulta.strip()

    salida = {
        "estado": "derivar",
        "intencion": None,
        "tema": "Atención al estudiante",
        "respuesta": (
            "No identifico un tema para orientar esta consulta. "
            "Indica el trámite o servicio que necesitas, "
            "o consulta a Contacto UPN."
        ),
        "fuente": (
            "https://contacto.upn.edu.pe/canales-de-atencion-upn"
        ),
        "area_responsable": "Contacto UPN"
    }

    if not texto:
        salida.update(
            estado="aclarar",
            respuesta="Escribe una consulta para comenzar."
        )
        return salida

    saludo = texto.lower().strip("¡!¿?. ")

    if saludo in {
        "hola",
        "buenos días",
        "buenas tardes",
        "buenas noches"
    }:
        salida.update(
            estado="saludo",
            respuesta=(
                "¡Hola! Puedo orientarte sobre matrícula, "
                "horarios, becas, pagos y trámites de UPN. "
                "¿Qué necesitas consultar?"
            )
        )
        return salida

    import re
    import unicodedata

    normal = "".join(
        letra
        for letra in unicodedata.normalize("NFD", texto.lower())
        if not unicodedata.combining(letra)
    )

    palabras = set(re.findall(r"[a-z0-9]+", normal))

    def contiene(*raices):
        return any(
            palabra.startswith(raiz)
            for palabra in palabras
            for raiz in raices
        )

    tema_ajeno = contiene(
        "receta", "cocinar", "ensalada", "comida", "ingrediente",
        "futbol", "pelicula", "clima", "musica", "videojuego"
    )

    if tema_ajeno:
        salida["respuesta"] = (
            "Ese tema se sale de la orientación universitaria que manejo. "
            "Sí puedo ayudarte con matrícula, horarios, becas, pagos, "
            "acceso y trámites de UPN."
        )
        return salida

    vector = MODELO.named_steps["tfidf"].transform([texto])

    if vector.nnz == 0:
        return salida

    intencion = str(MODELO.predict([texto])[0])

    registro = CONOCIMIENTO[intencion]

    return {
        "estado": "sugerencia",
        "intencion": intencion,
        "tema": TEMAS.get(intencion, intencion),
        "respuesta": registro["respuesta"],
        "fuente": registro["fuente"],
        "area_responsable": registro["area_responsable"],
        "fecha_revision": registro.get("fecha_revision", "")
    }


MODELO, CONOCIMIENTO = cargar_recursos(CARPETA)
