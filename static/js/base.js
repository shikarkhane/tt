$('#base-tab-trinket').click(function () {
    event.preventDefault();
    location.replace('/bo/trinket/');
});
$('#base-tab-profile').click(function () {
    event.preventDefault();
    location.replace('/bo/profile/');
});
$('#base-tab-communicate').click(function () {
    event.preventDefault();
    location.replace('/bo/communicate/');
});
$('#base-tab-campaign').click(function () {
    event.preventDefault();
    location.replace('/bo/campaign/');
});
$(function() {
    var index = 0,
        hightlightElement = '#base-tab-trinket';
    if ( window.location.pathname == '/bo/trinket/'){
        index = 1;
        hightlightElement = '#base-tab-trinket';
    }
    else if ( window.location.pathname == '/bo/profile/'){
        index = 2;
        hightlightElement = '#base-tab-profile';
    }
    else if ( window.location.pathname == '/bo/communicate/'){
        index = 3;
        hightlightElement = '#base-tab-communicate';
    }
    else if ( window.location.pathname == '/bo/campaign/'){
        index = 4;
        hightlightElement = '#base-tab-campaign';
    }

    else{
        index = 0;
    }
    $('#tabs-main').tabs({ active: index });
    $(hightlightElement).addClass('ui-btn-active');
});