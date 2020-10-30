PACKAGES_TOOLS='make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev'
PACKAGES='nginx python3 python3-pip'
sudo apt-get update
sudo apt-get install -y $PACKAGES_TOOLS
sudo apt-get install -y $PACKAGES

#APP
sudo pip3 install -r requirements.txt
. config.sh
python3 install.py

#SERVER
sudo cp server.conf /etc/nginx/conf.d/easysystems.conf
sudo cp nginx.conf /etc/nginx/nginx.conf
sudo rm /etc/nginx/sites-available/*
sudo nginx -s reload