import time
from machine import Pin, PWM

import motor
import network

ssid = 'OWEN'
password = '123456789'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)
while not ap.active():
    pass
print('network config:', ap.ifconfig())

# Configure the socket connection
# over TCP/IP
import socket

# AF_INET - use Internet Protocol v4 addresses
# SOCK_STREAM means that it is a TCP socket.
# SOCK_DGRAM means that it is a UDP socket.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',80))
s.listen(1)

# Function for creating the web page to be displayed

def web_page():

    html_page = """    
    <html>    
    <head>    
      <meta name="viewport" content="width=device-width, initial-scale=.5, maximum-scale=1, user-scalable=no">   
    </head>    
    <body>    
     <center><h1> Pinata Bot </h1></center>    
     <center>
    <center><h2>Position:</h2></center>
    <center><h2 id="Position">Stop</h2></center>

   <input type="text" id="Motor" value="0">

<div id="DPAD">
    <input id="UP" type="button" onpointerdown="Move('Forward')" onpointerup="Move('Stop')" value="^">
    <input id="DOWN" type="button" onpointerdown="Move('Backward')" onpointerup="Move('Stop')" value="v">
    <input id="LEFT" type="button" onpointerdown="Move('Left')" onpointerup="Move('Stop')" value="<">
    <input id="RIGHT" type="button" onpointerdown="Move('Right')" onpointerup="Move('Stop')" value=">">
    <input id="CENTER" type="button">
</div>
      
     </center>      
    </body>
    <style>
body{

background-color: green;

}

h1{
font-size:80px;
}

h2{
font-size:60px;
}


#DPAD{
    width: 250px;
    height: 250px;
    background-color: darkgray;
   
    margin-top: 250px;
    margin-left: -250px;
}

#DPAD input{
    width: 250px;
    height: 250px;
    background-color: darkgray;
    position: absolute;
    text-align: center;
    font-size: 100px;
    border: solid 20px black;
}

#DPAD input:active{
    background-color: grey;
}

#UP{
    margin-top: -230px;
}

#DOWN{
    margin-top: 230px;
}

#LEFT{
    margin-left: -230px;
}

#RIGHT{
    margin-left: 230px;
}

#Motor{
    visibility: hidden;
}
    </style>
    <script>
    
 const Move = (value) => {
    document.getElementById("Motor").value = value 
    const motor = document.getElementById("Motor").value;
    document.getElementById("Position").textContent = value;
    const xhttp = new XMLHttpRequest();
    xhttp.open('GET', '/motor/'+ motor, true)
    xhttp.send();   
    
    }                 

    </script>
    </html>"""  
    return html_page   

while True:
    
    # Socket accept() 
    conn, addr = s.accept()
    
    print("")
    print("Got connection from %s" % str(addr))
    
    # Socket receive()
    request=conn.recv(1024)
    
    # Socket send()
    request = str(request)
    move = request.find('/motor/')
    
    if move == 6:
        
        split_request = request.split()
        split2_request = split_request[1].split('/')
        data = split2_request[2]
        print("Sequence:")
        
        if data == "Forward":
            print(data)
            motor.forward()
            position = data
            
        elif data == "Backward":
            print(data)
            motor.backward()
            position = data
            
        elif data == "Left":
            print(data)
            motor.left()
            
        elif data == "Right":
            print(data)
            motor.right()
            
        elif data == "Stop":
            print(data)
            motor.stop_all()
        else:
            print(data + "?")
            motor.stop_all()
    
    position = "test"
    
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n') 
    conn.sendall(response)
   
    # Socket close()
    conn.close()
