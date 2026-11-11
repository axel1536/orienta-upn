import re
import unicodedata
from agente import responder, TEMAS, CONOCIMIENTO, MODELO
from pasos import PASOS

CATEGORIAS = {
    "matricula": ("Matrícula", ["matricula_requisitos", "matricula_fechas"]),
    "pagos": ("Pagos", ["pagos_consulta"]),
    "horarios": ("Horarios", ["horarios_consulta"]),
    "becas": ("Becas", ["becas_requisitos"]),
    "tramites": ("Trámites", ["constancia_solicitud", "carne_solicitud", "certificado_estudios", "retiro_curso", "retiro_ciclo"]),
    "traslados": ("Traslados", ["traslado_carrera", "traslado_campus"]),
    "acceso": ("Acceso a mi cuenta", ["acceso_recuperacion"]),
    "contacto": ("Contacto UPN", ["contacto_atencion"]),
}

BREVES = {
    "matricula_requisitos": "Claro. Para matricularte, entra a MiMundoUPN → Servicios → Matrícula en línea. Antes revisa que la prematrícula esté pagada y que no tengas problemas con prerrequisitos, vacantes o cruces de horario.",
    "matricula_fechas": "Claro. Revisa el calendario de tu programa y periodo, además de los avisos de MiMundoUPN. Si no aparece tu fecha, puedes consultarla mediante Contacto UPN.",
    "horarios_consulta": "Parece que tienes un cruce de horarios. Entra a MiMundoUPN → Cursos, revisa las horas de ambos cursos y verifica si hay otra sección disponible. Si no puedes resolverlo, registra la consulta en Contacto UPN.",
    "becas_requisitos": "Claro. Primero elige la beca o beneficio que te interesa. Luego revisa sus requisitos y la convocatoria vigente en la sección de Becas de UPN, porque las condiciones cambian según el beneficio.",
    "pagos_consulta": "Entiendo. Entra a MiMundoUPN → Pagos → Obligaciones por pagar y abre el detalle del cobro. Si no lo reconoces, no lo pagues todavía: registra una consulta en Contacto UPN con el concepto y el monto.",
    "constancia_solicitud": "Claro. En MiMundoUPN entra a Solicitudes → Listado de trámites, elige Constancia de Estudios, revisa tus datos y sigue las indicaciones de pago. Después podrás revisar su estado en Solicitudes.",
    "acceso_recuperacion": "Entiendo. En la pantalla de MiMundoUPN elige recuperar el acceso y completa la verificación con tu correo o celular registrado. Si el código no llega, solicita ayuda en Contacto UPN. No compartas aquí tu contraseña ni el código.",
    "retiro_curso": "De acuerdo. Primero revisa la fecha límite. Luego entra a MiMundoUPN → Solicitudes → Otras solicitudes → Nueva solicitud → Retiro de curso. Lee las condiciones antes de enviarla, porque el retiro no reduce las cuotas.",
    "carne_solicitud": "Claro. Revisa si hay una convocatoria de carné abierta. Luego entra a MiMundoUPN → Solicitudes → Otras solicitudes → Nueva solicitud y busca el trámite de carné. Si lo perdiste, confirma allí la opción y condiciones para solicitar otro.",
    "certificado_estudios": "Claro. Entra a MiMundoUPN → Solicitudes → Documentos Virtuales → Solicitudes. Elige el certificado que necesitas, sigue el pago y revisa su estado hasta que puedas descargarlo.",
    "retiro_ciclo": "De acuerdo. Revisa primero la fecha límite y luego entra a MiMundoUPN → Solicitudes → Otras solicitudes → Nueva solicitud → Retiro de ciclo. Antes de enviarla, confirma los requisitos y efectos económicos. Dejar de asistir no cuenta como retiro.",
    "traslado_carrera": "Claro. Entra a MiMundoUPN → Solicitudes → Otras solicitudes → Nueva solicitud y busca Traslado de carrera. Antes de enviarla, revisa fechas, vacantes, costos y reconocimiento de cursos.",
    "traslado_campus": "Claro. Entra a MiMundoUPN → Solicitudes → Otras solicitudes → Nueva solicitud y busca Traslado de campus. Revisa las vacantes, el costo y si el cambio afecta algún beneficio antes de enviarla.",
    "contacto_atencion": "Claro. Entra a MiMundoUPN → Servicios → Contacto UPN. Ahí puedes registrar un ticket y revisar su seguimiento. Si ya enviaste uno, busca su estado antes de crear otro.",
}


