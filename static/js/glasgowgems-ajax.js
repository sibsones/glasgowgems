$(document).ready(function() {
	$("#likes").click(function(){
	    var gemid;
	    gemid = $(this).attr("data-gemid");
	    $.get('/like/', {gem_id: gemid}, function(data){
	        $('#like_count').html(data);
	        $('#likes').hide();
	    });
	});
    
    $("#comments").click(function(){
        var gemid;
        gemid = $(this).attr("data-gemid");
        var user;
        $("#myModal").modal();
        
            // process the form
            $('form').submit(function(event) {
            $('.form-group').removeClass('has-error'); // remove the error class
            $('.help-block').remove(); // remove the error text
            console.log("form calisdi");
            
            // get the form data
            // there are many ways to get this data using jQuery (you can use the class or id also)
            var comment_text = document.getElementById("comment").value;
            var formData = {"comment_text": comment_text, "gem_id": gemid}
            console.log(formData);

            // process the form
            $.ajax({
                type 		: 'POST', // define the type of HTTP verb we want to use (POST for our form)
                url 		: '/create_comment/', // the url where we want to POST
                data 		: formData, // our data object
                dataType 	: 'json', // what type of data do we expect back from the server
                encode 		: true
            })
            // using the done promise callback
			.done(function(data) {

			// log data to the console so we can see
			console.log(data); 

			// ALL GOOD! just show the success message!
			$('form').append('<div class="alert alert-success">' + data.message + '</div>');
			})

			// using the fail promise callback
			.fail(function(data) {

				// show any errors
				// best to remove for production
				console.log(data);
			});

		// stop the form from submitting the normal way and refreshing the page
		event.preventDefault();
        });
    });
    
    $("#report").click( function(event) {
        var gemid;
	    gemid = $(this).attr("data-gemid");
	    $.get('/report/', {gem_id: gemid}, function(data){
	        $('#report').hide();
	    });
		alert("Thank you.");
	});
});

