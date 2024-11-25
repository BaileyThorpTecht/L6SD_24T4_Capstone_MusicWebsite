var songInterval;

$(document).on("click", ".js-play-song", getCurrentChords)
//this could be 'loadSongPlayer' if we figure out how to make an actual player
function getCurrentChords() {
    let data = {};
    data["song-id"] = selectedSongId;

    $.ajax({
        url: "/songs/play/",
        type: 'get',
        dataType: 'json',
        data: data,
        success: function (data) {

          let fretsList = JSON.parse(data.frets_list);
          let chords = JSON.parse(data.chords);

          playSong(chords);
          //test();

        }
      });
}

function playSong(chords) {
  $(".js-play-song").css("display","none");
  $(".js-stop-song").css("display","inline");


  //4 beats in a bar, each chord is 1 bar
  let bpm = 40;
  let strumPattern = [true,false,true,false,true,false,true,false]
  let strumsPerChord = strumPattern.length
  let timeBetweenChords = (60/ bpm) * 4 * 1000; //bpm => seconds per beat * 1000 milliseconds per second * 4 beats per bar
  let timeBetweenStrums = timeBetweenChords / strumsPerChord; //8 strums per bar (per chord)

  let chordIndex = 0;
  let strumIndex = 0;
  let chord;


  //playsong
  songInterval = setInterval(function (){

    //if its the start of a new chord, change the chord
    if (strumIndex == 0) {
      chord = chords[chordIndex];
    }
    
    //if it is meant to strum, play
    if (strumPattern[strumIndex]) {
      playAllStrings(chord.frets)
    }

    //increment strum index. when it reaches the end of the bar, reset it and increment chordIndex. If it went through all the chords, stop
    strumIndex++;
    if (strumIndex == strumsPerChord){
      strumIndex = 0;
      chordIndex++;
      if (chordIndex > chords.length){
        stopSong();
      }
    }

  }, timeBetweenStrums)

}

$(document).on("click", ".js-stop-song", stopSong)

function stopSong() {
  clearInterval(songInterval);
  $(".js-play-song").css("display","inline");
  $(".js-stop-song").css("display","none");
}