def normalizar(texto):
    texto = "".join(c for c in unicodedata.normalize("NFD", texto.lower())
                    if not unicodedata.combining(c))
    return " ".join(re.findall(r"[a-z0-9]+", texto.replace("carnet", "carne")))


def opcion(texto, accion):
    return {"texto": texto, "accion": accion}


def elegir_categoria(claves=None, mensaje=None):
    claves = list(claves or CATEGORIAS)
    return ({"respuesta": mensaje or "Claro, ¿sobre qué tema necesitas ayuda?",
             "opciones": [opcion(CATEGORIAS[c][0], "categoria:" + c) for c in claves],
             "explicacion": {"metodo": "Reglas del diálogo", "motivo": "Falta identificar un único tema; se ofrecen categorías para aclararlo."}},
            {"fase": "categorias", "categorias": claves})


def elegir_tema(claves):
    if len(claves) == 1:
        return informar(claves[0])
    preguntas = {
        frozenset({"traslado_carrera", "traslado_campus"}): "¿El traslado es de carrera o de campus?",
        frozenset({"retiro_curso", "retiro_ciclo"}): "¿Quieres retirarte de un curso o de todo el ciclo?",
        frozenset({"matricula_requisitos", "matricula_fechas"}): "¿Necesitas las fechas o los requisitos de matrícula?",
        frozenset({"constancia_solicitud", "certificado_estudios"}): "Claro. ¿Necesitas una constancia o un certificado de estudios?",
        frozenset({"acceso_recuperacion", "contacto_atencion"}): "Entiendo. ¿Quieres recuperar tu acceso o prefieres hablar con un asesor de UPN?",
    }
    opciones = [opcion(TEMAS[c], "tema:" + c) for c in claves]
    if frozenset(claves) == frozenset({"matricula_requisitos", "matricula_fechas"}):
        opciones.append(opcion("Requisitos y fechas", "varios:matricula_requisitos,matricula_fechas"))
    opciones.append(opcion("Otro tema", "menu"))
    return ({"respuesta": preguntas.get(frozenset(claves), "¿Qué necesitas consultar exactamente?"),
             "opciones": opciones,
             "explicacion": {"metodo": "Reglas del diálogo", "motivo": "Hay varias intenciones posibles. Se pregunta cuál necesitas antes de dar una guía."}},
            {"fase": "temas", "temas": claves})


def informar(intencion, metodo="Reglas del diálogo", motivo=None):
    registro = CONOCIMIENTO[intencion]
    return ({"respuesta": BREVES[intencion], "tema": TEMAS[intencion],
             "intencion": intencion,
             "origen": "modelo" if metodo.startswith("Modelo entrenado") else "regla",
             "fuente": registro["fuente"], "detalle": registro["respuesta"],
             "area_responsable": registro["area_responsable"],
             "fecha_revision": registro.get("fecha_revision", ""),
             "opciones": [opcion("Hacer otra consulta", "menu")],
             "explicacion": {"metodo": metodo, "motivo": motivo or "El tema o la opción elegida corresponde a una única intención; se recupera su guía de la base de conocimiento.", "intencion": intencion}},
            {"fase": "respondido", "intencion": intencion})


def informar_varios(intenciones):
    partes = [f"**{TEMAS[i]}**\n\n{BREVES[i]}" for i in intenciones]
    return ({"respuesta": "Perfecto, te explico ambos puntos:\n\n" + "\n\n".join(partes),
             "tema": "Matrícula",
             "fuente": CONOCIMIENTO[intenciones[0]]["fuente"],
             "opciones": [opcion("Hacer otra consulta", "menu")]},
            {"fase": "respondido", "intenciones": intenciones})


