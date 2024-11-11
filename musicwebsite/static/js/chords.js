
$(function () {

    $(".js-create-chord").click(function () {
      $.ajax({
        url: '/chords/create/',
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $("#modal-chord").modal("show");
        },
        success: function (data) {
          $("#modal-chord .modal-content").html(data.html_form);
        }
      });
    });
  
  });