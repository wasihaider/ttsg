$(function(){
	if(localStorage.getItem('auth') != 'true'){
		window.location.replace('http://0.0.0.0:5000/admin-ttsg')
	}
	$('#cover-spin').show(0)
	var $container = $('#images');
	var $dropdown = $('#image-category');
	$.ajax({
		url: 'http://0.0.0.0:5000/get/images',
		method: 'POST',
		contentType: 'application/json',
		dataType: 'json',
		data: JSON.stringify({'type': 'all', 'category': ''}),
		success: function(response, status, type){
			console.log(images)
			$dropdown.append('<li><a class="dropdown-item" id="All" href="#">All</a></li>')
			$.each(response.categories, function(i, category){
				$dropdown.append('<li><a class="dropdown-item" id="'+category+'" href="#">'+category+'</a></li>')
				$('#cover-spin').hide(0)
			})
			$.each(response.images, function(i, image){
				console.log('Iterating')
				addImage(image)
			});
		}
	});
	$container.on('mouseenter', '.image', function(){
		$(this).find('.frame').css({opacity:0.3});
		$(this).find('.remove').css({display:'block'});
	}).on('mouseleave', '.image', function(){
		$(this).find('.frame').css({opacity:1});
		$(this).find('.remove').css({display:'none'});
	});

	$container.delegate('.remove', 'click', function(){
		var $div = $(this).closest('div');

		$.ajax({
			url: 'http://0.0.0.0:5000/delete/image',
			method: 'POST',
			contentType: 'application/json',
			dataType: 'json',
			data: JSON.stringify({name: $(this).attr('data-id')}),
			success: function(response, status, type){
				alert(response.message)
				$div.fadeOut(300, function(){
					$div.remove();
				});
				location.reload()
			},
			error: function(){
				alert('SOME ERROR OCCURED')
			}
		});
	});
	$('#logout-button').click(function(){
		localStorage.auth = 'false';
		window.location.replace("/admin-ttsg")
	});
	$(".dropdown-menu").on('click', 'li a', function(){
		console.log($(this).text())
		$container.empty()
		if($(this).text() == "All"){
			location.reload()
		}
		else{
			$('#cover-spin').show(0)
			$.ajax({
				url: 'http://0.0.0.0:5000/get/images',
				method: 'POST',
				contentType: 'application/json',
				dataType: 'json',
				data: JSON.stringify({
					'type': 'one', 
					'category': $(this).text()
				}),
				success: function(response, status, type){
					$.each(response, function(i, image){
						addImage(image)
					})
					$('#cover-spin').hide(0)
				}
			});
		}
	});

	function addImage(image){
		$container.append('<div class="col-md-4 image"'+
			'style="height:400px; z-index:2">'+
			'<img class="frame" src="data:image/png;base64, '+image.image+'" '+
			'style="max-width:100%; max-height:100%; margin: 0; '+
			'position: absolute; top: 50%; left: 50%; margin-right: -50%; '+
			'transform: translate(-50%, -50%); '+
			'" >'+
			'<button class="btn btn-lg btn-danger remove" '+
			'style="max-width:100%; max-height:100%; margin: 0; '+
			'position: absolute; top: 50%; left: 50%; margin-right: -50%; '+
			'transform: translate(-50%, -50%); display:none;"'+
			' data-id="'+image.name+'"</button>'+
			'<span class="fa fa-trash" style="color:white"></span></button>'+
		'</div>');
	}

	var input = document.querySelector('input[type=file]');
	var b64;
	input.onchange = function () {
		var file = input.files[0],
			reader = new FileReader();

		reader.onloadend = function () {
			// Since it contains the Data URI, we should remove the prefix and keep only Base64 string
			b64 = reader.result.replace(/^data:.+;base64,/, '');
		};

		reader.readAsDataURL(file);
	};

	$("#btn_upload").click(function (){
		// console.log(b64)
		// alert($('#modal-categories').children('option:selected').val())
		$.ajax({
			url: "http://0.0.0.0:5000/add/image",
			method: 'POST',
			contentType: 'application/json',
			dataType: 'json',
			data: JSON.stringify({
				'category': $('#modal-categories').children('option:selected').val(),
				'image': b64
			}),
			success: function(response, status, type){
				location.reload()
			}
		});
	});

});