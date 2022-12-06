document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    // var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port, {transports: ['websocket']});

    var socket = io.connect("http://127.0.0.1:5000", {transports: ['websocket']});

    // socket.on('connect', () =>{
    //     socket.send("I am connected!");
    // });

    // Set default room
    let room = "Lounge"
    joinRoom("Lounge");

    // // Retrieve username
    // const username = document.querySelector('#get-username').innerHTML;

    ////////////////////////////////////////////////
                // Receive messsages //
    ///////////////////////////////////////////////

    // data is the exact string that is being sent from the server
    socket.on("message", data => {
        console.log(`Data is: ${data}`)
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const br = document.createElement('br');

        span_username.innerHTML = data.username;
        p.innerHTML = span_username.innerHTML + br.outerHTML + data.msg + br.outerHTML;
        document.querySelector("#display-message-section").append(p);
    });

    ///////////////////////////////////////////////
    // Functionality to send a websocket message //
    ///////////////////////////////////////////////

    // Send a json message
    document.querySelector("#send_message").onclick = () => {
        socket.send({"msg": document.querySelector('#user_message').value, 
                    "username": username, 
                    "room": room
        });
    }

    // Send room selection
    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            if (newRoom == room){
                msg = `You are already in the ${room} room`
                printSysMsg(msg);
            } else {
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        }
    })

    //////////////////////////////////////////////
                    // Functions //
    //////////////////////////////////////////////

    // Leave room functionality
    function leaveRoom(room){
        socket.emit('leave', {'username': username, "room": room});
    }

    // Join room functionality
    function joinRoom(room){
        socket.emit('join', {'username': username, 'room': room});
        document.querySelector("#display-message-section").innerHTML = ""
    }

    // Print system messages
    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
    }
});