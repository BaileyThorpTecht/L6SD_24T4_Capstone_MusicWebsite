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

}

$("#js-song-section").on("click", ".js-load-song", loadSong)

function loadSong(){
  var btn = $(this);
  selectedSongId = btn.attr("data-id");

  doSongAjaxRequest(btn);

}

$("#js-song-container").on("click", ".js-delete-song", deleteSong)

function deleteSong(){
  var btn = $(this);
  if(selectedSongId == btn.attr("data.id")) { selectedSongId = 0;}

  doSongAjaxRequest(btn);

}

