function upload_random_pictures( thumbnailFile){
    var fd = new FormData();
        fd.append("thumbnail", thumbnailFile);

         $.ajax({
           url: '/bo/random-profile-picture/',
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

function read_folders(){
    thumbs = $('#thumbnail_directory')[0].files;
    for (i = 0; i < thumbs.length; i++) {
        t = thumbs[i];
        upload_random_pictures(t);
    }
}

$(document).on('click', "#save-multiple-random_pictures", function(event) {
    event.preventDefault();
    console.log('directory check');
    read_folders();
    });

 function handleImage(evt) {
    var f = evt.target.files[0]; // FileList object

      var reader = new FileReader();

      reader.onload = (function(theFile) {
        return function(e) {
          $('#profile-img-preview').attr('src', e.target.result);
        };
      })(f);

      reader.readAsDataURL(f);
  }
function loadRandomPictures(){
       $.ajax({
                type: 'GET',
            contentType: 'application/json',
            url: '/bo/random-profile-picture/'
            }).done(function( response) {
                console.log(response);

            });
}
$(function() {
    document.getElementById('profile_thumbnail').addEventListener('change', handleImage, false);
    loadRandomPictures();
  });

$(document).on('focusout', "#txtPhoneNumber", function(event) {
    var phn = $('#txtPhoneNumber').val().replace(/\s+/g, '')

    if (phn){
      $.ajax({
                type: 'GET',
            contentType: 'application/json',
            url: '/profile-picture/' + phn + '/'
            }).done(function( response) {
                console.log(response);
                $('#imgCurrentPic').attr("src", response);
            });
    }

});

function upload_profile(phn, thumbnailFile){
    var fd = new FormData();
        fd.append("profile-picture", thumbnailFile);

         $.ajax({
           url: '/profile-picture/' + phn + '/',
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

$(document).on('click', "#saveProfile", function(event) {
    event.preventDefault();
    var phn = $('#txtPhoneNumber').val().replace(/\s+/g, '');

    thumbnailFile = $('#profile_thumbnail')[0].files[0];

    upload_profile(phn, thumbnailFile);
});