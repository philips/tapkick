$(document).ready(function(){

	$("#submit").click(function(){
	
		console.log($("#number").val());
		window.location = window.location + "/rename/" + $("#number").val();
	
	});
	
});