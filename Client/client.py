import Pyro4
import Pyro4.errors
import time
import threading
import os
import sys
import uuid
from heartbeat import Heartbeat

id = None
interval = 0
server = None
connected = True

def client_create(filename,value):
    print '\n'
    print(server.create(filename,value))
    print '\n'

def client_read(filename):
    print '\n'
    print(server.read(filename))
    print '\n'

def client_update(filename,value):
    print '\n'
    print(server.update(filename,value))
    print '\n'

def client_delete(filename):
    print '\n'
    print(server.delete(filename))
    print '\n'

def client_show():
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


def get_server(id):
    try:
        uri = "PYRONAME:{}@localhost:7777".format(id)
        gserver = Pyro4.Proxy(uri)
        return gserver
    except:
        gracefully_exits()

def job_heartbeat():
    global id
    heartbeat = Heartbeat(id)
    t1 = threading.Thread(target=job_heartbeat_failure, args=(heartbeat,))
    t1.start()

    t = threading.Thread(target=expose_function_heartbeat, args=(heartbeat, id,))
    t.start()
    return heartbeat, t, t1

def job_heartbeat_failure(heartbeat):
    while True:
        if time.time() - heartbeat.last_received > 2*interval:
            print("\nserver is down [DETECT BY heartbeat]")
            break
        time.sleep(interval)
    gracefully_exits()

def expose_function_heartbeat(heartbeat, id):
    __host = "localhost"
    __port = 7777
    daemon = Pyro4.Daemon(host = __host)
    ns = Pyro4.locateNS(__host, __port)
    uri_server = daemon.register(heartbeat)
    ns.register("maile-{}".format(id), uri_server)
    daemon.requestLoop()


def job_heartbeat_failure(heartbeat):
    while True:
        if time.time() - heartbeat.last_received > 2*interval:
            print("\nserver is down [DETECT BY heartbeat]")
            break
        time.sleep(interval)
    gracefully_exits()


def communicate():
    try:
        res = server.ok()
        if res.value == 'ok':
            pass
    except:
        return False
    return True

def ping_server():
    global connected
    while True and connected:
        alive = communicate()
        if not alive:
            alive = communicate()
            if not alive:
                print("\nserver is down [DETECT BY ping ack]")
                break
        time.sleep(interval)
    gracefully_exits()

def job_ping_server_ping_ack():
    t = threading.Thread(target=ping_server)
    t.start()
    return t

def gracefully_exits():
    # unregister device on server
    server.connected_device_delete(id)
    print("disconnecting..")
    time.sleep(0.5)
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

def clear_connected_device(devices, id):
    if id in devices:
        devices.remove(id)
    return devices

def all_to_al_heartbeat_job(heartbeat, devices):
    for device in devices:
        heartbeat.new_thread_job(device)

if __name__=='__main__':

    # device id
    id = str(uuid.uuid4())
    print('---------- registered id : {}'.format(id))
    # core
    server = get_server('maile')
    try:
        interval = server.ping_interval()
    except:
        print('server not running')
        sys.exit(0)
    server._pyroTimeout = interval
    server._pyroAsync()


    # register device on server (heartbeat)
    server.connected_device_add(id)

    heartbeat, thread_heartbeat, thread_heartbeat_detector = job_heartbeat()
    thread_ping_ack = job_ping_server_ping_ack()

    # register failure detector on server
    server.new_thread_job(id)

    conn_device = server.connected_device_ls()
    conn_device.ready
    conn_device.wait(1)
    conn_device = clear_connected_device(conn_device.value.split(','), id)

    all_to_al_heartbeat_job(heartbeat, conn_device)


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

    connected = False
    thread_ping_ack.join()
    # thread_heartbeat.join()
    # thread_heartbeat_detector.join()
    gracefully_exits()