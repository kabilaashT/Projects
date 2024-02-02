//addRemove file (add)
$(document).ready(function() {
	const moleculeSelect = $("#selectMolecule");
    $.ajax({
        url: "http://localhost:53482/select",
        type: "POST",
        processData: false,
        contentType: false,
        success: function (response) {
            response['molecules'].forEach((x)=>{
                moleculeSelect.append(`<option value=${x}>${x}</option>`);
            })
        },
        error: function (xhr, status, error) {
            console.error("Error:", error);
        },
    });

    $("#showMol").on("click",()=>{
        $.ajax({
            url: "http://localhost:53482/display",
            type: "POST",
            data: JSON.stringify({"mol_name":$("#selectMolecule").val(),"rotation":$("#rotation").val()}),
            processData: false,
            contentType: false,
            success: function (response) {
                $("#container").html(response['svg'])
            },
            error: function (xhr, status, error) {
                console.error("Error:", error);
            },
        });
    })

		
  });



  