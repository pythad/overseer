$(document).ready(function() {
    $(".alert-message").delay(4000).fadeOut("fast");
	$(".button-collapse").sideNav();
	$(".dropdown-button").dropdown({
		inDuration: 300,
		outDuration: 225,
		constrain_width: false, // Does not change width of dropdown to that of the activator
		hover: false, // Activate on hover
		gutter: 0, // Spacing from edge
		belowOrigin: false // Displays dropdown below the button
	});
})