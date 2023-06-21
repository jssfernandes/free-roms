Garantir que o python e o pip estejam breviamente instalados


Download do client para utilizar a base de dados oracle
wget https://download.oracle.com/otn_software/nt/instantclient/218000/instantclient-basic-windows.x64-21.8.0.0.0dbru.zip
Criar uma pasta no C:\ com o nome de oracle
Fazer a extracao dos arquivos do client que fez o download no diretorio C:\oracle
Adicionar ao PATH do usuario ou do sistema o caminho do client
SET PATH=C:\oracle\instantclient_21_8;%PATH%
Criar a variavel de ambiente TNS_ADMIN e atribuir a ela a localizacao do client da oracle conforme o exemplo abaixo
SET X TNS_ADMIN=C:\oracle\instantclient_21_8


Fazer a instalacao dos pacotes do projeto
pip3 install -r requirements.txt

