var swiffy = [];

 function handleSwiffyJson(evt) {
    var f = evt.target.files[0]; // FileList object


      var reader = new FileReader();

      // Closure to capture the file information.
      reader.onload = (function(theFile) {
        return function(e) {
          //console.log(e.target.result);
          swiffy = e.target.result;
          $('#save-new-trinket').removeAttr('disabled');
        };
      })(f);

      reader.readAsText(f);

  }

 function handleImage(evt) {
    var f = evt.target.files[0]; // FileList object

      var reader = new FileReader();

      reader.onload = (function(theFile) {
        return function(e) {
          $('#trinket-img-preview').attr('src', e.target.result);
        };
      })(f);

      reader.readAsDataURL(f);
  }

function make_json( swiffy){
    var result = new Object();
    result.swiffyobject = swiffy;
    return result;
}

$(function() {
  document.getElementById('trinket-swiffy').addEventListener('change', handleSwiffyJson, false);
  document.getElementById('trinket-thumbnail').addEventListener('change', handleImage, false);
  });

$(document).on('click', "#save-new-trinket", function(event) {
    event.preventDefault();
    var name = $('#trinket-name').val().replace(/\s+/g, '');
    d = make_json(swiffy);

    blobFile = $('#trinket-thumbnail')[0].files[0];
    var fd = new FormData();
    fd.append("thumbnail", blobFile);

    $.ajax({
                type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(d),
            dataType: 'json',
            url: '/bo/trinket/swiffy/' + name + '/'
            }).done(function( response) {
                log_alert(response);
            });
     $.ajax({
       url: '/bo/trinket/image/' + name + '/',
       type: "POST",
       data: fd,
       processData: false,
       contentType: false,
       success: function(response) {
           console.log("image uploaded successfully!");
       },
       error: function(jqXHR, textStatus, errorMessage) {
           console.log(errorMessage); // Optional
       }
    });
});