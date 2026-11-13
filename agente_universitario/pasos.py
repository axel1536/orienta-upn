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
    "convalidacion_cursos": [
        ("¿Ya revisaste qué documentos exige UPN para acreditar tus estudios previos?", "Consulta en MiMundoUPN → Mis Documentos los certificados, constancias o sílabos que debes presentar."),
        ("¿Ya cargaste los documentos solicitados en el portal?", "Sube los documentos pendientes en Mis Documentos y corrige los que estén observados."),
        ("¿Ya verificaste el estado de la evaluación de equivalencias?", "Revisa el resultado de la evaluación; si hay una observación, corrígela o registra un ticket en Contacto UPN."),
    ],
    "examen_sustitutorio": [
        ("¿Ya verificaste que tu curso admita examen sustitutorio?", "Confirma en el reglamento o con tu coordinador si el curso permite evaluación sustitutoria."),
        ("¿Estás dentro del plazo establecido para solicitarlo?", "Revisa el calendario académico para confirmar las fechas del examen sustitutorio."),
        ("¿Ya revisaste el trámite y el pago en MiMundoUPN?", "Consulta en MiMundoUPN el trámite y realiza el pago correspondiente. Si no aparece, registra una consulta en Contacto UPN."),
    ],
    "correo_institucional": [
        ("¿Ya verificaste que tu cuenta termine en @upn.pe?", "Confirma que el dominio de tu correo institucional sea @upn.pe."),
        ("¿Puedes ingresar con tu contraseña actual?", "Si olvidaste la clave, usa la recuperación de acceso de MiMundoUPN. No compartas contraseñas ni códigos en este chat."),
        ("¿Ya revisaste la carpeta de spam de tu correo personal?", "Si no llega el código de verificación, revisa la carpeta de spam o correo no deseado."),
    ],
    "calendario_academico": [
        ("¿Ya identificaste tu programa y modalidad (Pregrado Tradicional o Adulto Trabajador)?", "Confirma tu programa para elegir el calendario correcto."),
        ("¿Ya descargaste el calendario académico vigente?", "Descarga la versión vigente desde la fuente oficial de UPN."),
    ],
    "modalidad_estudios": [
        ("¿Ya revisaste la disponibilidad de la modalidad que te interesa para tu carrera?", "Consulta qué modalidades ofrece tu carrera antes de solicitar el cambio."),
        ("¿Ya revisaste la convocatoria y los requisitos del cambio de modalidad?", "Revisa la convocatoria, requisitos y evaluación académica necesarios."),
        ("¿Ya confirmaste si el cambio afecta tus pensiones o beneficios?", "Verifica costos y efectos sobre tus beneficios antes de pagar y registrar la solicitud."),
    ],
    "biblioteca_servicio": [
        ("¿Ya ingresaste a la Biblioteca Virtual con tu correo institucional?", "Accede desde MiMundoUPN, la App UPN, el Aula Virtual o la web de Biblioteca UPN con tu cuenta @upn.pe."),
        ("¿Encontraste el recurso que necesitas en el catálogo o las bases de datos?", "Si no lo encuentras, consulta los servicios de tu campus o utiliza Bibliotecario en Línea."),
    ],
    "notas_calificaciones": [
        ("¿Ya revisaste el curso en MiMundoUPN → Mis estudios → Cursos y Notas?", "Abre el curso y consulta la sección Notas para ver cada evaluación, su peso y la calificación registrada."),
        ("Si detectaste un error, ¿ya reuniste la evidencia de la evaluación?", "Conserva la evaluación y registra la solicitud de revisión mediante Contacto UPN dentro del plazo vigente."),
    ],
    "asistencia_clases": [
        ("¿Ya revisaste la sección Asistencias del curso en MiMundoUPN?", "Entra a Mis estudios → Cursos y Notas, abre el curso y revisa el registro por fecha."),
        ("Si el registro es incorrecto, ¿tienes evidencia o un documento de sustento?", "Reúne la evidencia de asistencia o el sustento de la ausencia antes de consultar a UPN."),
    ],
    "practicas_preprofesionales": [
        ("¿Ya confirmaste la modalidad de práctica que vas a realizar?", "Identifica si corresponde a prácticas preprofesionales, pasantía u otra modalidad."),
        ("¿Ya solicitaste la carta de presentación para la empresa?", "Solicita la carta de presentación en MiMundoUPN con los datos de la empresa."),
        ("¿Tienes el convenio y el plan de capacitación firmados?", "Envía ambos documentos mediante Contacto UPN para solicitar la firma y el registro correspondiente."),
    ],
    "idiomas_requisito": [
        ("¿Ya verificaste qué idioma y nivel exige tu programa?", "Consulta el requisito vigente de tu carrera antes de registrar o pagar una solicitud."),
        ("¿Ya identificaste cómo acreditarás el requisito?", "Revisa si corresponde un certificado aceptado, una evaluación de suficiencia u otra opción reconocida por UPN."),
    ],
    "bolsa_laboral": [
        ("¿Ya creaste o actualizaste tu perfil en el Portal Empléate?", "Completa tus datos y actualiza tu currículum antes de postular."),
        ("¿Ya filtraste las ofertas según tu carrera y el tipo de trabajo que buscas?", "Busca prácticas o empleos y revisa los requisitos de cada oferta antes de postular."),
    ],
}
