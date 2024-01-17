import machine
from machine import TouchPad, Pin, Timer
import esp32
import socket, network

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
    <title>Loop through Buttons in HTML Table (8x8)</title>
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
    <!-- Create an 8 by 8 table -->
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
        <td><button id="a8" class="light" onclick="setButton(this)">♜</button></td>
        <td><button id="b8" class="dark" onclick="setButton(this)">♞</button></td>
        <td><button id="c8" class="light" onclick="setButton(this)">♝</button></td>
        <td><button id="d8" class="dark" onclick="setButton(this)">♛</button></td>
        <td><button id="e8" class="light" onclick="setButton(this)">♚</button></td>
        <td><button id="f8" class="dark" onclick="setButton(this)">♝</button></td>
        <td><button id="g8" class="light" onclick="setButton(this)">♞</button></td>
        <td><button id="h8" class="dark" onclick="setButton(this)">♜</button></td>
    </tr>
    <!-- Repeat the above row 7 more times to create an 8 by 8 table -->
    <tr>
        <th>7</th>
        <td><button id="a7" class="dark" onclick="setButton(this)">♟</button></td>
        <td><button id="b7" class="light" onclick="setButton(this)">♟</button></td>
        <td><button id="c7" class="dark" onclick="setButton(this)">♟</button></td>
        <td><button id="d7" class="light" onclick="setButton(this)">♟</button></td>
        <td><button id="e7" class="dark" onclick="setButton(this)">♟</button></td>
        <td><button id="f7" class="light" onclick="setButton(this)">♟</button></td>
        <td><button id="g7" class="dark" onclick="setButton(this)">♟</button></td>
        <td><button id="h7" class="light" onclick="setButton(this)">♟</button></td>
    </tr>
    <tr>
        <th>6</th>
        <td><button id="a6" class="light" onclick="setButton(this)"></button></td>
        <td><button id="b6" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="c6" class="light" onclick="setButton(this)"></button></td>
        <td><button id="d6" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="e6" class="light" onclick="setButton(this)"></button></td>
        <td><button id="f6" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="g6" class="light" onclick="setButton(this)"></button></td>
        <td><button id="h6" class="dark" onclick="setButton(this)"></button></td>
    </tr>
    <tr>
        <th>5</th>
        <td><button id="a5" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="b5" class="light" onclick="setButton(this)"></button></td>
        <td><button id="c5" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="d5" class="light" onclick="setButton(this)"></button></td>
        <td><button id="e5" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="f5" class="light" onclick="setButton(this)"></button></td>
        <td><button id="g5" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="h5" class="light" onclick="setButton(this)"></button></td>
    </tr>
    <tr>
        <th>4</th>
        <td><button id="a4" class="light" onclick="setButton(this)"></button></td>
        <td><button id="b4" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="c4" class="light" onclick="setButton(this)"></button></td>
        <td><button id="d4" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="e4" class="light" onclick="setButton(this)"></button></td>
        <td><button id="f4" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="g4" class="light" onclick="setButton(this)"></button></td>
        <td><button id="h4" class="dark" onclick="setButton(this)"></button></td>
    </tr>
    <tr>
        <th>3</th>
        <td><button id="a3" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="b3" class="light" onclick="setButton(this)"></button></td>
        <td><button id="c3" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="d3" class="light" onclick="setButton(this)"></button></td>
        <td><button id="e3" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="f3" class="light" onclick="setButton(this)"></button></td>
        <td><button id="g3" class="dark" onclick="setButton(this)"></button></td>
        <td><button id="h3" class="light" onclick="setButton(this)"></button></td>
    </tr>
    <tr>
        <th>2</th>
        <td><button id="a2" class="light" onclick="setButton(this)">♙</button></td>
        <td><button id="b2" class="dark" onclick="setButton(this)">♙</button></td>
        <td><button id="c2" class="light" onclick="setButton(this)">♙</button></td>
        <td><button id="d2" class="dark" onclick="setButton(this)">♙</button></td>
        <td><button id="e2" class="light" onclick="setButton(this)">♙</button></td>
        <td><button id="f2" class="dark" onclick="setButton(this)">♙</button></td>
        <td><button id="g2" class="light" onclick="setButton(this)">♙</button></td>
        <td><button id="h2" class="dark" onclick="setButton(this)">♙</button></td>
    </tr>
    <tr>
        <th>1</th>
        <td><button id="a1" class="dark" onclick="setButton(this)">♖</button></td>
        <td><button id="b1" class="light" onclick="setButton(this)">♘</button></td>
        <td><button id="c1" class="dark" onclick="setButton(this)">♗</button></td>
        <td><button id="d1" class="light" onclick="setButton(this)">♕</button></td>
        <td><button id="e1" class="dark" onclick="setButton(this)">♔</button></td>
        <td><button id="f1" class="light" onclick="setButton(this)">♗</button></td>
        <td><button id="g1" class="dark" onclick="setButton(this)">♘</button></td>
        <td><button id="h1" class="light" onclick="setButton(this)">♖</button></td>
    </tr>
    
</table>

<button id="buttonstart" style= "width: 200px; height: 90px; font-size: 44px;" onclick="setButton2(this)">Start</button>
<button id="buttonendgame" style= "width: 200px; height: 90px; font-size: 44px;" onclick="setButton3(this)">End</button>

<script>
    var orderCounter = 0;
    var tempholder = ''
    var buttonid = ''


    function setButton2(button) {
        if(button.textContent == "Start"){
            sendMessageToServer("Start");
        }

        orderCounter++;
        if (orderCounter > 2) {
            orderCounter = 1;
        }
        button.textContent = "Count " + (orderCounter)
    }

    function setButton3(button) {
        sendMessageToServer("End");
    }

    function setButton(button) {
        // Loop back to 1 after the eighth button is clicked
        if (orderCounter > 1) {
            orderCounter = 0;
            button.textContent = tempholder
            document.getElementById(buttonid).textContent = ""
            sendMessageToServer(buttonid + ' ' + button.id);
        }
        else {
            tempholder = button.textContent
            buttonid = button.id
        }
        
        orderCounter++;
        document.getElementById("buttonstart").textContent = "Count " + (orderCounter)

        // Send a message to the server
        
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
    wlan.connect('CookeFamily','P@rty0fF!ve')
    #wlan.connect('Chickennuggs','13221322')
    while not wlan.isconnected():
        pass
print("Connected to Network")
print('IP Address:', wlan.ifconfig()[0])


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = ('', 8081)
s.bind(addr)
s.listen(1)

led_board = Pin(13, Pin.OUT)
led_board.value(0)
# measure LED state
if led_board.value() == 1:
    red_led_state = "On"
else:
    red_led_state = "Off"
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
        html_content = web_page()

        # Send the HTML content as the HTTP response
        response = f"HTTP/1.1 200 OK\nContent-Type: text/html\n\n{html_content}\n"
        client.sendall(response.encode('utf-8'))

        
s.close()
wlan.disconnect()
    
