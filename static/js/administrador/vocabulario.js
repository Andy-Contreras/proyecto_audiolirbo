let itemCounter = 0;

// Obtener CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Mostrar alerta
function showAlert(message, type = "success") {
  const alertContainer = document.getElementById("alert-container");
  const alertClass = type === "success" ? "alert-success" : "alert-error";

  alertContainer.innerHTML = `
        <div class="alert ${alertClass}">
            ${message}
        </div>
    `;

  window.scrollTo({ top: 0, behavior: "smooth" });

  setTimeout(() => {
    alertContainer.innerHTML = "";
  }, 5000);
}

// Agregar item de vocabulario
function addVocabItem(data = null) {
  const container = document.getElementById("vocabulary-items");
  const itemId = itemCounter++;

  const itemDiv = document.createElement("div");
  itemDiv.className = "vocab-item";
  itemDiv.dataset.itemId = itemId;

  itemDiv.innerHTML = `
        <div class="vocab-item-header">
            <span class="vocab-number">Palabra #${itemCounter}</span>
            <button type="button" class="btn-remove-item" onclick="removeVocabItem(${itemId})">
                ✗ Eliminar
            </button>
        </div>
        <div class="vocab-fields">
            <div class="field-group">
                <label class="label-required">Palabra</label>
                <input type="text" 
                       name="palabra_${itemId}" 
                       placeholder="Ej: Resiliencia"
                       value="${data ? data.palabra : ""}"
                       required>
            </div>
            <div class="field-group">
                <label class="label-required">Definición</label>
                <textarea name="definicion_${itemId}" 
                          placeholder="Escribe la definición..."
                          required>${data ? data.definicion : ""}</textarea>
            </div>
            <div class="field-group full-width">
                <label>Ejemplo de uso <span class="label-optional">(opcional)</span></label>
                <textarea name="ejemplo_${itemId}" 
                          placeholder="Escribe un ejemplo...">${
                            data ? data.ejemplo || "" : ""
                          }</textarea>
            </div>
        </div>
    `;

  container.appendChild(itemDiv);
}

// Remover item de vocabulario
function removeVocabItem(itemId) {
  const item = document.querySelector(`[data-item-id="${itemId}"]`);
  if (item) {
    item.style.animation = "fadeOut 0.3s ease";
    setTimeout(() => {
      item.remove();
      updateItemNumbers();
    }, 300);
  }
}

// Actualizar números de items
function updateItemNumbers() {
  const items = document.querySelectorAll(".vocab-item");
  items.forEach((item, index) => {
    const number = item.querySelector(".vocab-number");
    if (number) {
      number.textContent = `Palabra #${index + 1}`;
    }
  });
}

// Limpiar formulario
function clearForm() {
  if (confirm("¿Estás seguro de que quieres limpiar todos los campos?")) {
    document.getElementById("vocabulary-items").innerHTML = "";
    itemCounter = 0;
    addVocabItem();
  }
}

// Recopilar datos del formulario
function getFormData() {
  const container = document.getElementById("vocabulary-items");
  const items = container.querySelectorAll(".vocab-item");
  const vocabulario = [];

  items.forEach((item) => {
    const itemId = item.dataset.itemId;
    const palabra = item
      .querySelector(`[name="palabra_${itemId}"]`)
      .value.trim();
    const definicion = item
      .querySelector(`[name="definicion_${itemId}"]`)
      .value.trim();
    const ejemplo = item
      .querySelector(`[name="ejemplo_${itemId}"]`)
      .value.trim();

    if (palabra && definicion) {
      vocabulario.push({
        palabra: palabra,
        definicion: definicion,
        ejemplo: ejemplo,
      });
    }
  });

  return vocabulario;
}

// ========== MODAL DE EDICIÓN ==========

function openEditModal(vocabId) {
  const modal = document.getElementById("editModal");
  modal.classList.add("active");
  document.body.style.overflow = "hidden";

  fetch(`/vocabulario/${vocabId}/details/`, {
    method: "GET",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        document.getElementById("edit_vocab_id").value = data.id;
        document.getElementById("edit_palabra").value = data.palabra;
        document.getElementById("edit_definicion").value = data.definicion;
        document.getElementById("edit_ejemplo").value = data.ejemplo || "";
      } else {
        showAlert(data.message, "error");
        closeEditModal();
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      showAlert("Error al cargar los datos", "error");
      closeEditModal();
    });
}

function closeEditModal() {
  const modal = document.getElementById("editModal");
  modal.classList.remove("active");
  document.body.style.overflow = "";

  document.getElementById("editForm").reset();
  document.getElementById("edit_vocab_id").value = "";
}

function editVocabulary(button) {
  const vocabId = button.dataset.vocabId;
  openEditModal(vocabId);
}

