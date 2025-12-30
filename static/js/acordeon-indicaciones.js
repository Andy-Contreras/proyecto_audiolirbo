document.addEventListener("DOMContentLoaded", () => {
  // 1. Creamos una función para configurar cualquier botón de "Toggle"
  const configurarToggle = (btnId, contentId) => {
    const btn = document.getElementById(btnId);
    const content = document.getElementById(contentId);

    if (btn && content) {
      const flecha = btn.querySelector(".indicaciones-flecha");

      btn.addEventListener("click", () => {
        content.classList.toggle("abierto");

        // Rotar la flecha si existe
        if (flecha) {
          flecha.style.transform = content.classList.contains("abierto")
            ? "rotate(180deg)"
            : "rotate(0deg)";
        }
      });
    }
  };

  // 2. Aplicamos la función al primer bloque (Instrucciones)
  configurarToggle("indicacionesToggle", "indicacionesContent");

  // 3. Aplicamos la función al segundo bloque (Lesson Plan)
  // Asegúrate de que en tu HTML usaste estos IDs nuevos:
  configurarToggle("indicacionesTogglePDF", "indicacionesContentPDF");
});
