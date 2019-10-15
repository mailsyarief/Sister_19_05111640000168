from backend import *
import Pyro4

def server():
    #JALANIN NAMESERVER LOCAL  pyro4-ns -n localhost -p 7777
    # --- start
    # pyro4-ns -n localhost -p 7777

    # --- list
    # pyro4-nsc -n localhost -p 7777 list
    __host = "localhost"
    __port = 7777
    server = Backend()
    daemon = Pyro4.Daemon(host = __host)
    ns = Pyro4.locateNS(__host, __port)
    uri_server = daemon.register(server)
    print("URI server : ", uri_server)
    ns.register("server", uri_server)
    daemon.requestLoop()


if __name__ == '__main__':
    server()

