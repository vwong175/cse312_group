document.addEventListener('DOMContentLoaded', () => {

    let message = document.querySelector('#user_message');
    message.addEventListener('keyup', event => {
        event.preventDefault();
        if (event.keyCode === 13) {
            document.querySelector('#send_message').click();
        }
    })
})