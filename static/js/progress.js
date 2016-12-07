
var timer;

function progressBar() {
	var remove = false;

	function loadProgress(id){
		var newprogress;
		var newstatus;
		var pg;
		var selector = '#progress-' + id;
		var progress_url = "/order/" + id + "/get_progress";
		var status_url = "/order/" + id + "/get_status";

		// get current order status
		$.get(status_url, function( newstatus ) {
		  switch (newstatus) {
		  	case 'P': //in progress
		  		pg = 'progress-bar progress-bar-success progress-bar-striped active';
		  		break;
		  	case 'C': //completed
		  		pg = 'progress-bar progress-bar-success progress-bar';
		  		break;
		  	case 'F': //failed
		  		pg = 'progress-bar progress-bar-danger progress-bar';
		  		break;
		  	case 'S': //paused
		  		pg = 'progress-bar progress-bar-info progress-bar-striped active';
		  		break;
		  	case 'X': //cancelled
		  		pg = 'progress-bar progress-bar-danger progress-bar';
		  		break;
		  }
		  $(selector).attr('class', pg);
		}); 

		// get current order progress
	    $.get(progress_url, function( newprogress ) {
	      $(selector).attr('aria-valuenow', parseFloat(newprogress)).css('width',parseFloat(newprogress)+'%');
	      if (newprogress == 100.00) {
	        remove = true;
	      }
	      $(selector).html(newprogress+'%');
	    });
	}

	// if no more in progress orders exist, stop polling
	if (parent_order_id.length == 0) {
		clearInterval(timer);
	} else {
		// otherwise update progress bars
		for (i = parent_order_id.length; i > 0; i--) {
			// update progress bar
			loadProgress(parent_order_id[i-1]);
			// if remove flag is set to true
			if (remove == true) {
				if (parent_order_id.length > 0) {
					// remove element
					parent_order_id.splice(i-1, 1);
					// reset flag
					remove = false;
				}
			}	
		}
	}
}

progressBar(); // This will run on page load
timer = setInterval(function(){ progressBar() }, 3000); // get progress every 1 seconds

/* function refreshProgress() {

	for (i = parent_order_id.length; i <= 0; i--) {
		// if remove flag is set to true
		if (remove == true) {
			if (parent_order_id.length >= 0) {
				// remove element
				parent_order_id.splice(0, i);
				// reset flag
				remove == false;
			}
		}
		// if no more in progress orders exist, stop polling
		if (parent_order_id.length == 0) {
			clearInterval(timer);
		} else {
			// otherwise update progress bars
			progressBar(parent_order_id[i]);
			// wrap loop index around to front to keep polling
			if (i == 0) {
				i = parent_order_id.length;
			}
		}
	}

} */

/* parent_order_id.forEach(function(listItem, index){
    loadProgress(listItem);
}); */
