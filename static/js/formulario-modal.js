document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("modalDatos");
  const abrir = document.getElementById("btnAbrirModal");
  const cerrar = document.getElementById("cerrarModal");
  const btnPractica = document.querySelector(".enviar-practica");
  const btnEnviarModal = document.getElementById("enviarModal");
  const formCuestionario = document.querySelector(".detalle-pregunta form");
  const modalError = document.getElementById("modalError");
  const cerrarError = document.getElementById("cerrarError");

  // 👉 SI NO EXISTE EL BOTÓN, NO HAY PREGUNTAS → SALIMOS
  if (!abrir || !formCuestionario) return;

  // ================= FUNCIÓN DE VALIDACIÓN DE PREGUNTAS =================
  // Extraemos esta lógica para no repetir código y mantener tus estilos de error
  const validarPreguntasRespondidas = () => {
    const preguntas = document.querySelectorAll(".pregunta-box");
    let todasRespondidas = true;

    preguntas.forEach((pregunta) => {
      const radios = pregunta.querySelectorAll("input[type='radio']");
      const algunoMarcado = [...radios].some((r) => r.checked);

      if (!algunoMarcado) {
        todasRespondidas = false;
        pregunta.classList.add("sin-responder");
      } else {
        pregunta.classList.remove("sin-responder");
      }
    });

    return todasRespondidas;
  };

  // ================= BOTÓN DE PRÁCTICA (NUEVO) =================
  btnPractica?.addEventListener("click", (event) => {
    event.preventDefault();

    // Usamos la validación para mostrar el modalError si falta algo
    if (!validarPreguntasRespondidas()) {
      modalError.style.display = "flex";
      return;
    }

    // Si todo está respondido, enviamos marcando que es PRÁCTICA
    // No pide datos personales, solo envía el formulario
    formCuestionario.insertAdjacentHTML(
      "beforeend",
      `<input type="hidden" name="es_practica" value="true">`,
    );

    formCuestionario.submit();
  });

  // ================= ABRIR MODAL (BOTÓN ENVIAR RESPUESTAS) =================
  abrir.addEventListener("click", (event) => {
    event.preventDefault();

    // Validamos preguntas antes de abrir el modal de datos
    if (!validarPreguntasRespondidas()) {
      modalError.style.display = "flex";
      return;
    }

    modal.style.display = "flex";
  });

  // ================= CERRAR MODAL =================
  cerrar?.addEventListener("click", () => {
    modal.style.display = "none";
    document.getElementById("nombre").value = "";
    document.getElementById("apellido").value = "";
    document.getElementById("curso").value = "";
    document.getElementById("correo").value = "";
    document.getElementById("mensajeError").textContent = "";
  });

  // ================= ENVIAR MODAL (DATOS PERSONALES) =================
  btnEnviarModal?.addEventListener("click", () => {
    let nombre = document.getElementById("nombre");
    let apellido = document.getElementById("apellido");
    let curso = document.getElementById("curso");
    let correo = document.getElementById("correo");
    let error = document.getElementById("mensajeError");

    error.textContent = "";
    nombre.style.border = "";
    apellido.style.border = "";
    curso.style.border = "";
    correo.style.border = "";

    let faltantes = [];

    if (!nombre.value.trim()) faltantes.push("nombre");
    if (!apellido.value.trim()) faltantes.push("apellido");
    if (!curso.value.trim()) faltantes.push("curso");
    if (!correo.value.trim()) faltantes.push("correo");

    // Mantengo tus mensajes de error de campos faltantes
    if (faltantes.length > 0) {
      error.textContent =
        faltantes.length === 1
          ? `missing ${faltantes[0]}.`
          : faltantes.length === 2
            ? `missing ${faltantes[0]} y el ${faltantes[1]}.`
            : "All fields are missing.";
      return;
    }

    // Mantengo tu validación de solo letras y espacios
    const regexSoloLetras = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/;

    if (!regexSoloLetras.test(nombre.value.trim())) {
      error.textContent = "El nombre no debe contener números ni símbolos.";
      nombre.style.border = "1px solid red";
      return;
    }

    if (!regexSoloLetras.test(apellido.value.trim())) {
      error.textContent = "El apellido no debe contener números ni símbolos.";
      apellido.style.border = "1px solid red";
      return;
    }
    formCuestionario.insertAdjacentHTML(
      "beforeend",
      `<input type="hidden" name="nombre" value="${nombre.value}">
       <input type="hidden" name="apellido" value="${apellido.value}">
       <input type="hidden" name="curso" value="${curso.value}">
       <input type="hidden" name="correo" value="${correo.value}">`,
    );

    formCuestionario.submit();
  });

  // ================= MODAL ERROR (PREGUNTAS FALTANTES) =================
  cerrarError?.addEventListener("click", () => {
    modalError.style.display = "none";
  });
});
