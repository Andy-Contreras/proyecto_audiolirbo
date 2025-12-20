document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("searchInput");
    const rows = document.querySelectorAll(".results-table tbody tr");

    if (!input) return;

    input.addEventListener("keyup", () => {
        const value = input.value.toLowerCase();

        rows.forEach(row => {
            const text = row.innerText.toLowerCase();
            row.style.display = text.includes(value) ? "" : "none";
        });
    });
});