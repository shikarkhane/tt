	$(function() {
        var referrer =  get_url_value('next');
        if (!referrer){referrer = '/'};
        $.cookie('mypagebeforelogin', referrer, { path: '/'});


        if (!($.cookie('MyLat'))){
            $('#no-coord-warning').removeClass('hide');
        };

	});

	$(document).on('click', "#btngoogle", function(event){
		event.preventDefault();
		window.location.replace("/auth");
	});
