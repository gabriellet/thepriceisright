var progress_timer;

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

	    // console.log("returning r " + r);
	    return r; // can't actually return r like this, need a callback function
	}

	function loadChildren(id){
		var children;
		var child_selector = '#children-' + id + ' tr:first';
		var child_id = parseInt(document.getElementsByClassName("child-id")[0].textContent);
		var children_url = "/order/" + id + "/get_children/" + child_id;
		// console.log(children_url);

		// get current order children
	    $.get(children_url, function( children ) {
	    	children = JSON.parse(children);
	    	// console.log(children);
	    	// console.log(children.length);

	    	for(var i=0; i<children.length; i++) {
	    		// console.log(children[i]);
	    		var fields = children[i]['fields'];
	    		var child_class = fields['is_successful'] ? "success" : "danger";
	    		var child_label = fields['is_successful'] ? "SUCCEEDED" : "FAILED";
	    		var date = new Date(fields['time_executed']);
	    		var options = {
    				year: "numeric", month: "short",
    				day: "numeric", hour: "2-digit", minute: "2-digit"
				};
	    		var date_formatted = date.toLocaleTimeString("en-us", options);
	    		date_formatted = date_formatted.replace("AM", "a.m.");
	    		date_formatted = date_formatted.replace("PM", "p.m.");
	    		date_formatted = date_formatted.replace(" ", ". ");
	    		// console.log(typeof date_formatted);
	    		// console.log(date_formatted);
	    		// for (var key in children[i]['fields']){
			    //     var attrName = key;
			    //     console.log("key: " + attrName);
			    //     var attrValue = children[i]['fields'][key];
			    //     console.log("value: " + attrValue);
			    // }
	    		$(child_selector).after(
	    		// console.log(
	    			"<tr class=\"" + child_class + "\"> \
                    	<td> " + date_formatted + " EST \
                    	<td class=\"child-id\"> " + children[i]['pk'] + " \
                    	<td> " + fields['quantity'] + " \
                    	<td> " + child_label + " \
                    	<td> " + fields['price'] + " \
              		</tr>"
              	);
	    	}
	    });
	}

	// progress_type declared on relevant template pages
	if(progress_type == "detail") {
		loadChildren(parent_order_id[0]);
	}

	// if no more in progress orders exist, stop polling
	if (parent_order_id.length == 0) {
		clearInterval(progress_timer);
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
				}
			}	
		}
	}
}

progressBar(); // This will run on page load
progress_timer = setInterval(function(){ progressBar() }, 2000); // get progress every 2 seconds
