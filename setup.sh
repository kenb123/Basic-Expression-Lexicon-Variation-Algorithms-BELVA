# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi
apt-get install -y python3-pip libqt4-dev python-qt4 qt4-dev-tools python-qt4-dev pyqt4-dev-tools
apt-get install -y python3-pyqt4 libxml2-dev libxslt1-dev zlib1g-dev
pip3 install sqlite3
pip3 install lxml
pip3 install bs4

echo -e '\n [*] Setup complete!\n'