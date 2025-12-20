let optionCounter = 0;

// Agregar opción al formulario
function addOption(data = null) {
  const container = document.getElementById("options-container");
  const optionId = optionCounter++;

  const optionDiv = document.createElement("div");
  optionDiv.className = "option-row";
  optionDiv.dataset.optionId = optionId;

  optionDiv.innerHTML = `
        <input type="text" 
               name="option_text_${optionId}" 
               placeholder="Paja" 
               value="${data ? data.text : ""}"
               required>
        
        <div class="checkbox-container">
            <input type="checkbox" 
                   name="option_correct_${optionId}" 
                   ${data && data.is_correct ? "checked" : ""}>
        </div>
        
        <textarea name="option_justification_${optionId}" 
                  placeholder="La primera casa que construyó uno de los cerditos fue de paja...">${
                    data ? data.justification || "" : ""
                  }</textarea>
        
        <input type="number" 
               name="option_points_correct_${optionId}" 
               value="${data ? data.points_if_correct : 1}" 
               min="0">
        
        <input type="number" 
               name="option_points_wrong_${optionId}" 
               value="${data ? data.points_if_wrong : 0}" 
               min="0">
        
        <button type="button" class="btn-remove" onclick="removeOption(${optionId})">
            ✗
        </button>
    `;

  container.appendChild(optionDiv);
}

