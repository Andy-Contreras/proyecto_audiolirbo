document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("toggleCuestionario");
    const content = document.getElementById("cuestionarioContent");

    btn.addEventListener("click", () => {
        btn.classList.toggle("activo");
        content.classList.toggle("activo");
    });
});

