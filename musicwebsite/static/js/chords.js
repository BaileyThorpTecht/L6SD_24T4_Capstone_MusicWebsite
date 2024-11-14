
$(function () {

    $(".js-create-chord").click(function () {

      var exampleData = {
        "name" : "kk",
        "base" : 6,
        "frets" : [ 0,3,2,0,1,0 ],
        "fingers" : [ 0,3,2,0,1,0 ],
    };

      $.ajax({
        url: '/chords/create/',
        type: 'get',
        dataType: 'json',
        data:  exampleData,
        beforeSend: function () {
          $("#modal-chord").modal("show");
        },
        success: function (data) {
          $("#modal-chord .modal-content").html(data.html_form);
        }
      });
    });
  
  });


$(document).on("submit", ".js-chord-create-form", function () {
    window.alert("clicked");  // <-- This is just a placeholder for now for testing
    var form = $(this);

    $.ajax({
        
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
            window.alert("success");  // <-- This is just a placeholder for now for testing

        if (data.form_is_valid) {
            window.alert("Chord created!");  // <-- This is just a placeholder for now for testing
        }
        else {
            window.alert("Chord invalid");  // <-- This is just a placeholder for now for testing
            $("#modal-chord .modal-content").html(data.html_form);

        }
        }
    });
    return false;
    });
