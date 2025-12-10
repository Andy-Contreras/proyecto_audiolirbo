document.addEventListener("DOMContentLoaded", () => {

  // Elementos
  const audio = document.getElementById("player");
  const playBTN = document.getElementById("playBtn");
  const progressBar = document.getElementById("progreso-bar");
  const tiempoActual = document.getElementById("currentTime");
  const tiempoTotal = document.getElementById("durationTime");
  const rewind = document.getElementById("rewindBtn");
  const forward = document.getElementById("forwardBtn");

  // Íconos
  const iconPlay = `
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
      viewBox="0 0 24 24" fill="currentColor">
      <path d="M6 4v16l12-8z" />
    </svg>
  `;

  const iconPause = `
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
      viewBox="0 0 24 24" fill="none" stroke="currentColor"
      stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M6 5h4v14H6z" />
      <path d="M14 5h4v14h-4z" />
    </svg>
  `;

  // Formato mm:ss
  function formatTime(seconds) {
    if (isNaN(seconds)) return "00:00";
    const min = Math.floor(seconds / 60);
    const sec = Math.floor(seconds % 60);
    return `${min}:${sec < 10 ? "0" + sec : sec}`;
  }

  // Estado inicial
  playBTN.disabled = true;
  progressBar.value = 0;
  tiempoActual.textContent = "00:00";
  tiempoTotal.textContent = "00:00";

  // ✅ Metadata cargada
  audio.addEventListener("loadedmetadata", () => {
    tiempoTotal.textContent = formatTime(audio.duration);
  });

  // ✅ Audio listo para reproducir
  audio.addEventListener("canplay", () => {
    playBTN.disabled = false;
  });

  // Play / Pause
  playBTN.addEventListener("click", () => {
    if (audio.paused) {
      audio.play()
        .then(() => {
          playBTN.innerHTML = iconPause;
        })
        .catch(err => {
          console.error("Error al reproducir:", err);
        });
    } else {
      audio.pause();
      playBTN.innerHTML = iconPlay;
    }
  });

  // Actualizar barra y tiempo
  audio.addEventListener("timeupdate", () => {
    if (!isNaN(audio.duration)) {
      progressBar.value = (audio.currentTime / audio.duration) * 100;
      tiempoActual.textContent = formatTime(audio.currentTime);
    }
  });

  // Mover audio usando la barra
  progressBar.addEventListener("input", () => {
    if (!isNaN(audio.duration)) {
      audio.currentTime = (progressBar.value / 100) * audio.duration;
    }
  });

  // Retroceder 10s
  rewind.addEventListener("click", () => {
    audio.currentTime = Math.max(0, audio.currentTime - 10);
  });

  // Avanzar 10s
  forward.addEventListener("click", () => {
    audio.currentTime = Math.min(audio.duration, audio.currentTime + 10);
  });

  // Al finalizar
  audio.addEventListener("ended", () => {
    audio.currentTime = 0;
    progressBar.value = 0;
    playBTN.innerHTML = iconPlay;
  });

});
