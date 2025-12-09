const modal = document.getElementById("modalDatos");
const abrir = document.getElementById("btnAbrirModal");
const cerrar = document.getElementById("cerrarModal");
const btnEnviarModal = document.getElementById("enviarModal");
const formCuestionario = document.querySelector(".detalle-pregunta form");


// VALIDACIÓN antes de abrir el modal
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
    document.getElementById("modalError").style.display = "flex";
    return;
  }

  modal.style.display = "flex";
});

cerrar.addEventListener("click", () => {
  modal.style.display = "none";
  document.getElementById("nombre").value = "";
  document.getElementById("apellido").value = "";
  document.getElementById("correo").value = "";
  document.getElementById("mensajeError").textContent = "";
});

btnEnviarModal.addEventListener("click", () => {
  let nombre = document.getElementById("nombre");
  let apellido = document.getElementById("apellido");
  let correo = document.getElementById("correo");
  let error = document.getElementById("mensajeError");

  error.textContent = "";
  nombre.style.border = "";
  apellido.style.border = "";
  correo.style.border = "";

  let faltantes = [];

  if (nombre.value.trim() === "") faltantes.push("nombre");
  if (apellido.value.trim() === "") faltantes.push("apellido");
  if (correo.value.trim() === "") faltantes.push("correo");

  if (faltantes.length > 0) {
    if (faltantes.length === 1) {
      error.textContent = `Falta el ${faltantes[0]}.`;
    } else if (faltantes.length === 2) {
      error.textContent = `Faltan el ${faltantes[0]} y el ${faltantes[1]}.`;
    } else {
      error.textContent = "Faltan todos los campos.";
    }
    return;
  }

  error.textContent = "";

  formCuestionario.insertAdjacentHTML(
    "beforeend",
    `<input type="hidden" name="nombre" value="${nombre.value}">
     <input type="hidden" name="apellido" value="${apellido.value}">
     <input type="hidden" name="correo" value="${correo.value}">`
  );

  nombre.value = "";
  apellido.value = "";
  correo.value = "";

  formCuestionario.submit();
});

document.getElementById("cerrarError").addEventListener("click", () => {
    document.getElementById("modalError").style.display = "none";
});