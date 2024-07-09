console.log("JavaScript file loaded");

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded and parsed"); // Check if DOMContentLoaded is fired

    const deleteButtons = document.querySelectorAll('.delete-booking');
    console.log("Delete buttons found:", deleteButtons.length); // Check if delete buttons are found

    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            console.log("Delete button clicked"); // Check if click event is attached
            event.preventDefault();
            if (confirm('Are you sure you want to delete this booking?')) {
                window.location.href = this.getAttribute('href');
            }
        });
    });