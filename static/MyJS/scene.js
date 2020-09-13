$(function(){
	$('#cover-spin').show(0)
	var selected_category = null
	$.ajax({
		url: "http://0.0.0.0:5000/generate/scene",
		method: 'POST',
		contentType: 'application/json',
		dataType: 'json',
		data: JSON.stringify({
			'type': 'new',
			'input': localStorage.userInput
		}),
		success: function(response, status, type){
			console.log(response.objects)
			addScene(response.scene)
			add_categories(response.objects)
			$('#cover-spin').hide(0)
			localStorage.objects = JSON.stringify({})
		}
	});
	$(".dropdown-menu").on('click', 'li a', function(){
		$('#cover-spin').show(0)
		// console.log($(this).text())
		selected_category = $(this).text()
		console.log("selected_category: ", selected_category)
		$("#images").empty()
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
	});
	$("#images").on('mouseenter', '.image', function(){
		$(this).find('.frame').css({opacity:0.3});
		$(this).find('.change').css({display:'block'});
	}).on('mouseleave', '.image', function(){
		$(this).find('.frame').css({opacity:1});
		$(this).find('.change').css({display:'none'});
	});
	function addImage(image){
		$("#images").append('<div class="col-12 image"'+
			'style="height:200px; z-index:2;">'+
			'<img class="frame" src="data:image/png;base64, '+image.image+'" '+
			'style="max-width:100%; max-height:100%; margin: 0; '+
			'position: absolute; top: 50%; left: 50%; margin-right: -50%; '+
			'transform: translate(-50%, -50%); padding: 2%;'+
			'" >'+
			'<button class="btn btn-success change" '+
			'style="max-width:100%; max-height:100%; margin: 0;'+
			'position: absolute; top: 50%; left: 50%; margin-right: -50%; '+
			'transform: translate(-50%, -50%); display:none;"'+
			' data-id="'+image.name+'"</button>'+
			'<span class="fa fa-plus" style="color:white"></span></button>'+
		'</div>');
	};
	function addScene(image){
		$("#scene-result").attr("src", "data:image/png;base64,"+image)
		$("#download-scene").attr("href", "data:image/png;base64,"+image)
	};
	function add_categories(objects){
		$('#image-category').empty()
		$.each(objects, function(i, category){
				$('#image-category').append('<li><a class="dropdown-item" id="'+category+'" href="#">'+category+'</a></li>')
			})
	};

	$("#images").on("click", '.change', function(){
		$('#cover-spin').show(0)
		localStorage.type = 'edit'
		objectss = JSON.parse(localStorage.objects)
		objectss[selected_category] = $(this).attr('data-id')
		localStorage.objects = JSON.stringify(objectss)
		console.log(objectss)
		$.ajax({
			url: "http://0.0.0.0:5000/generate/scene",
			method: 'POST',
			contentType: 'application/json',
			dataType: 'json',
			data: JSON.stringify({
				type: localStorage.type,
				input: localStorage.userInput,
				object: JSON.parse(localStorage.objects)
			}),
			success: function(response, status, type){
				console.log(response.objects)
				$("#download-scene").attr("href", "data:image/png;base64,"+response.scene)
				$("#scene-result").attr("src", "data:image/png;base64,"+response.scene)	
				$('#cover-spin').hide(0)
			}
		});
	});
})