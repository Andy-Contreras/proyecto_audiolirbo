const btn = document.getElementById("toggleSidebar");
const sidebar = document.getElementById("sidebar");

btn.addEventListener("click", () => {
  sidebar.classList.toggle("open");
});

document.addEventListener("DOMContentLoaded", () => {
    const bars = document.querySelectorAll("#chart-bars .bar");
    const total = Number("{{ usuarios_mes_actual }}") || 0;

    // Simulación simple de distribución
    const values = [
        Math.round(total * 0.2),
        Math.round(total * 0.3),
        Math.round(total * 0.4),
        Math.round(total * 0.1),
    ];

    const max = Math.max(...values, 1);

    bars.forEach((bar, i) => {
        const height = (values[i] / max) * 100;
        bar.style.height = height + "%";
    });
});