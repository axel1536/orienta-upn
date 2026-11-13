from pathlib import Path
import json
import joblib
import re
import unicodedata

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

UMBRAL_CONFIANZA = 0.20
UMBRAL_MARGEN = 0.05
RAICES_UNIVERSITARIAS = (
    "upn", "mimundo", "universit", "matricul", "prematricul",
    "prerrequisit", "curso", "asignatur", "horari", "beca",
    "pago", "pagar", "cuota", "pension", "deuda", "cobro",
    "constancia", "certificad", "document", "tramite", "solicitud",
    "ticket", "contacto", "asesor", "contrasen", "clave", "codigo",
    "cuenta", "acceso", "portal", "retiro", "retir", "traslad",
    "campus", "sede", "ciclo", "semestre", "calendario",
    "convocatoria", "vacante",
)
RAICES_AJENAS = (
    "receta", "cocin", "ensalada", "comida", "ingrediente",
    "futbol", "partido", "pelicula", "serie", "musica", "cancion",
    "clima", "llover", "videojuego", "banco", "bancari", "dolar",
    "salud", "medic", "dieta", "presidente", "politic", "viaje",
    "turismo", "hotel", "celular", "computadora", "perro", "mascota",
    "poema", "chiste", "trabajo", "empleo", "netflix", "spotify",
)


def _palabras_normalizadas(texto):
    normal = "".join(
        letra for letra in unicodedata.normalize("NFD", texto.lower())
        if not unicodedata.combining(letra)
    )
    return set(re.findall(r"[a-z0-9]+", normal))


def consulta_en_alcance(texto):
    """Valida el tema sin intentar clasificarlo en una intención."""
    palabras = _palabras_normalizadas(texto)
    if any(palabra.startswith(RAICES_AJENAS) for palabra in palabras):
        return False
    if re.search(r"\bcarn(?:é|et)\b", texto.lower()):
        return True
    return any(palabra.startswith(RAICES_UNIVERSITARIAS) for palabra in palabras)


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

    if not consulta_en_alcance(texto):
        salida["estado"] = "fuera_alcance"
        salida["respuesta"] = (
            "No tengo información suficiente sobre ese tema. "
            "Puedo orientarte sobre matrícula, horarios, becas, pagos, "
            "acceso y trámites universitarios. Para otros casos, "
            "te recomiendo comunicarte con Contacto UPN."
        )
        return salida

    vector = MODELO.named_steps["tfidf"].transform([texto])

    if vector.nnz == 0:
        return salida

    clasificador = MODELO.named_steps["clasificador"]
    probabilidades = clasificador.predict_proba(vector)[0]
    orden = probabilidades.argsort()
    mejor = int(orden[-1])
    segunda = int(orden[-2])
    confianza = float(probabilidades[mejor])
    margen = float(probabilidades[mejor] - probabilidades[segunda])

    if confianza < UMBRAL_CONFIANZA or margen < UMBRAL_MARGEN:
        salida.update(
            estado="aclarar",
            confianza=confianza,
            margen=margen,
            respuesta=(
                "No tengo información suficiente para identificar tu consulta "
                "con seguridad. Puedes reformularla indicando el trámite o "
                "comunicarte con Contacto UPN."
            ),
        )
        return salida

    intencion = str(clasificador.classes_[mejor])

    registro = CONOCIMIENTO[intencion]

    return {
        "estado": "sugerencia",
        "intencion": intencion,
        "tema": TEMAS.get(intencion, intencion),
        "respuesta": registro["respuesta"],
        "fuente": registro["fuente"],
        "area_responsable": registro["area_responsable"],
        "fecha_revision": registro.get("fecha_revision", ""),
        "confianza": confianza,
        "margen": margen,
    }


MODELO, CONOCIMIENTO = cargar_recursos(CARPETA)
