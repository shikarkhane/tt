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
        t = thumbs[i];
        if (t.type == 'image/png'){
            for( var s in swiffys){
                var q = swiffys[s];
                if( q.type == 'text/html'){
                    if( t.name.split('.')[0] == q.name.split('.')[0]){
                        console.log(t.name);
                        upload_trinket(t.name.split('.')[0], t, q);
                    }
                }
            }
        }
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
    var name = $(this).siblings('span.trinketname')[0].innerText;
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
    var name = $(this).attr('data-trinketname');
    $.ajax({
                type: 'POST',
            contentType: 'application/json',
            url: '/bo/trinket/' + name + '/active/1/'
            }).done(function( response) {
                console.log(response);
            });

});
$(document).on('click', "button.preview", function(event) {
    event.preventDefault();
    var name = $(this).attr('data-trinketname'),
    swiffyurl = $(this).attr('data-swiffyurl');
    createPopup(name, swiffyurl);

    window.setTimeout(function(){document.getElementById('tinkcontainer-'+name).contentWindow.tt_start_animation();}, 2000);
});

function createPopup(tname, sUrl){

    // close button
    var closeBtn = $('<a href="#" data-rel="back" data-role="button" data-theme="a" data-icon="delete" data-iconpos="notext" class="ui-btn-right">Close</a>').button();

    // text you get from Ajax
    var content = '<iframe id="tinkcontainer-'+tname+'"  src="'+sUrl+'"></iframe>';

    // Popup body - set width is optional - append button and Ajax msg
    var popup = $("<div/>", {
        "data-role": "popup"
    }).css({
        "width": $(window).width() / 1.5 + "px",
        "height": $(window).height() / 1.5 + "px"
    }).append(closeBtn).append(content);

    // Append it to active page
    $(".ui-page-active").append(popup);

    // Create it and add listener to delete it once it's closed
    // open it
    $("[data-role=popup]").on("popupafterclose", function () {
        $(this).remove();
    }).on("popupafteropen", function () {
        $(this).popup("reposition", {
            "positionTo": "window"
            //x: 150,
            //y: 200
        });
    }).popup({
        "dismissible": false,
            "history": false,
            "theme": "d",
            "overlayTheme": "a"
    }).popup("open");


}