def _avanzar(texto="", contexto=None, accion=None):
    contexto = contexto or {}
    normal = normalizar(texto)
    fase = contexto.get("fase")

    if accion == "menu" or normal in {"menu", "inicio", "otra consulta", "otro tema", "cancelar"}:
        return elegir_categoria()
    if accion and accion.startswith("categoria:"):
        categoria = accion.split(":", 1)[1]
        if categoria in CATEGORIAS:
            return elegir_tema(CATEGORIAS[categoria][1])
    if accion and accion.startswith("tema:"):
        intencion = accion.split(":", 1)[1]
        if intencion in CONOCIMIENTO and intencion in BREVES:
            return informar(intencion, metodo="Selección del estudiante", motivo="Elegiste este tema directamente; no fue necesario utilizar el clasificador.")
    if accion and accion.startswith("varios:"):
        intenciones = [i for i in accion.split(":", 1)[1].split(",") if i in CONOCIMIENTO]
        if intenciones:
            return informar_varios(intenciones)
    if fase == "confirmar":
        if accion == "confirmar" or normal in {"si", "si por favor", "si claro", "correcto", "exacto", "confirmo", "de acuerdo", "1"}:
            return informar(contexto["intencion"])
        if normal in {"no", "no gracias", "no es eso", "incorrecto", "2"}:
            return elegir_categoria(mensaje="De acuerdo. ¿Qué tema necesitas?")
    elif normal in {"si", "no", "correcto", "confirmo"}:
        return elegir_categoria(mensaje="Primero elige el tema de tu consulta.")

    if fase in {"categorias", "temas"} and normal.isdecimal() and len(normal) <= 2:
        claves = contexto["categorias" if fase == "categorias" else "temas"]
        numero = int(normal)
        if 1 <= numero <= len(claves):
            clave = claves[numero - 1]
            return (elegir_tema(CATEGORIAS[clave][1]) if fase == "categorias" else informar(clave))

    if fase == "temas" and normal:
        palabras = set(normal.split()) - {"de", "del", "la", "el", "un", "una", "mi", "quiero", "consulta", "consultar", "sobre"}
        puntajes = {c: len(palabras & set(normalizar(TEMAS[c]).split()))
                    for c in contexto["temas"]}
        mayor = max(puntajes.values(), default=0)
        candidatos = [c for c, puntaje in puntajes.items() if puntaje == mayor and mayor > 0]
        if len(candidatos) == 1:
            return informar(candidatos[0])
        if candidatos:
            return elegir_tema(candidatos)

    raices = {"matricula": ("matricul", "prematricul"), "pagos": ("pago", "pagar", "cuota", "pension", "deuda"),
              "horarios": ("horari",), "becas": ("beca",), "tramites": ("tramite",),
              "traslados": ("traslad",),
              "acceso": ("acceso", "contrasen", "cuenta"), "contacto": ("contacto",)}
    palabras = normal.split()

    if any(p.startswith(("receta", "cocin", "ensalada", "comida", "ingrediente")) for p in palabras):
        return ({"respuesta": "Ese tema se sale de la orientación universitaria que manejo. Puedo ayudarte con matrícula, horarios, becas, pagos, acceso y trámites de UPN.",
                 "opciones": [opcion("Hacer otra consulta", "menu")]},
                {"fase": "respondido"})
    tiene_fecha = any(p.startswith(("fecha", "cuando", "hasta", "plazo", "calendario")) for p in palabras)
    tiene_requisito = any(p.startswith(("requisit", "necesit", "condicion", "document", "prerrequisit")) for p in palabras)
    if any(p.startswith("matricul") for p in palabras) and tiene_fecha and tiene_requisito:
        return elegir_tema(["matricula_requisitos", "matricula_fechas"])
    if ("misma hora" in normal or "misma horario" in normal or "cruce de horario" in normal
            or ("dos cursos" in normal and any(p.startswith("hora") for p in palabras))):
        return informar("horarios_consulta")
    if (any(p.startswith(("cobro", "cargo", "monto")) for p in palabras)
            and any(p.startswith(("desconoc", "reconoc", "incorrect", "equivoc")) for p in palabras)):
        return informar("pagos_consulta")
    codigo_no_llega = "codigo" in palabras and any(p.startswith(("lleg", "recib")) for p in palabras)
    pide_asesor = any(p.startswith(("asesor", "atencion", "hablar", "contact")) for p in palabras)
    if codigo_no_llega and pide_asesor:
        return elegir_tema(["acceso_recuperacion", "contacto_atencion"])
    if codigo_no_llega:
        return informar("acceso_recuperacion")
    if (any(p.startswith(("solicitud", "ticket")) for p in palabras)
            and any(p.startswith(("seguim", "estado", "respond", "respuesta", "pendiente")) for p in palabras)):
        return informar("contacto_atencion")
    pide_documento = any(p.startswith(("document", "papel")) for p in palabras)
    prueba_estudios = any(p.startswith(("estudi", "alumno", "egres")) for p in palabras)
    if pide_documento and prueba_estudios:
        return elegir_tema(["constancia_solicitud", "certificado_estudios"])
    if any(p.startswith(("carne", "carnet")) for p in palabras):
        return informar("carne_solicitud")
    if any(p.startswith("retir") for p in palabras):
        claves = []
        if any(p.startswith(("curso", "asignatur")) for p in palabras):
            claves.append("retiro_curso")
        if any(p.startswith(("ciclo", "semestr")) for p in palabras):
            claves.append("retiro_ciclo")
        return elegir_tema(claves or ["retiro_curso", "retiro_ciclo"])
    categorias = [c for c, prefijos in raices.items()
                  if any(p.startswith(prefijos) for p in palabras)]
    if len(categorias) > 1:
        return elegir_categoria(categorias, "¿A cuál de estos temas te refieres?")
    if categorias:
        categoria = categorias[0]
        if categoria == "traslados":
            claves = []
            if any(p.startswith("carrer") for p in palabras):
                claves.append("traslado_carrera")
            if any(p.startswith(("campus", "sede")) for p in palabras):
                claves.append("traslado_campus")
            return elegir_tema(claves or CATEGORIAS[categoria][1])
        especifica = any(p.startswith(("fecha", "cuando", "hasta", "requisit", "document", "necesit", "condicion")) for p in palabras)
        if categoria == "tramites" or (categoria == "matricula" and not especifica):
            return elegir_tema(CATEGORIAS[categoria][1])
        if len(CATEGORIAS[categoria][1]) == 1:
            return informar(CATEGORIAS[categoria][1][0])

    genericas = {"hola", "buenos dias", "buenas tardes", "buenas noches", "consulta", "consultas", "ayuda", "tengo una consulta", "quiero hacer una consulta", "necesito ayuda", "necesito hacer una consulta"}
    if not normal or normal in genericas:
        return elegir_categoria()
    resultado = responder(re.sub(r"\bcarnet\b", "carné", texto, flags=re.IGNORECASE))
    if resultado["estado"] == "sugerencia":
        salida, contexto = informar(resultado["intencion"], metodo="Modelo entrenado: regresión logística", motivo="El modelo clasificó tu pregunta y se recuperó la respuesta asociada. La respuesta procede de la base de conocimiento, no se genera libremente.")
        vectorizador = MODELO.named_steps["tfidf"]
        clasificador = MODELO.named_steps["clasificador"]
        consulta_modelo = re.sub(r"\bcarnet\b", "carné", texto, flags=re.IGNORECASE)
        vector = vectorizador.transform([consulta_modelo])
        puntajes = clasificador.decision_function(vector)[0]
        if hasattr(clasificador, "predict_proba"):
            salida["confianza"] = float(clasificador.predict_proba(vector)[0].max())
        primera = list(clasificador.classes_).index(resultado["intencion"])
        segunda = max((i for i in range(len(puntajes)) if i != primera), key=lambda i: puntajes[i])
        diferencias = clasificador.coef_[primera] - clasificador.coef_[segunda]
        nombres = vectorizador.get_feature_names_out()
        aportes = sorted(((float(valor * diferencias[indice]), str(nombres[indice]))
                          for indice, valor in zip(vector.indices, vector.data)), reverse=True)
        salida["explicacion"]["terminos"] = [termino for aporte, termino in aportes if aporte > 0][:3]
        salida["explicacion"]["comparada_con"] = TEMAS[str(clasificador.classes_[segunda])]
        return salida, contexto
    return elegir_categoria(mensaje="Todavía no ubico bien el tema. ¿Se relaciona con alguna de estas opciones?")


