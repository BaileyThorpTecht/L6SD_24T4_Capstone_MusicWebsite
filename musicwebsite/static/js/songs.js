
var selectedSongId = 0;
function updateSongList(innerHtml){
    //update list of songchords
    $("#js-song-container").html(innerHtml);

    //highlight selected song
    if (selectedSongId){
        let btns = $(".js-load-song")
        btns.removeClass("table-warning");

        let selectedButton = btns.filter(function() {
            return $(this).attr("data-id") == selectedSongId
        });
        selectedButton.addClass("table-warning");
        
        //disable/enable play button if no song selected
        $(".js-play-song").removeClass("disabled");
        $(".js-update-song").removeClass("disabled");
        $(".js-add-chord-alert").addClass("d-none");
      }else{
        $(".js-play-song").addClass("disabled");
        $(".js-update-song").addClass("disabled");
        $(".js-add-chord-alert").removeClass("d-none");



      }
}

function doSongAjaxRequest(btn, data = {}){
    data["song-id"] = selectedSongId;

    $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        data: data,
    
        success: function (data) {
          updateSongList(data.html_song_list);

          //this is put here so it shows a custom chord being created when a new chord is added to a song. it must be here in 'success' so it happens in the right order, but it happens more often than it needs to. but its fine
          reloadCustomChords();

        }
      });
}


$("#js-song-section").on("click", ".js-create-song", createSong)

function createSong(){
  var btn = $(this);
  let data = {};

  let inputSongName = $("#js-song-name-input").val();

  //if  is not null or whitespace
  if (inputSongName || inputSongName.trim()) {
    data["song-name"] = inputSongName;
  } else {
    data["song-name"] = "New Song"
  }
  
  $("#js-song-name-input").val("");

  doSongAjaxRequest(btn, data);

  //refresh chord list

}

$("#js-song-section").on("click", ".js-load-song", loadSong)
$("#chord-table").on("click", ".js-load-song", loadSong)

function loadSong(){
  var btn = $(this);
  selectedSongId = btn.attr("data-id");

  doSongAjaxRequest(btn);

}

$(document).on( "mouseenter", ".js-load-song", hoverColor ).on( "mouseleave", ".js-load-song", hoverUncolor);

function hoverColor(){
  $(this).addClass("table-secondary");
}

function hoverUncolor(){
  $(this).removeClass("table-secondary");
}




$(document).on("click", ".js-update-song", updateSong)

function updateSong(){
  var btn = $(this);
  let data = {};

  //this unfortunately has to interact with the previous javascript of the fretboard
  data["selected-frets"] = JSON.stringify(selectedFretsGlobal);
  //generate a default name in case a new chord needs to be created in the view (unfortunately does this every time because bad coding)
  data["default-name"] = generateDefaultChordName(selectedFretsGlobal);

  doSongAjaxRequest(btn, data);
}

$("#chord-table").on("click", ".js-add-chord-to-song", updateSongFromChordList)

function updateSongFromChordList() {
  var btn = $(this);
  let data = {};

  doSongAjaxRequest(btn, data);
}


$("#js-song-container").on("click", ".js-delete-song", deleteSong)

function deleteSong(){
  var btn = $(this);
  let data = {};

  data["delete-id"] = selectedSongId;
  selectedSongId = 0;

  doSongAjaxRequest(btn, data);
}


$("#js-song-container").on("click", ".js-remove-song", removeSong)

function removeSong(){
  var btn = $(this);
  let data = {};

  doSongAjaxRequest(btn, data);
}







//I need to load the songs from outside this neat js file, so i have to copy and paste to make this messy function
function doSongLoadRequestOneOff(){
    let data = {};
    data["song-id"] = selectedSongId;
    var btn = $(".js-load-song");

    $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        data: data,
    
        success: function (data) {
          updateSongList(data.html_song_list);
        }
      }); 
}
