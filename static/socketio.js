document.addEventListener('DOMContentLoaded', () => {
    let roomID;
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port, {transports: ['websocket']});

    socket.on("new_game", data => {
        document.getElementsByClassName("row")[0].style.visibility = "hidden";
        document.getElementById("message").innerHTML ="Waiting for player 2,room ID is "+ data['room_id'];
        roomID = data['room_id']
    })

    socket.on('user1_joined', data => {
        showpage(data);
    })

    socket.on('user2_joined', data => {
        showpage(data);
    })
     
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
        
        socket.emit('create_room', {"username": username});
    }

    document.querySelector("#join_room_btn").onclick = () => {
        id = document.querySelector('#room_id').value;     
        socket.emit('join_game', {"username": username, 'room_id': id})
    }
    // Request to join a room
    function showpage(data){
        document.getElementsByClassName("row")[0].style.visibility = "hidden";
        document.getElementsByClassName("action")[0].style.visibility = "visibile";
        document.getElementsByClassName("name1")[0].innerHTML = data['user1'];
        document.getElementsByClassName("name2")[0].innerHTML = data['user2'];
        document.getElementById("message").innerHTML =data['user2'] + "is here!";
    }
});