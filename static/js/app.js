$(function() {
	$('.disabled, a[href="#"]').on('click', function(e) {
		e.preventDefault();
	});

	$('.show_replies a').on('click', function() {
		var text = $(this).text();
		if (text[0] === 'S') text = 'Hide replies';
		else text = 'Show replies';
		$(this).text(text);
		$(this).closest('.show_replies').siblings('.replies').stop().slideToggle();
	});

});
