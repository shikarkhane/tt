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

function make_json( swiffy){
    var result = new Object();
    result.swiffyobject = swiffy;
    return result;
}

$(function() {

  document.getElementById('trinket-swiffy').addEventListener('change', handleSwiffyJson, false);
  });

$(document).on('click', "#save-new-trinket", function(event) {
    event.preventDefault();
    var name = $('#trinket-name').val().replace(/\s+/g, '');
    d = make_json(swiffy);
    $.ajax({
                type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(d),
            dataType: 'json',
            url: '/bo/trinket/' + name + '/'
            }).done(function( response) {
                log_alert(response);
            });
});