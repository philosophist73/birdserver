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


