$(function(){
	$("#generate").click(function(){
		if($("#text-input").val() == ""){
			alert('Please enter some input!!')
		}
		else{
			localStorage.userInput = $("#text-input").val()
			localStorage.type = "new"
			window.location.replace("/ttsg/scene")
		}
	});
});