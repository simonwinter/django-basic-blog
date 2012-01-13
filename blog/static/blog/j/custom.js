jQuery(document).ready(function($) {
	$('.entry_list article').equalHeightColumns();
	
	/* ------ Captions --------- */
	$('img[alt!=""]:not(.greyscale):not(.rollover)').each(function() {
		var im = $(this).clone(),
			container = $('<div class="image_caption">');
		
		container.append(im);
		im.after(
			$('<div class="show">').append('<span>+</span>')
		);
		
		$(this).replaceWith(container);
		$('.show').after($('<div class="caption_text">').append(
			$('<span class="caption">').text(im.attr('alt'))
		));
		$('.caption').after(
			$('<span class="close">').text('-')
		);
		
		$('.show').click(function() {
			$('.caption_text').slideDown();
		});
		
		$('.close').click(function() {
			$('.caption_text').slideUp();
		});
	});
	
	/* ------ Entry list rollovers ----------- */
	$('.entry_list article').hover(function() {
		$(this).find('.rollover').hide().fadeIn(400);
	}, function() {
		$(this).find('.rollover').show().fadeOut(400);
	});
	
	$('.entry_list article').click(function() {
		window.location.href = $(this).find('a:first').attr('href');
	});
	
	/* ------ collapsable Banner. --------------- */
	var header_height = $('header').height(),
		logo_height = $('.title').outerHeight();
	
	$('header .grid_3.tags').after($('<div class="grid_3 omega">').html('<span>-</span>'));
	
	$('header .grid_3.omega').delegate('span', 'click', function() {
		var h = logo_height,
			t = '+',
			that = this;
		
		if($(this).hasClass('clicked')) {
			var h = header_height,
				t = '-';
		};
		
		$('header, header .grid_3:not(.omega)').animate({'height': h}, 500, function() {
			$(that).text(t);
		});
		
		$('header .grid_3 ul').slideToggle();
		$(this).toggleClass('clicked');
	});
	
	/*
$('header .grid_3.omega span.clicked').click(function() {
		var that = this;
		
		$('header, header .grid_3:not(.omega)').animate({'height': header_height}, 500, function() {
			$(that).text('-');
			$('header .grid_3 ul').slideUp();
			return false;
		});
		
		$(this).removeClass('clicked');
	});
*/
	

});