var latitude = null;
var longitude = null;

//Bird Ticker
document.addEventListener("DOMContentLoaded", function() {

    // Get user's location and fetch birds
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(displayTicker);
    } else {
        //TODO- add another API call to get user's location by IP address
        alert("Geolocation is not supported by this browser.");
    }

    // Callback function to handle the user's location
    function displayTicker(position) {
        latitude = position.coords.latitude;
        longitude = position.coords.longitude;

        // Now you can use 'latitude' and 'longitude' in your fetch request or anywhere else in your code
        getNotableBirdSightings(latitude, longitude);
    }

    //TODO: "cache" this on client side
    function getNotableBirdSightings(latitude, longitude) {
        fetch(`/birdticker?latitude=${latitude}&longitude=${longitude}`)  // Pass latitude and longitude as query parameters
            .then(response => response.json())
            .then(birds => {
                const birdListElement = document.getElementById("birdList");
                birds.forEach(bird => {
                    const listItem = document.createElement("li");
                    listItem.textContent = bird;
                    birdListElement.appendChild(listItem);
                });
                scrollBirds();
            });
    }

    function scrollBirds() {
        var birdList = document.getElementById('birdList');
        var birds = birdList.querySelectorAll('li');
        var birdWidth = birds[0].offsetWidth;
        var containerWidth = birdList.offsetWidth;

        var animationDuration = (containerWidth + birdWidth) / 50; // Adjust speed by changing the denominator

        birdList.style.animation = `scrollBirds linear infinite ${animationDuration}s`;
    }
});


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

//Sorting for the birdSightingsTable
$(document).ready( function () {
    var table = $('#birdSightingsTable').DataTable({
        "columnDefs": [
            { "searchable": false, "targets": [4] }, // Disable searching for Edit column
            { "orderable": false, "targets": [4] }  // Disable sorting for Edit column
        ]
    });

    //disable pagination if there are 10 or fewer items
    //TODO: fix, this doesnt work
    var numItems = table.rows().count();
    if (numItems <= 10) {
        table.page.len(-1).draw(); // -1 disables pagination
    }
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
                console.log('Data edited successfully!');
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



