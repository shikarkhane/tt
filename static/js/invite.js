$(document).ready(function()
{
    $('#email').attr('placeholder','joe@tinktime.com');
});

$(document).on('click', "#inviteme", function(event) {
    event.preventDefault();
    var email = $('#email').val().replace(/\s+/g, '');

    if ((email.length == 0) || !(isValidEmail(email))){
        $('#email').val('');
        $('#email').attr('placeholder', 'not valid!');
        console.log('Subscribe email not valid');
    }
    else{
        var jqxhr = $.post( get_servername_from_url() + 'subscribe/'+ email +'/' );
        $('#email').val('');
        $('#email').attr('placeholder', 'thank you!');
    }
});