// Wait for the document to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log("Deletion script loaded"); 
    // Find all elements with the class 'delete-booking'
    const deleteButtons = document.querySelectorAll('.delete-booking');

    // Add a click event listener to each delete button
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            // Prevent the default action (following the link)
            event.preventDefault();

            // Confirm deletion using a browser dialog
            if (confirm('Are you sure you want to delete this booking?')) {
                // If confirmed, get the href attribute of the clicked link and navigate to it
                window.location.href = this.getAttribute('href');
            }
        });
    });
});
