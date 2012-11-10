$(function() {
	$('.disabled, a[href="#"]').on('click', function(e) {
		e.preventDefault();
	});

	$('.show_replies a').on('click', function() {
		$(this).closest('.show_replies').hide().siblings('.replies').show();
	});

});