def preguntar_paso(contexto):
    intencion = contexto["intencion"]
    pregunta = PASOS[intencion][contexto["paso"]][0]
    return ({"respuesta": pregunta, "tema": "Mis pasos · " + TEMAS[intencion],
             "opciones": [opcion("Sí", "paso:si"), opcion("No", "paso:no"),
                          opcion("Aún no lo sé", "paso:no_se"), opcion("Cancelar revisión", "menu")],
             "explicacion": {"metodo": "Sistema experto: hechos y reglas", "motivo": "Se pregunta por un punto de la guía para identificar los pasos que todavía necesitas revisar."}}, contexto)


def revisar_paso(contexto, valor):
    nuevo = dict(contexto, hechos=list(contexto["hechos"]) + [valor], paso=contexto["paso"] + 1)
    intencion = nuevo["intencion"]
    pasos = PASOS[intencion]
    if nuevo["paso"] < len(pasos):
        return preguntar_paso(nuevo)
    pendientes = [siguiente for (_, siguiente), hecho in zip(pasos, nuevo["hechos"]) if hecho != "si"]
    resultado, final = informar(intencion)
    resultado["respuesta"] = ("Estos son los puntos que te falta revisar:\n\n" + "\n".join("- " + p for p in pendientes)
                              if pendientes else "Marcaste todos los puntos como revisados. Continúa con las indicaciones del portal de UPN.")
    resultado["respuesta"] += "\n\nEsta lista es una orientación; no confirma la aprobación de un trámite."
    etiquetas = {"si": "Revisado", "no": "Pendiente", "no_se": "Por confirmar"}
    resultado["lista_estado"] = [{"Punto": pregunta, "Tu respuesta": etiquetas[hecho]}
                                  for (pregunta, _), hecho in zip(pasos, nuevo["hechos"])]
    resultado["explicacion"] = {"metodo": "Sistema experto: hechos y reglas",
        "motivo": "SI un punto está pendiente o no está confirmado, ENTONCES se incluye en los siguientes pasos. Solo se usan tus respuestas de esta conversación.",
        "hechos": resultado["lista_estado"], "intencion": intencion}
    return resultado, final


