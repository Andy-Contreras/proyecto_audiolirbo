document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("modalDatos");
  const abrir = document.getElementById("btnAbrirModal");
  const cerrar = document.getElementById("cerrarModal");
  const btnEnviarModal = document.getElementById("enviarModal");
  const formCuestionario = document.querySelector(".detalle-pregunta form");
  const modalError = document.getElementById("modalError");
  const cerrarError = document.getElementById("cerrarError");

  // 👉 SI NO EXISTE EL BOTÓN, NO HAY PREGUNTAS → SALIMOS
  if (!abrir || !formCuestionario) return;

  // ================= ABRIR MODAL =================
  abrir.addEventListener("click", (event) => {
    event.preventDefault();

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

    if (!todasRespondidas) {
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
    document.getElementById("correo").value = "";
    document.getElementById("mensajeError").textContent = "";
  });

  // ================= ENVIAR MODAL =================
  btnEnviarModal?.addEventListener("click", () => {
    let nombre = document.getElementById("nombre");
    let apellido = document.getElementById("apellido");
    let correo = document.getElementById("correo");
    let error = document.getElementById("mensajeError");

    error.textContent = "";
    nombre.style.border = "";
    apellido.style.border = "";
    correo.style.border = "";

    let faltantes = [];

    if (!nombre.value.trim()) faltantes.push("nombre");
    if (!apellido.value.trim()) faltantes.push("apellido");
    if (!correo.value.trim()) faltantes.push("correo");

    if (faltantes.length > 0) {
      error.textContent =
        faltantes.length === 1
          ? `Falta el ${faltantes[0]}.`
          : faltantes.length === 2
          ? `Faltan el ${faltantes[0]} y el ${faltantes[1]}.`
          : "Faltan todos los campos.";
      return;
    }
    // 2. NUEVA VALIDACIÓN: Solo letras y espacios
    // Esta regex permite letras (a-z), mayúsculas, tildes y la letra ñ
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
       <input type="hidden" name="correo" value="${correo.value}">`
    );

    formCuestionario.submit();
  });

  // ================= MODAL ERROR =================
  cerrarError?.addEventListener("click", () => {
    modalError.style.display = "none";
  });
});
