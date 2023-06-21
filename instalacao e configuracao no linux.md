Atualizar os pacotes e fazer o upgrade
sudo apt update && sudo apt upgrade

instalar o zip e o unzip
sudo apt install zip unzip

Garantir que o python e o pip estejam breviamente instalados
sudo apt install python3
sudo apt install python3-pip

instalar o certbot-auto
sudo apt-add-repository ppa:certbot/certbot
sudo apt install certbot
certbot --version

Download do client para utilizar a base de dados oracle
wget https://download.oracle.com/otn_software/linux/instantclient/219000/instantclient-basic-linux.x64-21.9.0.0.0dbru.zip
Criar uma pasta no /opt com o nome de oracle
sudo mkdir /opt/oracle
Fazer a extracao dos arquivos do client que fez o download no diretorio /opt/oracle
Criar a variavel de ambiente LD_LIBRARY_PATH e atribuir a ela a localizacao do client da oracle conforme o exemplo abaixo
export LD_LIBRARY_PATH=/opt/oracle/instantclient_21_9:$LD_LIBRARY_PATH
Depois instalr o pacote libaio
sudo apt install libaio1 libaio-dev

Fazer a instalacao dos pacotes do projeto
pip install -r requirements.txt

Depois crair o diretorio e da a permissao para o usuario de execusao , conforme o exemplo
sudo mkdir /var/run/gunicorn
sudo chown ubuntu /var/run/gunicorn







NO WSL2
https://www.linuxtopic.com/2021/11/system-has-not-been-booted-with-systemd.html
sudo apt-get install -yqq daemonize dbus-user-session fontconfig
Add these lines to the /etc/wsl.conf (note you will need to run your editor with sudo privileges, e.g: sudo nano /etc/wsl.conf) :
[boot]
systemd=true


Thanks to @gmegidish I came to the solution which worked for me:

unset PYTHON_INSTALL_LAYOUT
sudo rm -rf /opt/eff.org/certbot/
pip install cryptography interface
./certbot-auto renew -v --debug
/opt/letsencrypt/letsencrypt-auto --help (testing if it works)