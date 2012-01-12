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
			//$(this).slideUp();
			$('.caption_text').slideDown();
		});
		
		$('.close').click(function() {
			$('.caption_text').slideUp();
			//$('.show').slideDown();
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
});