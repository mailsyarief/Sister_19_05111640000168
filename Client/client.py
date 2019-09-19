import Pyro4
import os
import numpy as np

uri = "PYRONAME:maile@localhost:7777"

def client_create(filename,value):
    server = Pyro4.Proxy(uri)
    print '\n'
    print(server.create(filename,value))
    print '\n'

def client_read(filename):
    server = Pyro4.Proxy(uri)
    print '\n'
    print(server.read(filename))
    print '\n'

def client_update(filename,value):
    server = Pyro4.Proxy(uri)
    print '\n'
    print(server.update(filename,value))
    print '\n'

def client_delete(filename):
    server = Pyro4.Proxy(uri)
    print '\n'
    print(server.delete(filename))
    print '\n'

def client_show():
    server = Pyro4.Proxy(uri)
    print '\n'
    print '\n'.join(server.show())
    print '\n'

def client_send(filename):
    name = filename
    path = os.getcwd()
    filename = os.path.join(path, filename)

    if (os.path.exists(filename)):
        fd = os.open(filename, os.O_RDWR)
        ret = os.read(fd, 16 * 1024)
        os.close(fd)
        client_create(name,ret)
    else:
        print "File Tidak Ada :("


if __name__=='__main__':
    file = ""
    while True:
        print("1. Create | 2. Read | 3. Update | 4. Delete | 5. Show | 6. Send | 0. Exit")
        cmd = raw_input("Pilih Opsi : ")
        if(cmd == '1'):
            filename = raw_input("Nama File : ")
            value = raw_input("Isi : ")
            client_create(filename,value)
        elif(cmd == '2'):
            filename = raw_input("Nama File : ")
            client_read(filename)
        elif(cmd == '3'):
            filename = raw_input("Nama File : ")
            value = raw_input("Isi : ")
            client_update(filename,value)
        elif(cmd == '4'):
            filename = raw_input("Nama File : ")
            client_delete(filename)
        elif (cmd == '5'):
            client_show()
        elif (cmd == '6'):
            filename = raw_input("Nama File : ")
            client_send(filename)
        elif(cmd == '0'):
            print("Exit")
            exit()
        else:
            print("Wrong Input")