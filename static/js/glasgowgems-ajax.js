$(document).ready(function() {
	$("#likes").click(function(){
	    var gemid;
	    gemid = $(this).attr("data-gemid");
		console.log("Clicked like");
	    $.get('/like/', {gem_id: gemid}, function(data){
	        $('#like_count').html(data);
	        $('#likes').hide();
	    });
	});
});

