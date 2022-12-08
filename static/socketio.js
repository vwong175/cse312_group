document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port, {transports: ['websocket']});

    socket.on('connect', () =>{
        console.log(`The socket instance id is: ${socket.id}`)
        console.log("socket is connected on the client side")
        socket.send("I am connected!");
    });

    socket.on('disconnect', () =>{
        socket.send(`The socket with id ${socket.id} disconnected`)
    });
     
    ////////////////////////////////////////////////
      // Joining and leaving rooms functionality //
    ////////////////////////////////////////////////
    // Join room functionality
    function joinRoom(){
        socket.emit('join', {'username': username});
    }

    // Leave room functionality
    function leaveRoom(room){
        socket.emit('leave', {'username': username, "room": room});
    }

    ///////////////////////////////////////////////
            // SENDING a websocket message //
    ///////////////////////////////////////////////

    // Request to create a room
    document.querySelector("#create_room_btn").onclick = () => {
        socket.emit('create_room', {"name": username});
        console.log("Emitted the message")
    }

    // Request to join a room
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
});