def avanzar(texto="", contexto=None, accion=None):
    contexto = contexto or {}
    normal = normalizar(texto)
    if accion and accion.startswith("lista:"):
        intencion = accion.split(":", 1)[1]
        if intencion in PASOS:
            return preguntar_paso({"fase": "pasos", "intencion": intencion, "paso": 0, "hechos": []})
    if contexto.get("fase") == "pasos" and accion != "menu":
        valor = (accion.split(":", 1)[1] if accion and accion.startswith("paso:") else
                 {"si": "si", "si ya": "si", "1": "si", "no": "no", "2": "no", "no se": "no_se", "aun no lo se": "no_se", "3": "no_se"}.get(normal))
        if valor in {"si", "no", "no_se"}:
            return revisar_paso(contexto, valor)
        if normal == "4":
            return elegir_categoria()
        return _avanzar(texto, {}, accion)
    return _avanzar(texto, contexto, accion)


def crear_conversacion():
    return {"contexto": {}, "historial": [], "consulta_actual": None}


def conversar(sesion, texto, accion=None):
    resultado, contexto = avanzar(texto, sesion["contexto"], accion)
    consulta_actual = sesion.get("consulta_actual")
    if accion == "menu":
        consulta_actual = None
    elif accion is None and texto.strip():
        mensajes_genericos = {
            "hola", "buenos dias", "buenas tardes", "buenas noches",
            "consulta", "consultas", "ayuda", "tengo una consulta",
            "quiero hacer una consulta", "necesito ayuda",
        }
        consulta_actual = (None if normalizar(texto) in mensajes_genericos
                           else texto.strip())
    if not sesion["historial"]:
        resultado = dict(resultado, respuesta="¡Hola! " + resultado["respuesta"])
        if accion is None and normalizar(texto) in {"hola", "buenos dias", "buenas tardes", "buenas noches"}:
            resultado.pop("explicacion", None)
    return {"contexto": contexto, "consulta_actual": consulta_actual,
            "historial": sesion["historial"] + [
        {"role": "user", "texto": texto, "accion": accion},
        {"role": "assistant", "resultado": resultado},
    ]}
