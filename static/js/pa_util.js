
$(document).on('click', "#sendbtn", function(event) {
    event.preventDefault();
    var o = new Object();
    o.from_user = $('#from').val().replace(/\s+/g, '');
    o.to_user = $('#to').val().replace(/\s+/g, '');
    o.seconds_sent = $('#seconds').val().replace(/\s+/g, '');
    o.trinket_id = $('#trinketid').val().replace(/\s+/g, '');
    o.text = $('#text').val().replace(/\s+/g, '');
    o.send_timestamp = (new Date()).valueOf();
    var url = get_servername_from_url() + 'message-queue/';
    $.ajax({
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(o),
                dataType: 'json',
                url: url
            }).success(function( response) {
                $('#senddiv').removeClass('alert-info');
                $('#senddiv').addClass('alert-success');
            })
            .error(function( response) {
                $('#senddiv').removeClass('alert-info');
                $('#senddiv').addClass('alert-danger');
            });
});

$(document).on('click', "#getfeed", function(event) {
    event.preventDefault();
    var o = new Object();
    var to_user = $('#to').val().replace(/\s+/g, '');

    var url = get_servername_from_url() + 'pre-alpha/feed/8161/' + to_user + '/';
    window.location = url;
});