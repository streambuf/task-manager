$.ajaxSetup({ 
	 beforeSend: function(xhr, settings) {
		 function getCookie(name) {
			 var cookieValue = null;
			 if (document.cookie && document.cookie != '') {
				 var cookies = document.cookie.split(';');
				 for (var i = 0; i < cookies.length; i++) {
					 var cookie = jQuery.trim(cookies[i]);
					 // Does this cookie string begin with the name we want?
				 if (cookie.substring(0, name.length + 1) == (name + '=')) {
					 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					 break;
				 }
			 }
		 }
		 return cookieValue;
		 }
		 if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
			 // Only send the token to relative URLs i.e. locally.
			 xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
		 }
	 } 
});

$(document).ready(function() {
	var TIME_HIDE = 2000;

	var sendPost = function (url, data) {
	    var self = this;
	    $.ajax({
	        url: url,
	        method: 'POST',
	        data: data,
	        dataType: 'json'
	    }).done(function(data) {
	        if (data.status == 'ok') {
	        	if (data.messageType != undefined) {
	        		$.event.trigger({
						type: data.messageType,
						record: data.record,
					});
	        	}
	        } else {
	            showErrors(data.record);
	        }
	    }).fail(function(data) {
	        alert('Connection error, please try again later');
	    });
	}

	$(document).on('click', '.delete-task', function(){
		var button = $(this);
		var tid = button.data('tid');
		button.closest('li').slideUp(TIME_HIDE);
		var data = {'tid': tid}
		sendPost('/tasks/delete/', data);

	});

	$(document).on('click', 'input:checkbox', function(){
		var checkbox = $(this);
		var tid = checkbox.data('tid');
		var li = checkbox.closest('li');
		var checked = false
		if (checkbox.prop('checked')) {
			li.addClass('item-success');
			li.find('.task-title').addClass('line-through');
			checked = true
		} else {
			li.removeClass('item-success');
			li.find('.task-title').removeClass('line-through');
		}
		var data = {'tid': tid, 'checked': checked}
		sendPost('/tasks/complete/', data);
	});

	$('form').submit(function(event){
		event.preventDefault();
		var form = $(this);
		var data = form.serialize();
		var url = form.attr('action');
		sendPost(url, data);				
	});

	$(document).on('addTask', addTask);

	function showErrors(data) {
		if (data.title) {
			$('.error-title').html(data.title).slideDown().delay(3000).slideUp();
		}
		if (data.expiration_date) {
			$('.error-edate').html(data.expiration_date).slideDown().delay(3000).slideUp();
		}
	}

	function addTask(e) {
		$('.list-group').append('<li class="list-group-item row">' +
		      '<div class="col-lg-1 list-group__checkbox">' +
		      '<input type="checkbox" data-tid = "' + e.record.id + '">' +
		      '</div>' +
		      '<div class="col-lg-6">' +
		      '<p class="task-title">' + e.record.title + '</p>' +
		      '</div>' +
		      '<div class="col-lg-4">' +
        	  '<p>' + e.record.edate + '</p>' +
      		  '</div>' +
		      '<div class="col-lg-1">'+
		      '<button class="btn btn-small btn-danger delete-task" data-tid = "' + 
		      e.record.id + '">'+
		      '<i class="icon-remove icon-white">X</i>'+
		      '</button>' +
		      '</div>'+
		      '</li>');		
	}
});