import machine
from machine import TouchPad, Pin, Timer
import esp32
import socket, network
import time

# Global variables
temp = esp32.raw_temperature() # measure temperature sensor data
hall = esp32.hall_sensor() # measure hall sensor data
red_led_state = "Off" # string, check state of red led, ON or OFF


    
def web_page():
    """Function to build the HTML webpage which should be displayed
    in client (web browser on PC or phone) when the client sends a request
    the ESP32 server.
    
    The server should send necessary header information to the client
    (YOU HAVE TO FIND OUT WHAT HEADER YOUR SERVER NEEDS TO SEND)
    and then only send the HTML webpage to the client.
    
    Global variables:
    temp, hall, red_led_state
    """
    
    html_webpage = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chess Game
    </title>
    <style>
        .chess-board { border-spacing: 0; border-collapse: collapse; }
        .chess-board th { padding: .5em; }
        .chess-board th + th { border-bottom: 1px solid #000; }
        .chess-board th:first-child,
        .chess-board td:last-child { border-right: 1px solid #000; }
        .chess-board tr:last-child td { border-bottom: 1px solid; }
        .chess-board th:empty { border: none; }
        .chess-board td { width: 1.5em; height: 1.5em; text-align: center; font-size: 44px; line-height: 0;}
        .chess-board .light { background: #eee; width: 100px; height: 90px; font-size: 44px; }
        .chess-board .dark { background: #aaa; width: 100px; height: 90px; font-size: 44px; }
    </style>
</head>
<body>

<table class="chess-board">
    <tr>
        <th></th>
        <th>a</th>
        <th>b</th>
        <th>c</th>
        <th>d</th>
        <th>e</th>
        <th>f</th>
        <th>g</th>
        <th>h</th>
    <tr>
        <th>8</th>
        <td><button id="57" class="light" onclick="setButton(this)">♜</button></td>
        <td><button id="58" class="dark" onclick="setButton(this)">♞</button></td>
        <td><button id="59" class="light" onclick="setButton(this)">♝</button></td>
        <td><button id="60" class="dark" onclick="setButton(this)">♛</button></td>
        <td><button id="61" class="light" onclick="setButton(this)">♚</button></td>
        <td><button id="62" class="dark" onclick="setButton(this)">♝</button></td>
        <td><button id="63" class="light" onclick="setButton(this)">♞</button></td>
        <td><button id="64" class="dark" onclick="setButton(this)">♜</button></td>
    </tr>
    <tr>
        <th>7</th>
        <td><button id="49" class="dark" onclick="setButton(this)">♟</button></td>
        <td><button id="50" class="light" onclick="setButton(this)">♟</button></td>
        <td><button id="51" class="dark" onclick="setButton(this)">♟</button></td>
        <td><button id="52" class="light" onclick="setButton(this)">♟</button></td>
        <td><button id="53" class="dark" onclick="setButton(this)">♟</button></td>
        <td><button id="54" class="light" onclick="setButton(this)">♟</button></td>
        <td><button id="55" class="dark" onclick="setButton(this)">♟</button></td>
        <td><button id="56" class="light" onclick="setButton(this)">♟</button></td>
    </tr>
    <tr>
        <th>6</th>
        <td><button id="41" class="light" onclick="setButton(this)"></button></td>
        <td><button id="42" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="43" class="light" onclick="setButton(this)"></button></td>
        <td><button id="44" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="45" class="light" onclick="setButton(this)"></button></td>
        <td><button id="46" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="47" class="light" onclick="setButton(this)"></button></td>
        <td><button id="48" class="dark" onclick="setButton(this)"></button></td>
    </tr>
    <tr>
        <th>5</th>
        <td><button id="33" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="34" class="light" onclick="setButton(this)"></button></td>
        <td><button id="35" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="36" class="light" onclick="setButton(this)"></button></td>
        <td><button id="37" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="38" class="light" onclick="setButton(this)"></button></td>
        <td><button id="39" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="40" class="light" onclick="setButton(this)"></button></td>
    </tr>
    <tr>
        <th>4</th>
        <td><button id="25" class="light" onclick="setButton(this)"></button></td>
        <td><button id="26" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="27" class="light" onclick="setButton(this)"></button></td>
        <td><button id="28" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="29" class="light" onclick="setButton(this)"></button></td>
        <td><button id="30" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="31" class="light" onclick="setButton(this)"></button></td>
        <td><button id="32" class="dark" onclick="setButton(this)"></button></td>
    </tr>
    <tr>
        <th>3</th>
        <td><button id="17" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="18" class="light" onclick="setButton(this)"></button></td>
        <td><button id="19" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="20" class="light" onclick="setButton(this)"></button></td>
        <td><button id="21" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="22" class="light" onclick="setButton(this)"></button></td>
        <td><button id="23" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="24" class="light" onclick="setButton(this)"></button></td>
    </tr>
    <tr>
        <th>2</th>
        <td><button id="9" class="light" onclick="setButton(this)">♙</button></td>
        <td><button id="10" class="dark" onclick="setButton(this)">♙</button></td>
        <td><button id="11" class="light" onclick="setButton(this)">♙</button></td>
        <td><button id="12" class="dark" onclick="setButton(this)">♙</button></td>
        <td><button id="13" class="light" onclick="setButton(this)">♙</button></td>
        <td><button id="14" class="dark" onclick="setButton(this)">♙</button></td>
        <td><button id="15" class="light" onclick="setButton(this)">♙</button></td>
        <td><button id="16" class="dark" onclick="setButton(this)">♙</button></td>
    </tr>
    <tr>
        <th>1</th>
        <td><button id="1" class="dark" onclick="setButton(this)">♖</button></td>
        <td><button id="2" class="light" onclick="setButton(this)">♘</button></td>
        <td><button id="3" class="dark" onclick="setButton(this)">♗</button></td>
        <td><button id="4" class="light" onclick="setButton(this)">♕</button></td>
        <td><button id="5" class="dark" onclick="setButton(this)">♔</button></td>
        <td><button id="6" class="light" onclick="setButton(this)">♗</button></td>
        <td><button id="7" class="dark" onclick="setButton(this)">♘</button></td>
        <td><button id="8" class="light" onclick="setButton(this)">♖</button></td>
    </tr>
    
</table>

<button id="buttonstart" style= "width: 200px; height: 90px; font-size: 44px;" onclick="setButton2(this)">Start</button>
<button id="buttonendgame" style= "width: 200px; height: 90px; font-size: 44px;" onclick="setButton3(this)">End</button>
<button id="buttonTurn" style= "width: 200px; height: 90px; font-size: 30px;" onclick="setButton3(this)">Turn: White</button>

<script>
    var orderCounter = 1; // flag to keep track of order of button presses, goes from 1-> 2 for first click, 2-> 1 for second click
    var c_spacetomove = '#fbe790'; // color for the possible move spaces
    var possiblemoves= []; // Holds button ids, array to hold all possible moves for a piece, index 0 holds the square where the piece to be moved is
    var move_flag = 0; // flag that swaps to 1 if player move was in the list of possible moves
    var turn_flag = 0 // 0 for white, 1 for black


    function setButton2(button) {
        if(button.textContent == "Start"){
            sendMessageToServer("Start");
        }
        orderCounter = 1;
        turn_flag = 0;
        button.textContent = "Count " + (orderCounter);
    }

    function setButton3(button) {
        sendMessageToServer("End");
    }

    function setButton(button) {
        // what happens when the clicked space is where the old piece will be moved
        if (orderCounter > 1) {
            // make sure button is in list of possible moves
            for (var i = 0; i < possiblemoves.length; i++) {
                if(String(possible_moves[i]) == button.id){
                    move_flag = 1;
                    break;
                }
            }
            // if space not in list if possible moves do nothing
            if(move_flag == 0){return;}
            // reset move flag
            move_flag = 0;
            // check if clicked space is the same as the selected piece
            if(button.id == String(possiblemoves[0])){
                revertcolor(possible_moves);
                // reset order counter
                orderCounter = 1;
                document.getElementById("buttonstart").textContent = "Count " + (orderCounter);
                return;
            }
        
            //move the piece by: changing the now clicked button to the old text and removing the text of the old button
            button.textContent = document.getElementById(String(possiblemoves[0])).textContent;
            document.getElementById(String(possiblemoves[0])).textContent = "";
            sendMessageToServer(String(possiblemoves[0]) + ' ' + button.id);
            revertcolor(possiblemoves);
            orderCounter = 0
            // increment turn counter and update display
            turn_flag = turn_flag + 1;
            if(turn_flag > 1){turn_flag = 0;}
            if(turn_flag == 0){document.getElementById("buttonTurn").textContent = "Turn: white";}
            else{document.getElementById("buttonTurn").textContent = "Turn: Black";}
        }
        // what happens when the piece thats clicked is selected to be moved
        else {    
            // make sure its not empty
            if(button.textContent == ''){return}
            // check to make sure its the right turn
            if(turn_flag == 0){
                if(getColor(button.textContent) !== 'white'){return;}
            }
            if(turn_flag == 1){
                if(getColor(button.textContent) !== 'black'){return;}
            }
            //buttonid = button.id;
            // set color for the selected piece space
            button.style.backgroundColor = '#c8a951';
            possiblemoves = setpossiblemoves(parseInt(button.id),button.textContent);
        }
        
        orderCounter++;
        document.getElementById("buttonstart").textContent = "Count " + (orderCounter);
    }

    function setpossiblemoves(from,piece){
        possible_moves = [];

        possible_moves.push(from); // add the moving piece to the array

        //check what piece it is and set the moves accordingly
        if((piece == '♙') || (piece == '♟')){setPawnMoves(possible_moves,from,piece);}
        else if((piece == '♖') || (piece == '♜')){setRookMoves(possible_moves,from,piece);}
        else if((piece == '♗') || (piece == '♝')){setBishopMoves(possible_moves,from,piece);}
        else if((piece == '♕') || (piece == '♛')){setQueenMoves(possible_moves,from,piece);}
        else if((piece == '♘') || (piece == '♞')){setKnightMoves(possible_moves,from,piece);}
        else if((piece == '♔') || (piece == '♚')){setKingMoves(possible_moves,from,piece);}
        else{throw new Error('Cannot set possible moves, piece is not a chesspiece');}

        // change the color of all the potential move spaces
        for (var i = 1; i < possible_moves.length; i++) {
            document.getElementById(String(possible_moves[i])).style.backgroundColor = c_spacetomove;
        }

        return possible_moves;;
    }

    function setPawnMoves(possible_moves, from, piece){
        // set dirrection, either up the board or down, so that the possible moves can be multiplied by it
        if (piece == '♙'){dir = 1;}
        else{dir = -1;}
        pieceColor = getColor(piece);

        // if pawn is at the end of the board just return for now
        if((pieceColor == 'black' && (from >= 1 && from <= 8)) || (pieceColor == 'white' && (from >= 57 && from <= 64))){return;}

        // START ADDING POSSIBLE MOVES
        // if space ahead is empty add that move
        if(document.getElementById(String(from+(8*dir))).textContent == ''){
            possible_moves.push(from+(8*dir));
        }   
        // if there is a piece that can be taken
        if((document.getElementById(String(from+(8*dir) + 1)).textContent !== '') && (pieceColor !== getColor(document.getElementById(String(from+(8*dir) + 1)).textContent))){
            possible_moves.push(from+(8*dir) + 1);
        }
        if((document.getElementById(String(from+(8*dir) - 1)).textContent !== '') && (pieceColor !== getColor(document.getElementById(String(from+(8*dir) - 1)).textContent))){

            possible_moves.push(from+(8*dir) - 1);
        }
        // if piece is in the first row of either side add the optional 2 space move
        if (((dir == 1 && (from >= 9 && from <= 16)) ||(dir == -1 && (from >= 49 && from <= 66))) && (document.getElementById(String(from+(16*dir))).textContent == '') ){
            if(document.getElementById(String(from+(8*dir))).textContent == ''){
                possible_moves.push(from+(16*dir));
            }
        }

        return possible_moves;

    }

    function setRookMoves(possible_moves, from, piece){
        pieceColor = getColor(piece);
        col = ((from-1)%8)+1;
        row = Math.floor((from-1)/8);

        // START ADDING POSSIBLE MOVES
        // add moves to the right til you hit something
        tempcol = col + 1; // move by 1 to start checking 1 right of the piece
        temprow = row;
        while(tempcol <= 8){
            if(document.getElementById(String(tempcol + (temprow*8))).textContent == ''){
                possible_moves.push(String(tempcol + (temprow*8)));
            }
            else{
                if(getColor(document.getElementById(String(tempcol + (temprow*8))).textContent) !== pieceColor){
                    possible_moves.push(String(tempcol + (temprow*8)));
                }
                break;
            }
            tempcol++;
        }

        // add moves to the left til you hit something
        tempcol = col - 1; // move by 1 to start checking 1 left of the piece
        temprow = row;
        while(tempcol >= 1){
            if(document.getElementById(String(tempcol + (temprow*8))).textContent == ''){
                possible_moves.push(String(tempcol + (temprow*8)));
            }
            // check if piece hit is a different color
            else{
                if(getColor(document.getElementById(String(tempcol + (temprow*8))).textContent) !== pieceColor){
                    possible_moves.push(String((tempcol + (temprow*8))));
                }
                break;
            }
            tempcol--;
        }

        // add moves up til you hit something
        tempcol = col ;
        temprow = row + 1; // move by 1 to start checking 1 above the piece
        while(temprow <= 7){
            if(document.getElementById(String(tempcol + (temprow*8))).textContent == ''){
                possible_moves.push(String(tempcol + (temprow*8)));
            }
            // check if piece hit is a different color
            else{
                if(getColor(document.getElementById(String(tempcol + (temprow*8))).textContent) !== pieceColor){
                    possible_moves.push(String((tempcol + (temprow*8))));
                }
                break;
            }
            temprow++;
        }

        // add moves down til you hit something
        tempcol = col ;
        temprow = row - 1; // move by 1 to start checking 1 below the piece
        while(temprow >= 0){
            if(document.getElementById(String(tempcol + (temprow*8))).textContent == ''){
                possible_moves.push(String(tempcol + (temprow*8)));
            }
            // check if piece hit is a different color
            else{
                if(getColor(document.getElementById(String(tempcol + (temprow*8))).textContent) !== pieceColor){
                    possible_moves.push(String((tempcol + (temprow*8))));
                }
                break;
            }
            temprow--;
        }


        return possible_moves;
    }

    function setBishopMoves(possible_moves, from, piece){
        pieceColor = getColor(piece);
        col = ((from-1)%8)+1;
        row = Math.floor((from-1)/8);

        // START ADDING POSSIBLE MOVES
        // add moves to the top right til you hit something
        tempcol = col + 1; // move by 1 to start checking 1 right of the piece
        temprow = row + 1; // move by 1 to start checking 1 up of the piece
        while(tempcol <= 8 && temprow <= 7){
            if(document.getElementById(String(tempcol + (temprow*8))).textContent == ''){
                possible_moves.push(String(tempcol + (temprow*8)));
            }
            else{
                if(getColor(document.getElementById(String(tempcol + (temprow*8))).textContent) !== pieceColor){
                    possible_moves.push(String(tempcol + (temprow*8)));
                }
                break;
            }
            tempcol++;
            temprow++;
        }

        // add moves to the bottom right til you hit something
        tempcol = col + 1; // move by 1 to start checking 1 right of the piece
        temprow = row - 1; // move by 1 to start checking 1 down of the piece
        while(tempcol <= 8 && temprow >= 0){
            if(document.getElementById(String(tempcol + (temprow*8))).textContent == ''){
                possible_moves.push(String(tempcol + (temprow*8)));
            }
            else{
                if(getColor(document.getElementById(String(tempcol + (temprow*8))).textContent) !== pieceColor){
                    possible_moves.push(String(tempcol + (temprow*8)));
                }
                break;
            }
            tempcol++;
            temprow--;
        }

        // add moves to the bottom left til you hit something
        tempcol = col - 1; // move by 1 to start checking 1 left of the piece
        temprow = row - 1; // move by 1 to start checking 1 down of the piece
        while(tempcol >= 1 && temprow >= 0){
            if(document.getElementById(String(tempcol + (temprow*8))).textContent == ''){
                possible_moves.push(String(tempcol + (temprow*8)));
            }
            else{
                if(getColor(document.getElementById(String(tempcol + (temprow*8))).textContent) !== pieceColor){
                    possible_moves.push(String(tempcol + (temprow*8)));
                }
                break;
            }
            tempcol--;
            temprow--;
        }

        // add moves to the top left til you hit something
        tempcol = col - 1; // move by 1 to start checking 1 left of the piece
        temprow = row + 1; // move by 1 to start checking 1 up of the piece
        while(tempcol >= 1 && temprow <= 7){
            if(document.getElementById(String(tempcol + (temprow*8))).textContent == ''){
                possible_moves.push(String(tempcol + (temprow*8)));
            }
            else{
                if(getColor(document.getElementById(String(tempcol + (temprow*8))).textContent) !== pieceColor){
                    possible_moves.push(String(tempcol + (temprow*8)));
                }
                break;
            }
            tempcol--;
            temprow++;
        }
    }

    function setQueenMoves(possible_moves, from, piece){
        // since the queen can move as both a rook and a bishop can simply call those 2 functions
        setBishopMoves(possible_moves,from,piece);
        setRookMoves(possible_moves,from,piece);
    }

    function setKnightMoves(possible_moves, from, piece){
        pieceColor = getColor(piece);
        col = ((from-1)%8)+1;
        row = Math.floor((from-1)/8);

        // START ADDING POSSIBLE MOVES
        // add all 8 possible moves to array
        movelist = [[col+1,row+2],[col-1,row+2],[col+1,row-2],[col-1,row-2],[col+2,row+1],[col+2,row-1],[col-2,row+1],[col-2,row-1]];
        // check to see what moves of the possible ones are valid
        for(var i=0;i<movelist.length;i++){
            if(movelist[i][0] >= 1 && movelist[i][0] <= 8 && movelist[i][1] >= 0 && movelist[i][1] <= 7){ // if the move is within bounds
                if(document.getElementById(String(movelist[i][0] + (movelist[i][1]*8))).textContent == ''){
                    possible_moves.push(String(movelist[i][0] + (movelist[i][1]*8)));
                }
                else{
                    if(getColor(document.getElementById(String(movelist[i][0] + (movelist[i][1]*8))).textContent) !== pieceColor){
                        possible_moves.push(String(movelist[i][0] + (movelist[i][1]*8)));
                    }   
                }
            }
            else{;} // move is not in bounds so do nothing
        }
    }

    function setKingMoves(possible_moves, from, piece){
        pieceColor = getColor(piece);
        col = ((from-1)%8)+1;
        row = Math.floor((from-1)/8);

        // START ADDING POSSIBLE MOVES
        // add all 8 possible moves to array
        movelist = [[col,row+1],[col+1,row+1],[col+1,row],[col+1,row-1],[col,row-1],[col-1,row-1],[col-1,row],[col-1,row+1]];
        // check to see what moves of the possible ones are valid
        for(var i=0;i<movelist.length;i++){
            if(movelist[i][0] >= 1 && movelist[i][0] <= 8 && movelist[i][1] >= 0 && movelist[i][1] <= 7){ // if the move is within bounds
                if(document.getElementById(String(movelist[i][0] + (movelist[i][1]*8))).textContent == ''){
                    possible_moves.push(String(movelist[i][0] + (movelist[i][1]*8)));
                }
                else{
                    if(getColor(document.getElementById(String(movelist[i][0] + (movelist[i][1]*8))).textContent) !== pieceColor){
                        possible_moves.push(String(movelist[i][0] + (movelist[i][1]*8)));
                    }   
                }
            }
            else{;} // move is not in bounds so do nothing
        }
    }

    function getColor(piece){
        color = ''
        if (piece == '♙' || piece == '♖' || piece == '♘' || piece == '♗' || piece == '♕'  || piece == '♔'){
            color = 'white';
        }
        else{color = 'black';}
        return color;
    }

    function revertcolor(moves) {

        for (var i = 0; i < moves.length; i++) {
            if ((moves[i] >= 1 && moves[i] <= 8) || (moves[i] >= 17 && moves[i] <= 24)|| (moves[i] >= 33 && moves[i] <= 40)|| (moves[i] >= 49 && moves[i] <= 56)) {
                if (moves[i] % 2 == 0) {
                    document.getElementById(String(moves[i])).style.backgroundColor = '#eee';
                } else {
                    document.getElementById(String(moves[i])).style.backgroundColor = '#aaa';
                }
            } else {
                if (moves[i] % 2 == 0) {
                    document.getElementById(String(moves[i])).style.backgroundColor = '#aaa';
                } else {
                    document.getElementById(String(moves[i])).style.backgroundColor = '#eee';
                }
            }
        }
    }


    function sendMessageToServer(message) {
        
                // Make an asynchronous request to the server
                fetch('/buttonClick', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message }),
                })
                .then(response => response.text())
                .then(data => {
                    console.log('Server response:', data);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
</script>

</body>
</html>
"""
    return html_webpage


wlan = network.WLAN(network.STA_IF)
#wlan = network.WLAN(network.AP_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    #wlan.connect('CookeFamily','P@rty0fF!ve')
    wlan.connect('Chickennuggs','13221322')
    while not wlan.isconnected():
        pass
print("Connected to Network")
print('IP Address:', wlan.ifconfig()[0])


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = ('', 8082)
s.bind(addr)
s.listen(1)

count = 1
while True:
        # Wait for a connection
        print("Waiting for a connection...")
        client, client_address = s.accept()
        print(f"Accepted connection from {client_address}")

        # Receive and print the incoming data (HTTP request)
        request_data = client.recv(1024).decode('utf-8')
        print("Received data:\n", request_data)
        processed_data = request_data.split('"message":')
        if(processed_data[len(processed_data) - 1][1:-2]) == 'End':
            break

        # Read the content of the HTML file
        if count == 1:
            html_content = web_page()

            # Send the HTML content as the HTTP response
            response = f"HTTP/1.1 200 OK\nContent-Type: text/html\n\n{html_content}\n"
            client.sendall(response.encode('utf-8'))
        else:
            response = f"HTTP/1.1 200 OK\nContent-Type: text/html\n\nThanks {count}\n"
            client.sendall(response.encode('utf-8'))
            
            #time.sleep(10)
            response = f"bye {count}"

            client.sendall(response.encode('utf-8'))
        count = count + 1
        client.close()
            

        
s.close()
wlan.disconnect()
    
