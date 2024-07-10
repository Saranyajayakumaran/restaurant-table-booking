

document.addEventListener('DOMContentLoaded', function() {
    $('#confirmDeleteModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var bookingId = button.data('booking-id'); // Extract info from data-* attributes
        var form = $('#deleteForm');
        var actionUrl = form.data('action-base') + bookingId + '/';
        form.attr('action', actionUrl); // Update form action with booking ID
    });
});