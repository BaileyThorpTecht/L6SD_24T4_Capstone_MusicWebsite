function updateSongList(innerHtml){
    $("#js-song-container").html(innerHtml);
}
 
$("#js-song-section").on("click", ".js-create-song", createSong)

function createSong(){
  var btn = $(this);
  $.ajax({
    url: btn.attr("data-url"),
    type: 'get',
    dataType: 'json',

    success: function (data) {
      updateSongList(data.html_song_list);
    }
  });

}


$("#js-song-container").on("click", ".js-delete-song", deleteSong)

function deleteSong(){
  var btn = $(this);
  $.ajax({
    url: btn.attr("data-url"),
    type: 'get',
    dataType: 'json',

    success: function (data) {
      updateSongList(data.html_song_list);
    }
  });

}