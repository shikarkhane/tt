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
    var dir = "Src/themes/base/images/";
    var fileextension = ".png";
    $.ajax({
        //This will retrieve the contents of the folder if the folder is configured as 'browsable'
        url: dir,
        success: function (data) {
            //List all .png file names in the page
            $(data).find("a:contains(" + fileextension + ")").each(function () {
                var filename = this.href.replace(window.location.host, "").replace("http://", "");
                $("body").append("<img src='" + dir + filename + "'>");
            });
        }
    });
}

$(function() {
  document.getElementById('trinket-thumbnail').addEventListener('change', handleImage, false);
  });


$(document).on('click', "#save-multiple-trinkets", function(event) {
    event.preventDefault();
    console.log('directory check');
    $('#thumbnail_directory')
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