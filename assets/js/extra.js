window.onload = function () {
  document.getElementById("show").addEventListener("click", changeBackground);

  function changeBackground() {
    var obj = document.getElementById('top');

    if (obj.className == 'background_initial') {
      obj.className = 'background_space';
    } else {
      obj.className = 'background_initial';
    }

  }

};

window.addEventListener("load", initAudioPlayer);
var audio, playbtn, mutebtn, seek_bar;

function initAudioPlayer() {
  audio = new Audio();
  audio.src = "blog/assets/sound/carl-sagan-pale-blue-dot.mp3";
  audio.loop = true;

  playbtn = document.getElementById("playpausebtn");
  playbtn.addEventListener("click", playPause);

  function playPause() {
    if (audio.paused) {
      audio.play();
    } else {
      audio.pause();
    }
  }
}