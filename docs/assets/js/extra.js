window.onload = function () {
  document.getElementById("show").addEventListener("click", changeBackground);

  function changeBackground() {
      var obj=document.getElementById('top');
        
      if(obj.className=='home_bg_01'){
        obj.className='home_bg_02';
      }else{
        obj.className='home_bg_01';
      }

  }

};

window.addEventListener("load", initAudioPlayer);
var audio, playbtn, mutebtn, seek_bar;

function initAudioPlayer(){
  audio = new Audio();
  audio.src = "blog/assets/sound/p a l e   b l u e   d o t.mp3";
  audio.loop = true;

  playbtn = document.getElementById("playpausebtn");
  playbtn.addEventListener("click",playPause);

  function playPause(){
    if(audio.paused){
        audio.play();	  
      } else {
        audio.pause();
      }
  }
}