// Manejar envío del formulario de edición
document.getElementById("editForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const vocabId = document.getElementById("edit_vocab_id").value;
  const palabra = document.getElementById("edit_palabra").value.trim();
  const definicion = document.getElementById("edit_definicion").value.trim();
  const ejemplo = document.getElementById("edit_ejemplo").value.trim();

  if (!palabra || !definicion) {
    showAlert("La palabra y la definición son requeridas", "error");
    return;
  }

  const submitBtn = this.querySelector('button[type="submit"]');
  submitBtn.disabled = true;

  fetch(`/vocabulario/${vocabId}/update/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      palabra: palabra,
      definicion: definicion,
      ejemplo: ejemplo,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      submitBtn.disabled = false;

      if (data.success) {
        showAlert("Palabra actualizada exitosamente", "success");
        closeEditModal();

        const card = document.querySelector(`[data-vocab-id="${vocabId}"]`);
        if (card) {
          card.querySelector(".vocab-word").textContent = data.vocab.palabra;
          card.querySelector(".vocab-definition").textContent =
            data.vocab.definicion;

          let exampleDiv = card.querySelector(".vocab-example");
          if (data.vocab.ejemplo) {
            if (!exampleDiv) {
              exampleDiv = document.createElement("div");
              exampleDiv.className = "vocab-example";
              card.querySelector(".vocab-definition").after(exampleDiv);
            }
            exampleDiv.textContent = `💬 ${data.vocab.ejemplo}`;
          } else if (exampleDiv) {
            exampleDiv.remove();
          }
        }
      } else {
        showAlert(data.message, "error");
      }
    })
    .catch((error) => {
      submitBtn.disabled = false;
      console.error("Error:", error);
      showAlert("Error al actualizar la palabra", "error");
    });
});

// ========== MODAL DE ELIMINACIÓN ==========

function openDeleteModal(vocabId) {
  const modal = document.getElementById("deleteModal");
  const card = document.querySelector(`[data-vocab-id="${vocabId}"]`);

  if (!card) {
    showAlert("No se pudo encontrar la palabra", "error");
    return;
  }

  const palabra = card.querySelector(".vocab-word").textContent;

  document.getElementById("delete_palabra_name").textContent = palabra;
  document.getElementById("delete_vocab_id").value = vocabId;

  modal.classList.add("active");
  document.body.style.overflow = "hidden";
}

function closeDeleteModal() {
  const modal = document.getElementById("deleteModal");
  modal.classList.remove("active");
  document.body.style.overflow = "";

  document.getElementById("delete_palabra_name").textContent = "";
  document.getElementById("delete_vocab_id").value = "";
}

function confirmDelete() {
  const vocabId = document.getElementById("delete_vocab_id").value;

  if (!vocabId) {
    showAlert("ID de vocabulario no válido", "error");
    closeDeleteModal();
    return;
  }

  const deleteBtn = document.querySelector(".btn-danger-full");
  deleteBtn.disabled = true;

  fetch(`/vocabulario/${vocabId}/delete/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((response) => response.json())
    .then((data) => {
      deleteBtn.disabled = false;

      if (data.success) {
        closeDeleteModal();

        const card = document.querySelector(`[data-vocab-id="${vocabId}"]`);
        if (card) {
          card.style.animation = "fadeOut 0.3s ease";
          setTimeout(() => {
            card.remove();
            updateCounter();
            checkEmptyState();
          }, 300);
        }

        showAlert(data.message, "success");
      } else {
        showAlert(data.message, "error");
        closeDeleteModal();
      }
    })
    .catch((error) => {
      deleteBtn.disabled = false;
      console.error("Error:", error);
      showAlert("Error al eliminar la palabra", "error");
      closeDeleteModal();
    });
}

function deleteVocabulary(button) {
  const vocabId = button.dataset.vocabId;
  openDeleteModal(vocabId);
}

// Actualizar contador
function updateCounter() {
  const cards = document.querySelectorAll(".vocabulary-card");
  const counter = document.querySelector(".list-count");
  if (counter) {
    counter.textContent = cards.length;
  }
}

// Verificar estado vacío
function checkEmptyState() {
  const container = document.getElementById("vocabulary-list-container");
  const cards = container.querySelectorAll(".vocabulary-card");

  if (cards.length === 0) {
    container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📚</div>
                <h3>No hay palabras guardadas aún</h3>
                <p>Comienza agregando vocabulario relevante para este audiolibro.</p>
            </div>
        `;
  }
}

// Manejar envío del formulario principal
document
  .getElementById("vocabularyForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();

    const vocabulario = getFormData();

    if (vocabulario.length === 0) {
      showAlert(
        "Debes agregar al menos una palabra con su definición",
        "error"
      );
      return;
    }

    const submitBtn = this.querySelector('button[type="submit"]');
    submitBtn.disabled = true;

    fetch(`/audiobook/${AUDIOBOOK_ID}/vocabulario/save/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ vocabulario: vocabulario }),
    })
      .then((response) => response.json())
      .then((data) => {
        submitBtn.disabled = false;

        if (data.success) {
          let message = data.message;
          if (data.errors && data.errors.length > 0) {
            message += "\n\nAdvertencias:\n" + data.errors.join("\n");
          }

          showAlert(message, "success");

          document.getElementById("vocabulary-items").innerHTML = "";
          itemCounter = 0;
          addVocabItem();

          setTimeout(() => {
            window.location.reload();
          }, 1500);
        } else {
          showAlert(data.message, "error");
        }
      })
      .catch((error) => {
        submitBtn.disabled = false;
        console.error("Error:", error);
        showAlert("Error al guardar las palabras", "error");
      });
  });

// ========== EVENT LISTENERS GLOBALES ==========

// Cerrar modales con ESC
document.addEventListener("keydown", function (event) {
  if (event.key === "Escape") {
    closeEditModal();
    closeDeleteModal();
  }
});

// Cerrar modales al hacer clic fuera
document.addEventListener("click", function (event) {
  const editModal = document.getElementById("editModal");
  const deleteModal = document.getElementById("deleteModal");

  if (event.target === editModal) {
    closeEditModal();
  }

  if (event.target === deleteModal) {
    closeDeleteModal();
  }
});

// Agregar animaciones CSS
const style = document.createElement("style");
style.textContent = `
    @keyframes fadeOut {
        from {
            opacity: 1;
            transform: scale(1);
        }
        to {
            opacity: 0;
            transform: scale(0.95);
        }
    }
`;
document.head.appendChild(style);

// Inicializar con un item por defecto
document.addEventListener("DOMContentLoaded", function () {
  addVocabItem();
});
