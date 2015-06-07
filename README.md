# python-lg
Python script for remote control with LG Smart TV

We need TV and Raspberry Pi or someone linux device or computer on the same network.
Using Raspberry Pi we can then SSH from anywhere and remotely control the TV.

First time we run the python script, TV will display the pair key.
The script is run with the next command:

	python3 lg.py

When the pairing key is displayed in TV, we need modify script editing this line with our pair key.

	lgtv["pairingKey"] = "099999"

Finally we only need run the script passing a command number as a parameter. May be possible enter 1 or more commands at the same time.

	python3 lg.py <cmd1> <cmd2> <cmd3> <cmd(n)>

Here some examples, first volume up and second volume down 2 points

	python3 lg.py 24
	python3 lg.py 25 25 
	
NOTE: If we don't enter any command number, the list of avaliables commands will be displayed.