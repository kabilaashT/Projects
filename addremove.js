//addRemove file (add)
$(document).ready(function() {
	const moleculeSelect = $("#elements-list");
    $.ajax({
        url: "http://localhost:53482/selectElement",
        type: "POST",
        processData: false,
        contentType: false,
        success: function (response) {
            response['elements'].forEach((x)=>{
                moleculeSelect.append(`<option value=${x}>${x}</option>`);
            })
        },
        error: function (xhr, status, error) {
            console.error("Error:", error);
        },
    });

    $("#remove-element").on("click",()=>{
        $.ajax({
            url: "http://localhost:53482/deleteElement",
            type: "POST",
            data: JSON.stringify({"element_name":$("#elements-list").val()}),
            processData: false,
            contentType: false,
            success: function (response) {
                // response['elements'].forEach((x)=>{
                //     moleculeSelect.append(`<option value=${x}>${x}</option>`);
                // })
            },
            error: function (xhr, status, error) {
                console.error("Error:", error);
            },
        });

        // location.reload()
    })



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



  