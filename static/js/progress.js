
var timer;

function progressBar() {

	var remove = false;

	function loadProgress(id){
		var r;
		var newprogress;
		var newstatus;
		var pg;
		var selector = '#progress-' + id;
		var progress_url = "/order/" + id + "/get_progress";
		var status_url = "/order/" + id + "/get_status";

		// get current order status, set progress bar color, etc
		r = false;
		$.get(status_url, function( newstatus ) {
		  switch (newstatus) {
		  	case 'P': //in progress
		  		pg = 'progress-bar progress-bar-success progress-bar-striped active';
		  		break;
		  	case 'C': //completed
		  		pg = 'progress-bar progress-bar-success progress-bar';
		  		r = true;
		  		console.log("you fucker this is r: " + r);
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
	      $(selector).html(newprogress+'%');
	    });

	    console.log("returning r " + r);
	    return r;
	}

	// if no more in progress orders exist, stop polling
	if (parent_order_id.length == 0) {
		clearInterval(timer);
	} else {
		// otherwise update progress bars
		for (i = parent_order_id.length; i > 0; i--) {
			// update progress bar
			remove = loadProgress(parent_order_id[i-1]);
			// if remove flag is set to true
			if (remove == true) {
				if (parent_order_id.length > 0) {
					// remove element
					parent_order_id.splice(i-1, 1);
					// reset flag
					remove = false;
					console.log("inside remove " + remove);
				}
			}	
		}
		console.log("outside loop " + remove);
	}
}

progressBar(); // This will run on page load
timer = setInterval(function(){ progressBar() }, 2000); // get progress every 2 seconds

