$(document).ready(function()
{
    $('#email').val('');
});

$(document).on('click', "#inviteme", function(event) {
    event.preventDefault();
    var email = $('#email').val().replace(/\s+/g, '');

    if ((email.length == 0) || !(isValidEmail(email))){
        $('#email').val('Not valid!');
        console.log('Subscribe email not valid');
    }
    else{
        var jqxhr = $.post( get_servername_from_url() + 'subscribe/'+ email +'/' );
        $('#email').val('Thank you!');
    }
});