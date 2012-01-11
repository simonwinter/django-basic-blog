var $ = django.jQuery,
	empty = false,
	edited = false;

$(document).ready(function() {
	$('#id_excerpt').keypress(function() {
		edited = true;
	});

});

function entryOnInit() {
	var excerpt = $('#id_excerpt');
	var body = $('#id_body_ifr').contents().find('body');
	
	if(excerpt.text() == '' && body.html() != '') {
		empty = true;
		excerpt.html(body.find('p:first').text());
	};
};

function entryEvent(e) {
	if(e.type == 'keyup' && empty && !edited) {
		$('#id_excerpt').html($('#id_body_ifr').contents().find('body').find('p:first').text());
	};

	return true;
}

