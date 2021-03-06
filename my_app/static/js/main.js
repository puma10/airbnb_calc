// $ is shorthand for jquery
$(document).ready(function() {
	console.log("ready!");

	var form_state = "blank"
	$('#save').hide()
	$('#reset').hide()
	$('#calculate').show()

	$('.results').hide();
	$('#breakeven').hide();
	$('#revenue').hide();
   	$('#profit').hide();
    $('#submit_time').hide();
    $('#suggest').hide();


  // on form submission ...
  function buttonClick(button_value) {

  	if (button_value == "calculate") {
  		console.log("we have calculated the form")
  		$('#calculate').show();
        $('#save').show();
  		$('#reset').show();


  		// grab values from the form
	    title_form = $('input[name="title"]').val();
	    rent_form = $('input[name="rent"]').val();
	    water_form = $('input[name="water"]').val();
	    sewer_form = $('input[name="sewer"]').val();
	    garbage_form = $('input[name="garbage"]').val();
	    electric_form = $('input[name="electric"]').val();
	    cable_form = $('input[name="cable"]').val();
	    maid_form = $('input[name="maid_service"]').val();
	    hotel_tax_form = $('input[name="hotel_tax"]').val();
	    occupancy_form = $('input[name="occupancy"]').val();
	    daily_price_form = $('input[name="daily_price"]').val();




        submit_time = new Date($.now());

	    console.log(title_form,
	                rent_form,
	                water_form,
	                sewer_form,
	                garbage_form,
	                electric_form,
	                cable_form,
	                maid_form,
	                hotel_tax_form,
	                occupancy_form,
	                daily_price_form,
	                submit_time)

	    $.ajax({
		    type: "POST",
		    url: "/calc",
		    data : {
		      	'form_title': title_form,
		        'form_rent': rent_form,
		        'water_form': water_form,
		        'sewer_form': sewer_form,
		        'garbage_form': garbage_form,
		        'electric_form': electric_form,
		        'cable_form': cable_form,
		        'maid_form': maid_form,
		        'hotel_tax_form': hotel_tax_form,
		        'occupancy_form': occupancy_form,
		        'daily_price_form': daily_price_form,
		        'submit_time': submit_time,
		        'clicked_button': button_value
		    },

      // if the ajax connection was succesful we pass the data back in a json object named results
      		success: function(results) {
	        	console.log(results);
                // scroll to the top of the window after form submission
                window.scrollTo(0, 0);
		        // finds the dom item with an id="results" - results (the variable) holds our data from the home funciton in view. We can access jsonify data with results.total
		        $('.results').show();
		        $('#breakeven').show();
		    	$('#revenue').show();
	        	$('#profit').show();
	        	$('#submit_time').show();

		        $('#breakeven').html(results.breakeven)
		        $('#revenue').html(results.revenue)
		        $('#profit').html(results.profit)
		        $('#submit_time').html(results.time_submitted)

		        if (results.profit < 0){
		        	$("#suggest_output").html("<b>Bummer</b>, you're not profitable yet. Adjust your nightly rate, increase your average occupancy or find a way to decrease costs.");
		        	$('#suggest').show();
		        	$( "#suggest" ).removeClass( "alert alert-success" );
		        	$( "#suggest" ).addClass( "alert alert-danger" );
		        	// $("#suggest_output").css( "background-color", "#a50404" );
		        	// $("#suggest_output").css( "background-color", "red" );
		        	$("div.results").css( "background-color", "rgb(238, 144, 144" );
		        	$(".output").css( "color", "#9E0505" );



		        }else{
		        	$("#suggest_output").html("<b>Cha-ching</b> Given your calculations your unit is profitable! Checkout these resources to help you get started with Airbnb!");
		        	$( "#suggest" ).removeClass( "alert alert-danger" );
		        	$( "#suggest" ).addClass( "alert alert-success" );

		        	$("div.results").css( "background-color", "lightgreen" );
		        	$(".output").css( "color", "rgb(89, 89, 89)" );
		        	$('#suggest').show();
		        }
      		}, // close success function


      		error: function(error) {
		        console.log("there was an ajax error")
		        console.log(error)
      		}

    	}); // close ajax call

	} // close if statement


  	if (button_value == "save") {
  		console.log("we have saved the form")

        title_form = $('input[name="title"]').val();
	    rent_form = $('input[name="rent"]').val();
	    water_form = $('input[name="water"]').val();
	    sewer_form = $('input[name="sewer"]').val();
	    garbage_form = $('input[name="garbage"]').val();
	    electric_form = $('input[name="electric"]').val();
	    cable_form = $('input[name="cable"]').val();
	    maid_form = $('input[name="maid_service"]').val();
	    hotel_tax_form = $('input[name="hotel_tax"]').val();

	    occupancy_form = $('input[name="occupancy"]').val();
	    daily_price_form = $('input[name="daily_price"]').val();

	    submit_time = new Date($.now());

	    console.log(title_form,
	                rent_form,
	                water_form,
	                sewer_form,
	                garbage_form,
	                electric_form,
	                cable_form,
	                maid_form,
	                hotel_tax_form,
	                occupancy_form,
	                daily_price_form,
	                submit_time)

	    $.ajax({
	      	type: "POST",
	      	url: "/calc",
	     	data : {
		      	'form_title': title_form,
		        'form_rent': rent_form,
		        'water_form': water_form,
		        'sewer_form': sewer_form,
		        'garbage_form': garbage_form,
		        'electric_form': electric_form,
		        'cable_form': cable_form,
		        'maid_form': maid_form,
		        'hotel_tax_form': hotel_tax_form,
		        'occupancy_form': occupancy_form,
		        'daily_price_form': daily_price_form,
		        'submit_time': submit_time,
		        'clicked_button': button_value
	    	},

			success: function(results) {
        		console.log("ajax request/response succesful")
      		},

      		// close success function
      		error: function(error) {
		        console.log("there was an ajax error")
		        console.log(error)
      		}

    	}); // close ajax call

    	$('#save').hide();
  		$('#reset').hide();
        $('#calculate').show();

        $('.results').hide();
        $('#suggest').hide();

        // This clears all input fields after the form submission so the user can easily start over.
        //Add the below on clear
        $('input').val('')

    } // close if statement

    if (button_value == "reset") {
  		console.log("we have reset the form")
  		$('#save').hide();
  		$('#reset').hide();
        $('#calculate').show();

        $('.results').hide();
        $('#suggest').hide();
  	} // close if statement


    console.log("the form has been submitted")
    // console.log("clicked_button type is " + jQuery.type(button_value))
    console.log("clicked_button type is " + button_value)




    //send the POST data back to the server from the client using AJAX. Anything not put in the data variable is not passed in the post.
    //$.ajax() is a jquery method to create an ajax request
    // http://learn.jquery.com/ajax/jquery-ajax-methods/


  };
// close buttonClick function


	$(".btn").click(function () {
	   buttonClick($(this).val());


	});


});

