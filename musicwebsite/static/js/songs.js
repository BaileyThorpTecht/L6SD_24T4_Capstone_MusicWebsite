var selectedSongId = 0;
function updateSongList(innerHtml){
    $("#js-song-container").html(innerHtml);

    if (selectedSongId){
        let btns = $(".js-load-song")
        btns.removeClass("btn-danger");

        let selectedButton = btns.filter(function() {
            return $(this).attr("data-id") == selectedSongId
        });
        selectedButton.addClass("btn-danger");
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

$("#js-song-container").on("click", ".js-update-song", updateSong)

function updateSong(){
  var btn = $(this);
  let data = {};

  //this unfortunately has to interact with the previous javascript of the fretboard
  data["selected-frets"] = JSON.stringify(selectedFretsGlobal);
  //generate a default name in case a new chord needs to be created in the view (unfortunately does this every time because bad coding)
  data["default-name"] = generateDefaultChordName(selectedFretsGlobal);

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