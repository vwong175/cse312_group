document.addEventListener('DOMContentLoaded', () => {

    // Hide the game page and the controls the momment the user enters the lobby
    hideGame();

    let roomid;
    let player1 = false;
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port, {transports: ['websocket']});

    socket.on("new_game", data => {
        document.getElementsByClassName("row")[0].style.visibility = "hidden";
        document.getElementsByClassName("header")[0].style.visibility = "hidden";
        document.getElementById("message").innerHTML ="Waiting for player 2, room ID is "+ data['room_id'];
        roomid = data['room_id']
    })

    socket.on('user2_joined', data => {
        showpage(data);
    })
    
    socket.on('wait', data =>{
        document.getElementById("message").innerHTML = data['person_waiting'] + " is waiting...";
    })

    socket.on('leave', data => {
        clearScores();
        document.getElementsByClassName("row")[0].style.visibility = "visible";
        document.getElementsByClassName("header")[0].style.visibility = "visible";
        hideGame();
    })
    
    socket.on('result', data => {
        if (data['result'] === 'TIE'){
            document.getElementById("message").innerHTML = "It's a tie!";
        }else{
            if (data['result'] === 'player1_win'){
                winner = document.getElementsByClassName("name1")[0].innerHTML
                document.getElementById("message").innerHTML = winner + " won!";
                document.getElementById("player1_score").innerHTML = parseInt(document.getElementById("player1_score").innerHTML) + 1
            }else{
                winner = document.getElementsByClassName("name2")[0].innerHTML
                document.getElementById("message").innerHTML = winner + " won!";
                document.getElementById("player2_score").innerHTML = parseInt(document.getElementById("player2_score").innerHTML) + 1

            }
        }
    })

    // Show the game only on user 1's page
    socket.on('show_game_user_1', data => {
        showGame()
    })
    ///////////////////////////////////////////////
            // SENDING a websocket message //
    ///////////////////////////////////////////////

    // Request to create a room
    document.querySelector("#create_room_btn").onclick = () => {
        player1 = true;
        socket.emit('create_room', {"username": username});
        // Show the message div
        document.getElementById("message").style.visibility = "visible";
    }

    document.querySelector("#join_room_btn").onclick = () => {
        roomid = document.querySelector('#room_id').value;     
        socket.emit('join_game', {"username": username, 'room_id': roomid});
        // Show the game page on user 2's page
        showGame()
        socket.emit('show_game_user_1')
    }

    document.querySelector('#leave_room_btn').onclick = () => {
        socket.emit('leave_room', {'username':username, 'room_id': roomid})
    }

    document.querySelector('#rock').onclick = () => {
        let choice_number;
        if (player1 === true){
            choice_number = "player1_choice";
        }else{
            choice_number = "player2_choice";
        }
        socket.emit(choice_number, {'player1':document.getElementsByClassName("name1")[0].innerHTML,'player2':document.getElementsByClassName('name2')[0].innerHTML,'choice':'rock', 'room_id':roomid})
    }

    document.querySelector('#paper').onclick = () => {
        let choice_number;
        if (player1 === true){
            choice_number = "player1_choice";
        }else{
            choice_number = "player2_choice";
        }
        socket.emit(choice_number, {'player1':document.getElementsByClassName("name1")[0].innerHTML,'player2':document.getElementsByClassName('name2')[0].innerHTML,'choice':'paper', 'room_id':roomid})
    }

    document.querySelector('#scissor').onclick = () => {
        let choice_number;
        if (player1 === true){
            choice_number = "player1_choice";
        }else{
            choice_number = "player2_choice";
        }
        socket.emit(choice_number, {'player1':document.getElementsByClassName("name1")[0].innerHTML,'player2':document.getElementsByClassName('name2')[0].innerHTML,'choice':'scissor', 'room_id':roomid})
    }

    // Request to join a room
    function showpage(data){
        document.getElementsByClassName("row")[0].style.visibility = "hidden";
        document.getElementsByClassName("header")[0].style.visibility = "hidden";
        document.getElementsByClassName("name1")[0].innerHTML = data['user1'];
        document.getElementsByClassName("name2")[0].innerHTML = data['user2'];
        document.getElementById("message").innerHTML = data['user2'] +" and " + data['user1'] + " is here!";
    }

    // When the user enters the lobby
    function hideGame(){
        document.getElementsByClassName("leaderboard")[0].style.visibility = "hidden";
        document.getElementsByClassName("controls")[0].style.visibility = "hidden";
        document.getElementsByClassName("Leave")[0].style.visibility = "hidden";
        document.getElementById("message").style.visibility = "hidden";
    }

    function showGame(){
        document.getElementsByClassName("leaderboard")[0].style.visibility = "visible";
        document.getElementsByClassName("controls")[0].style.visibility = "visible";
        document.getElementsByClassName("Leave")[0].style.visibility = "visible";
        document.getElementById("message").style.visibility = "visible";
    }

    function clearScores(){
        document.getElementById("player2_score").innerHTML = "0"
        document.getElementById("player1_score").innerHTML = "0"
    }

});