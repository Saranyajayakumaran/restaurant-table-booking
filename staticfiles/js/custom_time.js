document.addEventListener('DOMContentLoaded', function () {
    var bookingDateInput = document.querySelector('input[name="booking_date"]');
    var bookingTimeInput = document.querySelector('.custom-time-input');
    var openingTime = 11;  // Restaurant opening time (e.g., 10:00 AM)
    var closingTime = 23;  // Restaurant closing time (e.g., 8:00 PM)
    var interval = 30;     // Time interval (in minutes)

    bookingDateInput.addEventListener('change', function () {
        var selectedDate = new Date(this.value);
        var today = new Date();
        var options = '';

        // Clear previous options
        bookingTimeInput.innerHTML = '';

        if (selectedDate.setHours(0, 0, 0, 0) === today.setHours(0, 0, 0, 0)) {
            // Today's date
            var currentTime = today.getHours() + 1;  // Start from the next hour
            for (var hour = currentTime; hour <= closingTime; hour++) {
                for (var minute = 0; minute < 60; minute += interval) {
                    var time = hour + ':' + (minute < 10 ? '0' : '') + minute;
                    options += '<option value="' + time + '">' + time + '</option>';
                }
            }
        } else {
            // Future date
            for (var hour = openingTime; hour <= closingTime; hour++) {
                for (var minute = 0; minute < 60; minute += interval) {
                    var time = hour + ':' + (minute < 10 ? '0' : '') + minute;
                    options += '<option value="' + time + '">' + time + '</option>';
                }
            }
        }

        bookingTimeInput.innerHTML = options;
    });
});