//birdSightingModal
document.addEventListener('DOMContentLoaded', function() {
    var birdSightingModal = document.getElementById('birdSightingModal');
    
    if (birdSightingModal) {
        birdSightingModal.addEventListener('shown.bs.modal', function() {
            var timestampField = document.getElementById('timestamp');
    
            // Get the current date and time
            var now = new Date();
    
            // Format it to match the format expected by the datetime-local input field
            var formattedDate = now.toISOString().slice(0, 16); // YYYY-MM-DDTHH:mm
    
            // Set the value of the timestamp input field
            timestampField.value = formattedDate;

            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function (position) {
                    document.getElementById("modal_latitude").value = position.coords.latitude;
                    document.getElementById("modal_longitude").value = position.coords.longitude;
                });
            }
        });
    }
});

//datatable for birdSightingsTable and birdResultsTable
$(document).ready(function () {
    $('#birdSightingsTable, #birdResultsTable').DataTable();
});


//Open the bird sighting modal and populate it with row data
$(document).ready( function () {
    $('#birdSightingsTable').on('click', '.edit-btn', function () {
        //fixed bug where modal would not open by HTML
        $('#editModal').modal('show');
        var row = $(this).closest('tr');
        var cols = row.find('td');

        // Assuming the order of columns is Timestamp, Bird Name, Notes, Location
        var timestamp = $(cols[0]).text();
        var birdName = $(cols[1]).text();
        var notes = $(cols[2]).text();
        var location = $(cols[3]).text();
        var birdSightingID = $(cols[5]).text();

        // Populate modal fields
        $('#editTimestamp').val(timestamp);
        $('#editBirdName').val(birdName);
        $('#editNotes').val(notes);
        $('#editLocation').val(location);
        $('#editBirdSightingID').val(birdSightingID);
    });
});

//Close the bird sighting edit modal
$(document).ready( function () {
    $('#cancelEdit').on('click', function () {
        $('#editModal').modal('hide');
    });
});


//Submit the bird sighting modal
//TODO: dont submit if no changes were made
//TODO: dont reload the page, just update the table
$(document).ready( function () {
    $('#submitEdit').on('click', function () {
        // Gather edited data from modal fields
        var editedTimestamp = $('#editTimestamp').val();
        var editedNotes = $('#editNotes').val();
        var editedLocation = $('#editLocation').val();
        var editBirdSightingID = $('#editBirdSightingID').val();

        var jsonData = {
            timestamp: editedTimestamp,
            notes: editedNotes,
            location: editedLocation,
            id: editBirdSightingID
        };

        // call birdserver
        $.ajax({
            url: '/edit_sighting',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(jsonData),
            success: function (response) {
                // Handle success
                //console.log('Data edited successfully!');
                location.reload();
            },
            error: function (error) {
                // Handle error
                console.error('Error editing data:', error);
            }
        });
        //fixed a bug where the modal would not close
        //$('#editModal').modal('hide');
    });
});

//add or remove a bird to favorites
$(document).ready(function() {
    $('#favorite-icon').click(function() {

        var birdId = $('#bird_id').val();
        var jsonData = {
            id: birdId
        };

        //this is a favorite
        if ($('#favorite-icon').hasClass('fas')) {
            console.log('fas');
            $.ajax({
                url: '/remove_favorite',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(jsonData),
                success: function (response) {
                    $('#favorite-icon').removeClass('fas').addClass('far');
                },
                error: function (error) {
                    console.error('Error editing data:', error);
                }
            });
        }
        else {
            console.log('far');
            $.ajax({
                url: '/add_favorite',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(jsonData),
                success: function (response) {
                    // Handle success
                    $('#favorite-icon').removeClass('far').addClass('fas');
                    console.log('Data edited successfully!');
                },
                error: function (error) {
                    // Handle error
                    console.error('Error editing data:', error);
                }
            });
        }
    });
});

//add or remove a bird to watch
$(document).ready(function() {
    $('#watch-icon').click(function() {

        var birdId = $('#bird_id').val();
        var jsonData = {
            id: birdId
        };

        //this is a favorite
        if ($('#watch-icon').hasClass('fa-eye')) {
            console.log('fa-eye');
            $.ajax({
                url: '/remove_watch',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(jsonData),
                success: function (response) {
                    $('#watch-icon').removeClass('fa-eye').addClass('fa-eye-slash');
                },
                error: function (error) {
                    console.error('Error editing data:', error);
                }
            });
        }
        else {
            console.log('fa-eye-slash');
            $.ajax({
                url: '/add_watch',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(jsonData),
                success: function (response) {
                    // Handle success
                    $('#watch-icon').removeClass('fa-eye-slash').addClass('fa-eye');
                    console.log('Data edited successfully!');
                },
                error: function (error) {
                    // Handle error
                    console.error('Error editing data:', error);
                }
            });
        }
    });
});



