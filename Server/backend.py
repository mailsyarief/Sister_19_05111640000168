import shlex
import os
import time
import Pyro4
import Pyro4.errors
import json
import threading


class Backend(object):

    def __init__(self):
        self.connected_device = []
        self.connected_device_thread_job = []

    @Pyro4.expose
    def connected_device_list(self):
        return 'connected device : '+', '.join(self.connected_device)

    @Pyro4.expose
    def connected_device_ls(self):
        return ','.join(self.connected_device)

    @Pyro4.expose
    def connected_device_add(self, id):
        print('register '+ id)
        self.connected_device.append(id)

    @Pyro4.expose
    def connected_device_delete(self, id):
        print('unregister '+ id)
        self.connected_device.remove(id)

    @Pyro4.expose
    def command_not_found(self):
        return "command not found"

    @Pyro4.expose
    def command_success(self):
        return "operation success"

    @Pyro4.expose
    def bye(self):
        return "bye!"

    @Pyro4.expose
    def ok(self):
        return "ok"

    @Pyro4.expose
    def fail(self):
        return "fail"

    @Pyro4.expose
    def ping_interval(self):
        return 3

    @Pyro4.expose
    def max_retries(self):
        return 100

    @Pyro4.expose
    def new_thread_job(self, id):
        t = threading.Thread(target=self.__new_thread_job, args=(id,))
        t.start()
        self.connected_device_thread_job.append(t)
        return self.ok()

    def __connect_heartbeat_server(self, id):
        time.sleep(self.ping_interval())
        try:
            uri = "PYRONAME:heartbeat-{}@localhost:7777".format(id)
            server = Pyro4.Proxy(uri)
        except:
            return None
        return server

    def __new_thread_job(self, id):
        server = self.__connect_heartbeat_server(id)
        while True:
            try:
                res = server.signal_heartbeat()
                print(res)
            except (Pyro4.errors.ConnectionClosedError, Pyro4.errors.CommunicationError) as e:
                print(str(e))
                break
            time.sleep(self.ping_interval())

    @Pyro4.expose
    def create(self,filename="",value=""):
        path = os.getcwd()
        name = filename
        filename = os.path.join(path, filename)
        f = open(filename, "w+")
        f.write(value)
        f.close()
        return "[ Nama : {}, Isi : {} ]".format(name,value)

    @Pyro4.expose
    def update(self,filename="",value=""):
        path = os.getcwd()
        name = filename
        filename = os.path.join(path, filename)
        if(os.path.exists(filename)):
            f = open(filename, "w+")
            f.write(value)
            f.close()
            return "[ Nama : {}, Isi : {} ]".format(name,value)
        else:
            return "File Tidak Ada :("

    @Pyro4.expose
    def read(self,filename=""):
        path = os.getcwd()
        filename = os.path.join(path, filename)
        if(os.path.exists(filename)):
            fd = os.open(filename, os.O_RDWR)
            ret = os.read(fd,16*1024)
            print ret
            os.close(fd)
            return ret
        else:
            return "File Tidak Ada :("

    @Pyro4.expose
    def delete(self,filename=""):
        path = os.getcwd()
        filename = os.path.join(path, filename)
        if(os.path.exists(filename)):
            os.remove(filename)
            return("Delete Berhasil :)")
        else:
            return "File Tidak Ada :("

    @Pyro4.expose
    def show(self):
        files = []
        path = os.getcwd()
        print path
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                if '.txt' in file:
                    files.append(file)

        return files

    @Pyro4.expose
    def down_my_server(self):
        time.sleep(self.ping_interval() + 1)
        return self.ok()


if __name__ == '__main__':
    k = Backend()
