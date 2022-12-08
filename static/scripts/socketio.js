document.addEventListener('DOMContentLoaded', ()=>{
    var socket = io();
    
    let room = "General";
    joinRoom('General');

    socket.on('message', data => {
        const p = document.createElement('p');
        const name = document.createElement('name');
        const br = document.createElement('br');

        if (data.username) {
            name.innerHTML = data.username;
            p.innerHTML = name.outerHTML + ": " + data.message + br.outerHTML;
            document.querySelector('#display-message-section').append(p);
        }else{
            printSysMsg(data.message);
        }
        
    });

    document.querySelector('#send_message').onclick = () => {
        socket.send({'message': document.querySelector('#user_message').value, 'username': username, 'room': room });
        document.querySelector('#user_message').value = '';
    }

    document.querySelector('#create_game').onclick = () => {
        const name = document.createElement('name')
        name.innerHTML = username
        document.querySelector('#user1').append(name)
        socket.send({'message':'waiting for another user','username': username, 'room': room})
    }

    document.querySelector('#join_game').onclick = () => {
        const name = document.createElement('name')
        name.innerHTML = username
        document.querySelector('#user2').append(name)
        socket.send({'message': "joined the game", 'username': username, 'room': room})
    }
    
    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            if (newRoom === room) {
                message = `You are already in ${room}.`;
                printSysMsg(message);
            }else{
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        }

    });

    function leaveRoom(room){
        socket.emit('leave', {'username': username, 'room': room});
    }
    
    function joinRoom(room){
        socket.emit('join', {'username': username, 'room': room});
        document.querySelector('#display-message-section').innerHTML = '';

    }

    function printSysMsg(message){
        const p = document.createElement('p');
        p.innerHTML = message;
        document.querySelector('#display-message-section').append(p);
    }
});