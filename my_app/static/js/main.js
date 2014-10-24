// $ is shorthand for jquery
$(document).ready(function() {
  console.log("ready!");

  // on form submission ...
  $('form').on('submit', function() {

    console.log("the form has been submitted");

    // grab values
    title_form = $('input[name="title"]').val();
    rent_form = $('input[name="rent"]').val();
    console.log(title_form, rent_form)

    //sends the POST data back to the server from the client using AJAX
    $.ajax({
      type: "POST",
      url: "/",
      data : { 'form_title': title_form, 'form_rent': rent_form },
      success: function(results) {
        console.log(results);

        // finds the dom item with an id="results" - results (the variable) holds our data from the home funciton in view. We can access jsonify data with results.total
        $('#results').html(results.total)
        $('input').val('')
      },
      error: function(error) {
        console.log(error)
      }
    });

  });

});
