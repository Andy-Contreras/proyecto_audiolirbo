const audio = document.getElementById("player");
const playBTN = document.getElementById("playBtn");
const progressBar = document.getElementById("progreso-bar");
const tiempoAtras = document.getElementById("currentTime");
const tiempoDelan = document.getElementById("durationTime");
const rewind = document.getElementById("rewindBtn");
const forward = document.getElementById("forwardBtn");
const finish = document.getElementById("finished");
// icono para los botones
const iconPlay = `
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor"
    class="icon icon-tabler icons-tabler-filled icon-tabler-player-play">
    <path stroke="none" d="M0 0h24v24H0z" fill="none" />
    <path d="M6 4v16a1 1 0 0 0 1.524 .852l13 -8a1 1 0 0 0 0 -1.704l-13 -8a1 1 0 0 0 -1.524 .852z" />
</svg>
`;
const iconPause = `
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-player-pause">
  <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
  <path d="M6 5m0 1a1 1 0 0 1 1 -1h2a1 1 0 0 1 1 1v12a1 1 0 0 1 -1 1h-2a1 1 0 0 1 -1 -1z" />
  <path d="M14 5m0 1a1 1 0 0 1 1 -1h2a1 1 0 0 1 1 1v12a1 1 0 0 1 -1 1h-2a1 1 0 0 1 -1 -1z" />
</svg>
`;

// configuracion para el boton de play/pause

playBTN.addEventListener("click", () => {
  // si el audio esta en pause, devuelve un estado de true
  if (audio.paused) {
    // empieza a reproducir
    audio.play();
    console.log("Estoy reproduciendo");
    playBTN.innerHTML = iconPause;
  }
  // si no es true y el estado es false, entonces se puede pausar
  else {
    audio.pause();
    playBTN.innerHTML = iconPlay;
  }
});


audio.addEventListener("ended", () => {
  playBTN.innerHTML = iconPlay;
});


// Ver el progreso
// 1. Configuramos el formtTime
function formatTime(seconds) {
  if (isNaN(seconds)) {
    return "00:00";
  }
  const min = Math.floor(seconds / 60);
  const sec = Math.floor(seconds % 60);
  return `${min}:${sec < 10 ? "0" + sec : sec}`;
}

audio.addEventListener("timeupdate", () => {
  progressBar.value = (audio.currentTime / audio.duration) * 100;
  // console.log("Tiempo actual:", audio.currentTime);
  //console.log("Tiempo actual:", audio.duration);
  tiempoAtras.textContent = formatTime(audio.currentTime);
  tiempoDelan.textContent = formatTime(audio.duration);
});

// Mover el audio en la barra
progressBar.addEventListener("input", () => {
  audio.currentTime = (progressBar.value / 100) * audio.duration;
});

// Botones adelante

rewind.addEventListener("click", () => {
  audio.currentTime = Math.max(0, audio.currentTime - 10);
});

forward.addEventListener("click", () => {
  audio.currentTime = Math.min(audio.duration, audio.currentTime + 10);
});

