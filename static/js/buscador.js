document.addEventListener("DOMContentLoaded", () => {
    const buscador = document.getElementById("buscador");
    const libros = document.querySelectorAll(".libro-item");
    const sinResultados = document.getElementById("sinResultados");

    buscador.addEventListener("input", () => {
        const texto = buscador.value.toLowerCase();
        let coincidencias = 0;

        libros.forEach(libro => {
            const titulo = libro.querySelector("h3").textContent.toLowerCase();
            const autor = libro.querySelector("p").textContent.toLowerCase();

            if (titulo.includes(texto) || autor.includes(texto)) {
                libro.style.display = "";
                coincidencias++;
            } else {
                libro.style.display = "none";
            }
        });

        // Mostrar mensaje si no hay resultados
        sinResultados.style.display = coincidencias === 0 ? "block" : "none";
    });
});
