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
