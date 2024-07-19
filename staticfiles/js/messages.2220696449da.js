document.addEventListener('DOMContentLoaded', (event) => {
    const messagesDiv = document.getElementById('messages');
    if (messagesDiv) {
        setTimeout(() => {
            messagesDiv.classList.add('hide');
            setTimeout(() => {
                messagesDiv.style.display = 'none';
            }, 1000); 
        }, 4000);  // Start fading out after 4 seconds
    }
});