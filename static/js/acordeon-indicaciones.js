document.addEventListener("DOMContentLoaded", () => {

    const btn = document.getElementById("indicacionesToggle");
    const content = document.getElementById("indicacionesContent");
    const flecha = document.querySelector(".indicaciones-flecha");

    if (btn && content) {
        btn.addEventListener("click", () => {
            content.classList.toggle("abierto");
            flecha.style.transform = content.classList.contains("abierto")
                ? "rotate(180deg)"
                : "rotate(0deg)";
        });
    }

});
