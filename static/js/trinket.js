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

function read_folders(){
    thumbs = $('#thumbnail_directory')[0].files;
    swiffys = $('#swiffy_directory')[0].files;
    for (i = 0; i < thumbs.length; i++) {
        console.log(thumbs[i].name);
    }
}

$(function() {
  document.getElementById('trinket-thumbnail').addEventListener('change', handleImage, false);
  });


$(document).on('click', "#save-multiple-trinkets", function(event) {
    event.preventDefault();
    console.log('directory check');
    read_folders();
    });

function upload_trinket(trinketName, thumbnailFile, swiffyFile){
    var fd = new FormData();
        fd.append("thumbnail", thumbnailFile);
        fd.append("swiffy", swiffyFile);

         $.ajax({
           url: '/bo/trinket/' + trinketName + '/',
           type: "POST",
           data: fd,
           processData: false,
           contentType: false,
           success: function(response) {
               console.log(response);
           },
           error: function(jqXHR, textStatus, errorMessage) {
               console.log(errorMessage); // Optional
           }
        });
}

$(document).on('click', "#save-new-trinket", function(event) {
    event.preventDefault();
    var name = $('#trinket-name').val().replace(/\s+/g, '');

    thumbnailFile = $('#trinket-thumbnail')[0].files[0];
    swiffyFile = $('#trinket-swiffy')[0].files[0];

    upload_trinket(name, thumbnailFile, swiffyFile);
});


$(document).on('click', "button.deactivate", function(event) {
    event.preventDefault();
    var name = this.nextSibling.nextSibling.innerText;
    $.ajax({
                type: 'POST',
            contentType: 'application/json',
            url: '/bo/trinket/' + name + '/active/0/'
            }).done(function( response) {
                console.log(response);
            });

});

$(document).on('click', "button.activate", function(event) {
    event.preventDefault();
    var name = this.nextSibling.nextSibling.innerText;
    $.ajax({
                type: 'POST',
            contentType: 'application/json',
            url: '/bo/trinket/' + name + '/active/1/'
            }).done(function( response) {
                console.log(response);
            });

});