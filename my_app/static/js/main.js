// $ is shorthand for jquery
$(document).ready(function() {
  console.log("ready!");


$(".btn").click(function () {
   buttonClick($(this).val());
});

  // on form submission ...
  function buttonClick(button_value) {

    console.log("the form has been submitted")
    console.log("clicked_button type is " + jQuery.type(button_value))

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


    //send the POST data back to the server from the client using AJAX. Anything not put in the data variable is not passed in the post.
    //$.ajax() is a jquery method to create an ajax request
    // http://learn.jquery.com/ajax/jquery-ajax-methods/
    $.ajax({
      type: "POST",
      url: "/",
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

        // finds the dom item with an id="results" - results (the variable) holds our data from the home funciton in view. We can access jsonify data with results.total
        $('#breakeven').html(results.breakeven)
        $('#revenue').html(results.revenue)
        $('#profit').html(results.profit)
        $('#submit_time').html(results.time_submitted)

        // This clears all input fields after the form submission so the user can easily start over.
        //Add the below on clear
        // $('input').val('')
      },
      // close succes function

      error: function(error) {
        console.log("Josh there was an error")
        console.log(error)
      }

    });
	 // close ajax call

  };
// close buttonClick function

});
