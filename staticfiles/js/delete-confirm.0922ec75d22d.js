
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.delete-booking').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default action

            const bookingId = button.getAttribute('data-booking-id'); // Get the booking id from the data attribute
            const deleteForm = document.getElementById(`delete-form-${bookingId}`); // Get the form element

            if (confirm('Are you sure you want to delete this booking?')) {
                deleteForm.submit(); // Submit the form
            }
        });
    });
});