document.addEventListener("DOMContentLoaded", function () {
  const ctx = document.getElementById("usuariosChart");

  if (!ctx) return;

  // Crear gradiente para el fondo del gráfico
  const gradient = ctx.getContext("2d").createLinearGradient(0, 0, 0, 400);
  gradient.addColorStop(0, "rgba(102, 126, 234, 0.4)");
  gradient.addColorStop(1, "rgba(102, 126, 234, 0.0)");

  const chart = new Chart(ctx, {
    type: "line",
    data: {
      labels: mesesLabels,
      datasets: [
        {
          label: "Nuevos Usuarios",
          data: mesesData,
          backgroundColor: gradient,
          borderColor: "#667eea",
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: "#667eea",
          pointBorderColor: "#fff",
          pointBorderWidth: 2,
          pointRadius: 5,
          pointHoverRadius: 7,
          pointHoverBackgroundColor: "#764ba2",
          pointHoverBorderColor: "#fff",
          pointHoverBorderWidth: 3,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          backgroundColor: "rgba(0, 0, 0, 0.8)",
          padding: 12,
          titleFont: {
            size: 14,
            weight: "bold",
          },
          bodyFont: {
            size: 13,
          },
          displayColors: false,
          callbacks: {
            label: function (context) {
              return `${context.parsed.y} nuevo${
                context.parsed.y !== 1 ? "s" : ""
              } usuario${context.parsed.y !== 1 ? "s" : ""}`;
            },
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 1,
            font: {
              size: 12,
            },
            color: "#6c757d",
          },
          grid: {
            color: "rgba(0, 0, 0, 0.05)",
            drawBorder: false,
          },
        },
        x: {
          ticks: {
            font: {
              size: 12,
            },
            color: "#6c757d",
          },
          grid: {
            display: false,
            drawBorder: false,
          },
        },
      },
      interaction: {
        intersect: false,
        mode: "index",
      },
    },
  });
});
