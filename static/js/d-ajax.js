function getCookie(name) {
	var matches = document.cookie.match(new RegExp(
		"(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
	));
	return matches ? decodeURIComponent(matches[1]) : undefined;
}

$(document).ready(function() {
	function reload_events() {
		$('.dropdown-button').dropdown({
			inDuration: 300,
			outDuration: 225,
			constrain_width: false, // Does not change width of dropdown to that of the activator
			hover: false, // Activate on hover
			gutter: 0, // Spacing from edge
			belowOrigin: false // Displays dropdown below the button
		});
		$('.favorite_person').click(function() {
			var pk = $(this).data('value');
			var csrftoken = getCookie('csrftoken');
			$.ajax({
				type: "POST",
				url: GLOBAL_VARS.distributorsFavoritePersonUrl,
				data: {
					'pk': pk,
					'csrfmiddlewaretoken': csrftoken
				},
				success: function(content) {
					$("a[data-value='" + pk + "']").toggleClass('blue-text');
				},
				error: function(rs, e) {
					alert(e);
				},
				async: false
			});
		});
		$('.favorite_group').click(function() {
			var pk = $(this).data('value');
			var csrftoken = getCookie('csrftoken');
			$.ajax({
				type: "POST",
				url: GLOBAL_VARS.distributorsFavoriteGroupUrl,
				data: {
					'pk': pk,
					'csrfmiddlewaretoken': csrftoken
				},
				success: function(content) {
					$("a[data-value='" + pk + "']").toggleClass('blue-text');
				},
				error: function(rs, e) {
					alert(e);
				},
				async: false
			});
		});
	}
	var delay = (function() {
		var timer = 0;
		return function(callback, ms) {
			clearTimeout(timer);
			timer = setTimeout(callback, ms);
		};
	})();
	var search = $('#search');
	var data = {};
	if (GLOBAL_VARS.query_id) {
		data.pk = GLOBAL_VARS.query_id;
	};
	$("#search").keyup(function() {
		delay(function() {
			data.query = $("#search").val();
			$.get(GLOBAL_VARS.distributorsSearchDistUrl, data, function(content) {
				$('#distributors').html(content);
				reload_events();
			});
		}, 500);
	});
	$('#all_distributors').click(function() {
		var data = {};
		if (GLOBAL_VARS.query_id) {
			data.pk = GLOBAL_VARS.query_id;
		};
		$.get(GLOBAL_VARS.distributorsAllUrl, data, function(content) {
			$('#distributors').html(content);
			reload_events();
		})
	});
	$('#by_mentions_distributors').click(function() {
		var data = {};
		if (GLOBAL_VARS.query_id) {
			data.pk = GLOBAL_VARS.query_id;
		}
		$.get(GLOBAL_VARS.distributorsByMentionsUrl, data, function(content) {
			$('#distributors').html(content);
			reload_events();
		})
	});
	$('#my_favorite').click(function() {
		var data = {};
		if (GLOBAL_VARS.query_id) {
			data.pk = GLOBAL_VARS.query_id;
		}
		$.get(GLOBAL_VARS.distributorsMyFavoriteUrl, data, function(content) {
			$('#distributors').html(content);
			reload_events();
		})
	});
	$('.favorite_person').click(function() {
		var pk = $(this).data('value');
		var csrftoken = getCookie('csrftoken');
		$.ajax({
			type: "POST",
			url: GLOBAL_VARS.distributorsFavoritePersonUrl,
			data: {
				'pk': pk,
				'csrfmiddlewaretoken': csrftoken
			},
			success: function(content) {
				$("a[data-value='" + pk + "']").toggleClass('blue-text');
			},
			error: function(rs, e) {
				alert(e);
			},
			async: false
		});
	});
	$('.favorite_group').click(function() {
		var pk = $(this).data('value');
		var csrftoken = getCookie('csrftoken');
		$.ajax({
			type: "POST",
			url: GLOBAL_VARS.distributorsFavoriteGroupUrl,
			data: {
				'pk': pk,
				'csrfmiddlewaretoken': csrftoken
			},
			success: function(content) {
				$("a[data-value='" + pk + "']").toggleClass('blue-text');
			},
			error: function(rs, e) {
				alert(e);
			},
			async: false
		});
	});
	$('#update_group').click(function() {
		var csrftoken = getCookie('csrftoken');
		$.ajax({
			type: "POST",
			url: GLOBAL_VARS.distributorsUpdateGroupUrl,
			data: {
				'pk': group_pk,
				'csrfmiddlewaretoken': csrftoken
			},
			dataType: "json",
			success: function(content) {
				if (content['is_closed']) {
					$('#distributor_is_closed').text(content['is_closed']);
				};
				if (content['type']) {
					$('#distributor_type').text(content['type']);
				};
				if (content['members_count']) {
					$('#distributor_members_count').text(content['members_count']);
				};
				if (content['contacts']) {
					$('#distributor_contacts').text(content['contacts']);
				};
				if (content['description']) {
					$('#distributor_description').text(content['description']);
				};
			},
			error: function(rs, e) {
				alert(e);
			},
			async: false
		});
		$('#update_group').replaceWith('<a class="btn disabled">Update Info</a>');
	});
	$('#update_person').click(function() {
		var csrftoken = getCookie('csrftoken');
		$.ajax({
			type: "POST",
			url: GLOBAL_VARS.distributorsUpdatePersonUrl,
			data: {
				'pk': person_pk,
				'csrfmiddlewaretoken': csrftoken
			},
			dataType: "json",
			success: function(content) {
				if (content['bdate']) {
					$('#distributor_bdate').text('Birthday: ' + content['bdate']);
				};
				if (content['address']) {
					$('#distributor_address').text('Address: ' + content['address']);
				};
				if (content['m_number']) {
					$('#distributor_m_number').text('Mobile phone: ' + content['m_number']);
				};
				if (content['photo_url']) {
					$('#distributor_photo').attr('src', content['photo_url']);
				};
			},
			error: function(rs, e) {
				alert(e);
			},
			async: false
		});
		$('#update_person').replaceWith('<a class="btn disabled">Update Info</a>');
	});
});