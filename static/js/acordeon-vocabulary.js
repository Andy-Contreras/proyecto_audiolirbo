document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("toggleVocabulario");
    const content = document.getElementById("vocabularioContent");
    const flecha = btn.querySelector(".flecha");

    btn.addEventListener("click", () => {
        content.classList.toggle("abierto");

        flecha.style.transform = content.classList.contains("abierto")
            ? "rotate(180deg)"
            : "rotate(0deg)";
    });
});