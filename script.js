//addRemove file (add)
$(document).ready(function() {
	$('#add-remove-form').submit(function(event) {
	  event.preventDefault();
	  
	  var formData = {
		'element-number': $('input[name=element-number]').val(),
		'element-code': $('input[name=element-code]').val(),
		'element-name': $('input[name=element-name]').val(),
		'element-colors-1': $('input[name=element-colors-1]').val(),
		'element-colors-2': $('input[name=element-colors-2]').val(),
		'element-colors-3': $('input[name=element-colors-3]').val(),
		'element-radius': $('input[name=element-radius]').val()
	  };
	  
	  $.ajax({
		type: 'POST',
		url: 'http://localhost:53482/add',
		data: JSON.stringify(formData),
		contentType: false,
		success: function(data) {
		  console.log('Data sent to server successfully.');
		},
		error: function(xhr, status, error) {
		  console.log('Error sending data to server:', error);
		}
	  });
	});

	//upload file
	$("#upload").on("submit", function (event) {
		event.preventDefault();

		var formData = new FormData();
		formData.append("moleculeName", $("#moleculeName").val());
		formData.append("filename", $("#sdf_file")[0].files[0]);

		$.ajax({
			url: "http://localhost:53482/upload",
			type: "POST",
			data: formData,
			processData: false,
			contentType: false,
			success: function (response) {
				console.log("Success:", response);
			},
			error: function (xhr, status, error) {
				console.error("Error:", error);
			},
		});
	});

	//select
	$("#selectMolecule").on("load", function (event) {
		event.preventDefault();
	const moleculeSelect = document.getElementById('mselectMolecule');
	fetch('/addRemove')
		.then(response => response.json())
		.then(data => {
		data.molecules.forEach(molecule => {
			const option = document.createElement('option');
			option.value = molecule;
			option.text = molecule;
			moleculeSelect.add(option);

			$.ajax({
				url: "http://localhost:53482/select",
				type: "POST",
				data: formData,
				processData: false,
				contentType: false,
				success: function (response) {
					console.log("Success:", response);
				},
				error: function (xhr, status, error) {
					console.error("Error:", error);
				},
			});

		});
		});
	});	
		
  });



  