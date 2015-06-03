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

function make_json(trinketId, groupId){
    var result = new Object();

    result.trinketId = trinketId;
    result.groupId = groupId;
    return result;
}

$(function() {
  document.getElementById('trinket-thumbnail').addEventListener('change', handleImage, false);
  });

$(document).on('click', "#save-new-trinket", function(event) {
    event.preventDefault();
    var name = $('#trinket-name').val().replace(/\s+/g, ''),
    trinketId = $('#trinket-id').val().replace(/\s+/g, ''),
    groupId = $('#trinket-group-id').val().replace(/\s+/g, '');
    d = make_json(trinketId, groupId);

    thumbnailFile = $('#trinket-thumbnail')[0].files[0];
    swiffyFile = $('#trinket-swiffy')[0].files[0];
    var fd = new FormData();
    fd.append("thumbnail", thumbnailFile);
    fd.append("swiffy", swiffyFile);

    $.ajax({
                type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(d),
            dataType: 'json',
            url: '/bo/trinket/' + name + '/info/'
            }).done(function( response) {
                log_alert(response);
            });
     $.ajax({
       url: '/bo/trinket/' + name + '/',
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