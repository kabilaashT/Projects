//Addremove molecule
$(document).ready(function() {
  $('#upload').submit(function(event) {
    event.preventDefault();
    const fileInput = $('#sdf_file')[0];
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('filename', file);
    
    $.ajax({
      url: '/molecule',
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {
        console.log(response);
        // do something with the response from the Python endpoint
      },
      error: function(error) {
        console.error(error);
      }
    });
  });
});

//Select Molecule
$(document).ready(function() {
  $('form').submit(function(event) {
    event.preventDefault();
    
    var formData = {
      'molecule-name': $('input[name=molecule-name]').val(),
    };
    
    $.ajax({
      type: 'POST',
      url: '/selectmolecule',
      data: JSON.stringify(formData),
      contentType: 'application/json',
      success: function(data) {
        console.log('Data sent to server successfully.');
        $('#display-molecule-container').removeClass('hidden');
        // call function to display molecule with data returned from server
        displayMolecule(data);
      },
      error: function(xhr, status, error) {
        console.log('Error sending data to server:', error);
      }
    });
  });
  
  $('#rotate-molecule').click(function() {
    // call function to rotate molecule
    rotateMolecule();
  });
});

function displayMolecule(data) {
  // replace this with your implementation to display the molecule on the canvas
  var canvas = document.getElementById('molecule-canvas');
  var ctx = canvas.getContext('2d');
  ctx.fillStyle = 'white';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = 'black';
  ctx.font = '24px Arial';
  ctx.fillText('Molecule Name: ' + data['molecule-name'], 10, 50);
}

function rotateMolecule() {
  // replace this with your implementation to rotate the molecule on the canvas
  console.log('Molecule rotated.');
}


