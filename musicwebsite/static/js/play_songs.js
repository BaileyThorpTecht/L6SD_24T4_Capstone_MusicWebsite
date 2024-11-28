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
          if (data.success)
          {
            let chords = JSON.parse(data.chords);
            
            playSong(chords);
          }
          //test();

        }
      });
}

function playSong(chords) {
  $(".js-play-song").css("display","none");
  $(".js-stop-song").css("display","inline");

  //4 beats in a bar, each chord is 1 bar
  let bpm = 80;
  let strumPattern = ["d","","d","","d","","d",""];

  let inputBpm = $(".js-bpm-input").val();
  if (inputBpm) { bpm = inputBpm;}

  let inputPattern = $(".js-pattern-input").val();
  if (inputPattern) {
  
    strumPattern = [];
    for (let b of inputPattern){
      if (b.toLowerCase() == "u") {strumPattern.push("u");} //u for up
      else if (b.toLowerCase() == "d") {strumPattern.push("d");} //d for down
      else if (b == " " || b == "," || b == "." || b == "-" || b == "_" || b == "/") {} //if its a spacer character, ignore it
      else {strumPattern.push("");} //anything else is a rest
    }

  }



  let strumsPerChord = strumPattern.length
  let timeBetweenChords = (60/bpm) * 4 * 1000; //bpm => seconds per beat * 1000 milliseconds per second * 4 beats per bar
  //let timeBetweenStrums = timeBetweenChords / strumsPerChord; //8 strums per bar (per chord)
  let timeBetweenStrums = timeBetweenChords / 8; //assuming 4/4 time sig with 2 notes per beat, or 8 beats per bar

  let chordIndex = 0;
  let strumIndex = 0;
  let chord;
  let frets;

  let tableRows = $(".js-songchord-row");
  let scrollContainer = $("#js-song-scroll");

  // ################### playsong
  songInterval = setInterval(function () {

    $(".js-beat-counter").html(strumIndex + 1);  

    //if its the start of a new chord, change the chord
    if (strumIndex == 0) {
      chord = chords[chordIndex];
      frets = addBaseToFrets(chord.frets, chord.base)

      tableRows.removeClass("table-warning");
      tableRows.slice(chordIndex, chordIndex + 1).addClass("table-warning");

      //auto scroll to show current chord
      scrollContainer.scrollTop(chordIndex * tableRows.height());
    }
    
    //if it is meant to strum, play
    if (strumPattern[strumIndex] == "d") {
      playAllStrings(frets);
    }
    else if (strumPattern[strumIndex] == "u"){
      playAllStringsReverse(frets);
    }

    //increment strum index. when it reaches the end of the bar, reset it and increment chordIndex. If it went through all the chords, stop
    strumIndex++;
    if (strumIndex == strumsPerChord){
      strumIndex = 0;
      chordIndex++;
      if (chordIndex >= chords.length){
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

  $(".js-songchord-row").removeClass("table-warning");
  $(".js-beat-counter").html("...");  

}
