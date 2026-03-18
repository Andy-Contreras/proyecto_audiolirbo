document.addEventListener("DOMContentLoaded", () => {
  const buscador = document.getElementById("buscador");
  const container = document.querySelector(".audiolibros-container");
  const sinResultados = document.getElementById("sinResultados");
  let timeoutId;

  buscador.addEventListener("input", () => {
    // Debounce: esperar 300ms después de que el usuario deje de escribir
    clearTimeout(timeoutId);

    timeoutId = setTimeout(() => {
      const texto = buscador.value.trim();
      buscarAudiobooks(texto);
    }, 300);
  });

  function buscarAudiobooks(query) {
    const url = `/buscar/?q=${encodeURIComponent(query)}`;

    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        mostrarResultados(data.audiobooks);
      })
      .catch((error) => {
        console.error("Error en la búsqueda:", error);
      });
  }

  function mostrarResultados(audiobooks) {
    container.innerHTML = "";

    if (audiobooks.length === 0) {
      sinResultados.style.display = "block";
      return;
    }

    sinResultados.style.display = "none";

    audiobooks.forEach((libro) => {
      const bookCard = document.createElement("div");
      bookCard.className = "book-card libro-item";
      bookCard.innerHTML = `
                <img src="${libro.cover_image}" alt="${libro.title}">
                <h3>${libro.title}</h3>
                <p>Autor: ${libro.author_name}</p>
                <a href="/detalle/${libro.id}/" class="detalle">
                    Detalle
                </a>
            `;
      container.appendChild(bookCard);
    });
  }
});
