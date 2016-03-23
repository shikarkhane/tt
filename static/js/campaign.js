
function save_campaign(network, name, url, imgurl){

    var o = new Object();
    o.network = network;
    o.name = name;
    o.url = url;
    o.imgurl = imgurl;
    var url =  '/bo/campaign/';
    $.ajax({
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(o),
                dataType: 'json',
                url: url
            }).done(function( response) {
                console.log('campaign successfully saved');
            })
            ;

}

$(document).on('click', "#savetwitter", function(event) {
    event.preventDefault();

    var name = $('#txtCampaignNameTwitter').val().replace(/\s+/g, '');
    var url = $('#txtCurrentUrlTwitter').val().replace(/\s+/g, '');
    var imgurl = $('#txtCurrentPicTwitter').val().replace(/\s+/g, '');

    save_campaign('twitter', name, url, imgurl);
});
$(document).on('click', "#savefb", function(event) {
    event.preventDefault();

    var name = $('#txtCampaignNameFb').val().replace(/\s+/g, '');
    var url = $('#txtCurrentUrlFb').val().replace(/\s+/g, '');
    var imgurl = $('#txtCurrentPicFb').val().replace(/\s+/g, '');

    save_campaign('facebook', name, url, imgurl);
});
$(document).on('click', "#saveinsta", function(event) {
    event.preventDefault();

    var name = $('#txtCampaignNameInsta').val().replace(/\s+/g, '');
    var url = $('#txtCurrentUrlInsta').val().replace(/\s+/g, '');
    var imgurl = $('#txtCurrentPicInsta').val().replace(/\s+/g, '');

    save_campaign('instagram', name, url, imgurl);
});