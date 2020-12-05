# RpiCanServer
Raspberry PI CAN Server example using: MCP2515 CAN Module, Django server y python-can libraries.

Spanish tutorial:
https://youtu.be/43H0YiSZ-4M

English tutorial:
comming soon

# Objective
The goal for this project is to give an real quick example how to setup a functional CAN capable device.

# Deployment
You can setup this project on a Raspberry Pi device using a MCP2515 (throught SPI). You can also deploy on any other machine, but you need a CAN controller and transceiver in order to communicate with a CAN network (check python-can compatible modules).If you have a few raspberry devices to play around you can use the Demo 1 but if you want a more practical example you can follow the Demo 2. Be aware, in order to communicate with an automotive device using a diagnostic protocol then a trasport and application layers are needed, check-out UDS (ISO-14229) or OBD-II standards.

<b>Demo 1:<br/></b>
&ensp;RPI<br/>
&ensp;&ensp;CanApp<br/>
&ensp;&ensp;&ensp;Python-can<br/>
&ensp;&ensp;&ensp;&ensp;MCP2515<br/>
&ensp;&ensp;&ensp;&ensp;&ensp;||<br/>
&ensp;&ensp;&ensp;&ensp;&ensp;|| CAN Network<br/>
&ensp;&ensp;&ensp;&ensp;&ensp;||<br/>
&ensp;&ensp;&ensp;&ensp;&ensp;||<br/>
&ensp;&ensp;&ensp;&ensp;MCP2515<br/>
&ensp;&ensp;&ensp;Python-can<br/>
&ensp;&ensp;CanApp<br/>
&ensp;RPI<br/>

<b>Demo 2:<br/></b>
&ensp;RPI<br/>
&ensp;&ensp;CanApp<br/>
&ensp;&ensp;&ensp;Python-can<br/>
&ensp;&ensp;&ensp;&ensp;MCP2515<br/>
&ensp;&ensp;&ensp;&ensp;&ensp;||<br/>
&ensp;&ensp;&ensp;&ensp;&ensp;|| CAN Network<br/>
&ensp;&ensp;&ensp;&ensp;&ensp;||<br/>
&ensp;&ensp;&ensp;&ensp;&ensp;||===== Automotive Module<br/>
&ensp;&ensp;&ensp;&ensp;&ensp;||<br/>
&ensp;&ensp;&ensp;&ensp;&ensp;||===== |VN1611|== Vector software tool<br/>
&ensp;&ensp;&ensp;&ensp;&ensp;||<br/>
          
# RPI deployment instructions
For the moment you have to follow these instructions manually:

<b>At your development computer:</b><br/>

#Copy your deployment files to the raspberry<br/>
scp -r LocalCanappDeployFolder pi@10.0.0.100.someDirectory:canapp<br/>

<b>At the raspberry:</b><br/>

#update the rpi<br/>
sudo apt-get update<br/>
sudo apt-get upgrade<br/>

#verify python3 is installed<br/>
python3 --version<br/>

#install pip3<br/>
sudo apt-get install -y python3-pip<br/>

#install virtual enviroment<br/>
sudo pip3 install virtualenv<br/>

#navigate to copied files<br/>
cd ~/canapp/<br/>

#create virtual enviroment and start it<br/>
virtualenv venv && source venv/bin/activate<br/>

#install python-can library and django<br/>
pip3 install python-can django<br/>

#init server<br/>
python3 manage.py makemigrations<br/>
python3 manage.py migrate<br/>
python3 manage.py runserver 0:8000<br/>

#Add to bootup (on session startup, if needed)<br/>
sudo nano /etc/profile<br/>
#Add to file (libraries should have been installed in regular enviroment, nor virtual):<br/>
@sudo python3 ~/canapp/manage.py runserver 0:8000<br/>
