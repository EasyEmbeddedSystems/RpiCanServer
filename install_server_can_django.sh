#windows arp -a to check list of clients
#scp -r LocalCanappFolder pi@192.168.1.yyy:canapp

#update the rpi
sudo apt-get update
sudo apt-get upgrade

#verify python3 is installed
python3 --version

#install pip3
sudo apt-get install -y python3-pip

#install virtual enviroment
sudo pip3 install virtualenv 

#navigate to copied files
cd ~/canapp/

#create virtual enviroment and start it
virtualenv venv && source venv/bin/activate

#install python-can library and django
pip3 install python-can django

#init server
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0:8000

#Add to bootup (on session startup)
sudo nano /etc/profile
#Add to file (libraries should have been installed in regular enviroment, nor virtual):
@sudo python3 ~/canapp/manage.py runserver 0:8000



















