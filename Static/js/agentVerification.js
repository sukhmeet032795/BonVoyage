window.onload = function (){
	main()
}

var startFunc= function(){

	$.ajax({
		url: '/imageProcessing',
		type: 'GET',

		data: {
				'imageName': $($('table tr td a')[0]).prop('title'),
				'imageName1': $($('table tr td a')[2]).prop('title')
		},
		success: function(data){
			
			$('#licenceNum').val(data['licenceNum'])
			$('#name').val(data['name'])
			$('#fathersName').val(data['fathersName'])
			$('#address').val(data['address'])
			$('#dobInput').val(data['dob'])
			
			var panObj=data['pan'];
			$('#PanCardNo').val(panObj['panNum'])
			$('#namePan').val(panObj['name'])
			$('#fathersNamePan').val(panObj['fathersName'])
			$('#dobInputPan').val(panObj['dob'])
			$('.loader').css("display","none");
		
		},
		error: function(xhr, textStatus, errorThrown) {
	        $('.loader').css("display","none");
	    }
	})
}
function main (){

	$('.start').click(function(){
		
		$('.loader').css("display","block");
		setTimeout(startFunc, 3000);
		// $.ajax({
		// 	url: '/imageProcessingPan',
		// 	type: 'GET',
		// 	data: {
  // 				'imageName': $($('table tr td a')[2]).prop('title')
		// 	},
		// 	success: function(data){
		// 		console.log("adad")
		// 		console.log(data)
		// 		$('#PanCardNo').val(data['panNum'])
		// 		$('#namePan').val(data['name'])
		// 		$('#fathersNamePan').val(data['fathersName'])
		// 		$('#dobInputPan').val(data['dob'])
		// 		$('.loader').css("display","none");
		// 	},
		// 	error: function(xhr, textStatus, errorThrown) {
		//         $('.loader').css("display","none");
		//     }
		// })	
	})


	$('#submitReq').click(function(){
		var licenceNum = $('#licenceNum').val()
		var name = $('#name').val()
		var fathersName = $('#fathersName').val()
		var address = $('#address').val()
		var dob = $('#dobInput').val()
		var panNum = $('#PanCardNo').val()
		var namePan = $('#namePan').val()
		var fathersNamePan = $('#fathersNamePan').val()
		var dobPan = $('#dobInputPan').val()
		$.ajax({
			url: '/submitAgentDetails',
			type: 'GET',
			data: {
				'licenceNum': licenceNum,
				'name': name,
				'fathersName': fathersName,
				'address': address,
				'dob': dob,
				'panNum': panNum,
				'namePan': namePan,
				'fathersNamePan': fathersNamePan,
				'dobPan': dobPan
			},
			success: function(data){
				window.location.href = "/dashboardAgent"
			}
		});

	});
}