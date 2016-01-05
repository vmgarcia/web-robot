# web-robot

This is code for an internet controlled robot. Uses raspberry pi camera to stream video over the internet.

To run on raspberry pi make sure camera is installed and enabled correctly.

Get IP address with <code>hostname -I</code> this is the address of the website with the video feed and controls

Instructions to get code working (sudo needed because gpio pins require super user)

<code>sudo pip install -r requirements.txt</code>

<code>sudo python control_server.py &</code>

<code>sudo python app.py</code>

Credit to Miguel Grinberg for his awesome tutorial on streaming video with flask. 

Credit to Stephen C Phillips for code to control the stepper motors. 
