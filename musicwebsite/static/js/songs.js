var selectedSongId = 4;

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

function doSongAjaxRequest(btn){
    $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        data: {"song-id" : selectedSongId},
    
        success: function (data) {
          updateSongList(data.html_song_list);
        }
      });
}


$("#js-song-section").on("click", ".js-create-song", createSong)

function createSong(){
  var btn = $(this);

  doSongAjaxRequest(btn);

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