// Remover opción
function removeOption(optionId) {
  const optionDiv = document.querySelector(`[data-option-id="${optionId}"]`);
  if (optionDiv) {
    optionDiv.remove();
  }
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

// Recopilar datos del formulario
function getFormData() {
  const questionText = document.getElementById("question_text").value;
  const questionId = document.getElementById("question_id").value;
  const optionsContainer = document.getElementById("options-container");
  const optionRows = optionsContainer.querySelectorAll(".option-row");

  const options = [];

  optionRows.forEach((row) => {
    const optionId = row.dataset.optionId;

    const text = row.querySelector(`[name="option_text_${optionId}"]`).value;
    const isCorrect = row.querySelector(
      `[name="option_correct_${optionId}"]`
    ).checked;
    const justification = row.querySelector(
      `[name="option_justification_${optionId}"]`
    ).value;
    const pointsCorrect = parseInt(
      row.querySelector(`[name="option_points_correct_${optionId}"]`).value
    );
    const pointsWrong = parseInt(
      row.querySelector(`[name="option_points_wrong_${optionId}"]`).value
    );

    options.push({
      text: text,
      is_correct: isCorrect,
      justification: justification,
      points_if_correct: pointsCorrect,
      points_if_wrong: pointsWrong,
    });
  });

  return {
    question_id: questionId || null,
    question_text: questionText,
    options: options,
  };
}

// Resetear formulario
function resetForm() {
  document.getElementById("questionForm").reset();
  document.getElementById("question_id").value = "";
  document.getElementById("options-container").innerHTML = "";
  optionCounter = 0;

  addOption();
}

// Editar pregunta existente
function editQuestion(button) {
  const questionId = button.dataset.questionId; // Obtener del data attribute
  const questionItem = document.querySelector(
    `[data-question-id="${questionId}"]`
  );

  if (!questionItem) {
    showAlert("No se pudo encontrar la pregunta", "error");
    return;
  }

  const audiobookId = window.location.pathname.split("/")[2];

  fetch(`/question/${questionId}/details/`, {
    method: "GET",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("question_id").value = questionId;
      document.getElementById("question_text").value = data.text;

      document.getElementById("options-container").innerHTML = "";
      optionCounter = 0;

      data.options.forEach((option) => {
        addOption(option);
      });

      window.scrollTo({ top: 0, behavior: "smooth" });
      showAlert(
        "Pregunta cargada para edición. Modifica y guarda los cambios.",
        "success"
      );
    })
    .catch((error) => {
      console.error("Error:", error);
      showAlert("Error al cargar la pregunta para edición", "error");
    });
}

// ========== MODAL DE ELIMINACIÓN DE PREGUNTA ==========

function openDeleteQuestionModal(questionId) {
  const modal = document.getElementById("deleteQuestionModal");
  const questionItem = document.querySelector(
    `[data-question-id="${questionId}"]`
  );

  if (!questionItem) {
    showAlert("No se pudo encontrar la pregunta", "error");
    return;
  }

  const questionText = questionItem.querySelector("h3").textContent;

  document.getElementById("delete_question_preview").textContent = questionText;
  document.getElementById("delete_question_id").value = questionId;

  modal.classList.add("active");
  document.body.style.overflow = "hidden";
}

function closeDeleteQuestionModal() {
  const modal = document.getElementById("deleteQuestionModal");
  modal.classList.remove("active");
  document.body.style.overflow = "";

  document.getElementById("delete_question_preview").textContent = "";
  document.getElementById("delete_question_id").value = "";
}

function confirmDeleteQuestion() {
  const questionId = document.getElementById("delete_question_id").value;

  if (!questionId) {
    showAlert("ID de pregunta no válido", "error");
    closeDeleteQuestionModal();
    return;
  }

  const deleteBtn = document.querySelector(".btn-danger-full");
  const originalText = deleteBtn.innerHTML;
  deleteBtn.disabled = true;
  deleteBtn.innerHTML = "⏳ Eliminando...";

  fetch(`/question/${questionId}/delete/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((response) => response.json())
    .then((data) => {
      deleteBtn.disabled = false;
      deleteBtn.innerHTML = originalText;

      if (data.success) {
        closeDeleteQuestionModal();

        const questionItem = document.querySelector(
          `[data-question-id="${questionId}"]`
        );

        if (questionItem) {
          questionItem.style.animation = "fadeOut 0.3s ease";
          setTimeout(() => {
            questionItem.remove();
            checkEmptyState();
            updateQuestionCount();
          }, 300);
        }

        showAlert("Pregunta eliminada exitosamente", "success");
      } else {
        showAlert("Error al eliminar la pregunta: " + data.message, "error");
        closeDeleteQuestionModal();
      }
    })
    .catch((error) => {
      deleteBtn.disabled = false;
      deleteBtn.innerHTML = originalText;
      console.error("Error:", error);
      showAlert("Error al eliminar la pregunta", "error");
      closeDeleteQuestionModal();
    });
}

function deleteQuestion(button) {
  const questionId = button.dataset.questionId;
  openDeleteQuestionModal(questionId);
}

// Verificar estado vacío
function checkEmptyState() {
  const container = document.getElementById("questions-list-container");
  const questions = container.querySelectorAll(".question-item");

  if (questions.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <div class="empty-state-icon">📝</div>
        <p>No hay preguntas guardadas aún.</p>
        <p style="font-size: 12px; margin-top: 5px;">Crea tu primera pregunta usando el formulario de arriba.</p>
      </div>
    `;
  }
}

// Actualizar contador de preguntas
function updateQuestionCount() {
  const questions = document.querySelectorAll(".question-item");
  const title = document.querySelector(".questions-list-title");
  if (title) {
    title.textContent = `Preguntas Guardadas (${questions.length})`;
  }
}

// ========== EVENT LISTENERS GLOBALES ==========

// Cerrar modal con ESC
document.addEventListener("keydown", function (event) {
  if (event.key === "Escape") {
    closeDeleteQuestionModal();
  }
});

// Cerrar modal al hacer clic fuera
document.addEventListener("click", function (event) {
  const deleteModal = document.getElementById("deleteQuestionModal");

  if (event.target === deleteModal) {
    closeDeleteQuestionModal();
  }
});

// Manejar envío del formulario
document
  .getElementById("questionForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = getFormData();

    if (formData.options.length === 0) {
      showAlert("Debes agregar al menos una opción de respuesta", "error");
      return;
    }

    const hasCorrect = formData.options.some((opt) => opt.is_correct);
    if (!hasCorrect) {
      showAlert("Debes marcar al menos una opción como correcta", "error");
      return;
    }

    const audiobookId = window.location.pathname.split("/")[2];

    fetch(`/audiobook/${audiobookId}/questions/save/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          showAlert("Pregunta guardada exitosamente", "success");
          resetForm();

          setTimeout(() => {
            window.location.reload();
          }, 1500);
        } else {
          showAlert("Error al guardar la pregunta: " + data.message, "error");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        showAlert("Error al guardar la pregunta", "error");
      });
  });

// Agregar animación CSS
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

// Inicializar con una opción por defecto
document.addEventListener("DOMContentLoaded", function () {
  addOption();
});
