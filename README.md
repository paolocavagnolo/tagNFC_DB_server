# tagNFC_DB_server


 1- Installare un database "server" sulla yun del techlab che si occupa del monitoraggio.

 2- Leggere quel database dalla yun collegata alla laser

 3- Aggiornare quel database da qualsiasi computer collegato alla rete del techlab


## Step eseguiti fin'ora

Per qualche motivo quantistico è stato scelto MongoDB, python edition.

    python -m pip install pymongo

si sta seguendo la guida su: https://docs.mongodb.org/getting-started/python/client/

aggiorna i file!
svn export https://github.com/paolocavagnolo/tagNFC_DB_server.git/trunk/provaDB.py --force



## Aggiornare il database direttamente dal gsheet dell'associazione (libro soci)

http://stackoverflow.com/questions/16178423/updating-mongodb-from-a-spreadsheet

## Creare rete wifi per macchinari

https://wiki.openwrt.org/doc/recipes/routedclient

## Inserire un IP fisso alla yun

    vi /etc/config/network
    config interface 'lan'
	      #option proto 'dhcp'
        option proto 'static'
        option ipaddr '192.168.1.150'
        option netmask '255.255.255.0'
	      option gateway   '192.168.1.1'

    /etc/init.d/network reload
