document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".answers-block").forEach((block) => {
    const container = block.querySelector(".answers-container");
    const addBtn = block.querySelector(".add-answer-btn");
    const totalFormsInput = block.querySelector('input[name$="-TOTAL_FORMS"]');

    if (!container || !addBtn || !totalFormsInput) return;

    /* ===================== */
    /* ➕ AGREGAR OPCIÓN */
    /* ===================== */
    addBtn.addEventListener("click", () => {
      const totalForms = parseInt(totalFormsInput.value);
      const firstForm = container.children[0];

      const newForm = firstForm.cloneNode(true);

      const regex = new RegExp(`-(\\d+)-`, "g");
      newForm.innerHTML = newForm.innerHTML.replace(regex, `-${totalForms}-`);

      newForm.querySelectorAll("input, textarea").forEach((input) => {
        if (input.type === "checkbox") {
          input.checked = false;
        } else {
          input.value = "";
        }
      });

      container.appendChild(newForm);
      totalFormsInput.value = totalForms + 1;
    });

    /* ===================== */
    /* ❌ ELIMINAR OPCIÓN */
    /* ===================== */
    container.addEventListener("click", (e) => {
      if (!e.target.classList.contains("remove-answer-btn")) return;

      const card = e.target.closest(".answer-card");
      const deleteInput = card.querySelector(
        'input[type="checkbox"][name$="DELETE"]'
      );

      if (deleteInput) {
        deleteInput.checked = true;
      }

      card.style.display = "none";
    });
  });
});
