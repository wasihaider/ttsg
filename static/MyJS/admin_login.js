$(function (){
	var $username = $('#adminUsername');
	var $password = $('#adminPassword');

	if(localStorage.getItem('auth') == 'true'){
		window.location.replace("http://0.0.0.0:5000/admin-panel")
	}

	$('#adminLogin').on('click', function(){

		var data = {
			username: $username.val(),
			password: $password.val()
		};
		if(data.username == ""){
			
		}
		else if(data.password == ""){
			
		}
		else{
			console.log("data: ", data)
			$.ajax({
				method: 'POST',
				url: 'http://0.0.0.0:5000/admin/login',
				contentType: "application/json",
				dataType: "json",
				data: JSON.stringify(data),
				success: function(response, status_code, type){
					console.log(response);
					localStorage.auth = 'true'
					window.location.replace("http://0.0.0.0:5000/admin-panel");
				},
				error: function(){
					alert('Some Error Occurred')
				}
			});
		}
	});
});