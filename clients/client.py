import Pyro4
import sys

if len(sys.argv) > 1:
    namainstance = sys.argv[1]
else:
    namainstance = "fileserver0"

def get_fileserver_object():
    uri = "PYRONAME:{}@localhost:7777" . format(namainstance)
    fserver = Pyro4.Proxy(uri)
    fserver.pyro_connect()
    return fserver

if __name__ == '__main__':

    s = get_fileserver_object()
    file = ""
    while True:
        print("1. Create | 2. Read | 3. Update | 4. Delete | 5. List | 0. Exit")
        cmd = raw_input("Pilih Opsi : ")
        if(cmd == '1'):
            filename = raw_input("Nama File : ")
            isi = raw_input("Isi : ")
            print '\n'
            print s.create(filename, isi)
            print '\n'

        elif(cmd == '2'):
            filename = raw_input("Nama File : ")
            print '\n'
            print s.read(filename)
            print '\n'

        elif(cmd == '3'):
            filename = raw_input("Nama File : ")
            value = raw_input("Isi : ")
            print '\n'
            print s.update(filename, value)
            print '\n'

        elif(cmd == '4'):
            filename = raw_input("Nama File : ")
            print '\n'
            print s.delete(filename)
            print '\n'

        elif (cmd == '5'):
            print '\n'
            print '\n'.join(s.list())
            print '\n'

        elif(cmd == '0'):
            print "Exit"
            exit()
        else:
            print("Wrong Input")
