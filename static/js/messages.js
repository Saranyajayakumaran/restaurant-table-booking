document.addEventListener('DOMContentLoaded', (event) => {
    const messagesDiv = document.getElementById('messages');
    if (messagesDiv) {
        setTimeout(() => {
            messagesDiv.classList.add('hide');
            setTimeout(() => {
                messagesDiv.style.display = 'none';
            }, 1000);  // Match this timeout with the CSS transition duration
        }, 4000);  // Start fading out after 3 seconds
    }
});