"""Preguntas y siguientes pasos derivados de la base de conocimiento del proyecto.

Son puntos para revisar, no decisiones de aprobación de trámites.
Cada tupla contiene: pregunta, siguiente paso si está pendiente.
"""

PASOS = {
    "matricula_requisitos": [
        ("¿Ya verificaste el pago de tu prematrícula?", "Verifica tu prematrícula en MiMundoUPN."),
        ("¿Ya revisaste los prerrequisitos de los cursos que quieres llevar?", "Revisa los prerrequisitos de tus cursos antes de registrarlos."),
        ("¿Ya comprobaste que tus cursos no tengan cruces de horario?", "Revisa que los horarios de los cursos no se crucen."),
        ("¿Ya revisaste las vacantes de tus cursos?", "Consulta las vacantes de tu campus y carrera en matrícula en línea."),
    ],
    "matricula_fechas": [
        ("¿Ya identificaste tu programa y periodo académico?", "Identifica tu programa y periodo antes de elegir el calendario."),
        ("¿Ya revisaste el calendario y los avisos de MiMundoUPN?", "Revisa el calendario de tu periodo y los avisos de MiMundoUPN."),
    ],
    "horarios_consulta": [
        ("¿Puedes ingresar a tu cuenta de MiMundoUPN?", "Recupera el acceso a tu cuenta si no puedes ingresar."),
        ("¿Ya abriste la opción Cursos?", "Abre Cursos en MiMundoUPN para consultar tu horario."),
    ],
    "becas_requisitos": [
        ("¿Ya elegiste la beca o beneficio que deseas consultar?", "Identifica la beca o beneficio que te interesa."),
        ("¿Ya revisaste los requisitos y la convocatoria de ese beneficio?", "Revisa su convocatoria y el Reglamento de Becas en la fuente de UPN."),
    ],
    "pagos_consulta": [
        ("¿Ya ingresaste a la sección Pagos de MiMundoUPN?", "Entra a MiMundoUPN y abre Pagos."),
        ("¿Ya revisaste Obligaciones por pagar?", "Consulta Obligaciones por pagar para revisar los conceptos pendientes."),
    ],
    "constancia_solicitud": [
        ("¿Ya confirmaste que necesitas una constancia de estudios de pregrado?", "Confirma qué constancia necesitas; otros documentos pueden tener procedimientos distintos."),
        ("¿Ya revisaste la vista previa, el costo y el plazo?", "Revisa los datos del documento, el costo y el plazo antes de continuar."),
    ],
    "acceso_recuperacion": [
        ("¿Ya intentaste la opción de recuperación de MiMundoUPN?", "Selecciona recuperar acceso en el portal institucional."),
        ("¿Puedes completar la verificación con el correo o celular registrado?", "Solicita apoyo a UPN si no puedes completar la verificación. No compartas códigos en este chat."),
    ],
    "retiro_curso": [
        ("¿Ya verificaste el plazo y los requisitos de retiro de curso?", "Revisa el calendario y los requisitos antes de solicitar el retiro."),
        ("¿Ya revisaste el costo y el efecto sobre tus cuotas de pensión?", "Revisa el costo; el retiro de un curso no reduce las cuotas de pensión."),
    ],
    "carne_solicitud": [
        ("¿Ya verificaste que exista una convocatoria de carné abierta?", "Consulta si hay una convocatoria de carné vigente."),
        ("¿Ya revisaste los requisitos de la fotografía?", "Comprueba que tu fotografía cumpla los requisitos publicados."),
        ("¿Ya revisaste las fechas y las indicaciones de pago?", "Revisa fechas, condiciones e indicaciones de pago de la convocatoria."),
    ],
    "certificado_estudios": [
        ("¿Ya identificaste qué certificado necesitas: por periodos o de egreso?", "Elige el certificado que corresponda a los periodos o al egreso."),
        ("¿Ya revisaste las características, el costo y el plazo del documento?", "Revisa las características, el costo y el plazo en Documentos Virtuales."),
    ],
    "retiro_ciclo": [
        ("¿Ya revisaste el calendario y las condiciones de retiro de tu programa?", "Revisa el calendario y las condiciones aplicables a tu programa."),
        ("¿Ya revisaste los efectos económicos y las autorizaciones que correspondan?", "Confirma efectos económicos y autorizaciones antes de solicitar el retiro. Dejar de asistir no lo formaliza."),
    ],
    "traslado_carrera": [
        ("¿Ya revisaste fechas, requisitos y vacantes de la carrera de destino?", "Consulta fechas, requisitos y vacantes de la carrera de destino."),
        ("¿Ya consultaste el reconocimiento de cursos y los costos del traslado?", "Revisa reconocimiento de cursos, pensiones y derecho de trámite antes de solicitarlo."),
    ],
    "traslado_campus": [
        ("¿Ya revisaste fechas y disponibilidad en el campus de destino?", "Revisa fechas y disponibilidad de carrera, ciclo y vacantes en el destino."),
        ("¿Ya revisaste las pensiones, el costo y el posible cambio en tus beneficios?", "Revisa costos y posibles cambios en tus beneficios antes de solicitar el traslado."),
    ],
    "contacto_atencion": [
        ("¿Ya revisaste las preguntas frecuentes de tu tema?", "Revisa las preguntas frecuentes de tu tema en MiMundoUPN."),
        ("Si necesitas atención, ¿ya identificaste cómo registrar o seguir un ticket?", "En Contacto UPN elige el tema y subtema para registrar un ticket o revisar su seguimiento."),
    ],
}
