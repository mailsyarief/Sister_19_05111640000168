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
connected = True
connected_device = []

def client_create(filename,value):
    res = server.create(filename,value)
    res.wait(2)
    print '\n'
    print(res.value)
    print '\n'

def client_read(filename):
    res = server.read(filename)
    res.wait(2)
    print '\n'
    print(res.value)
    print '\n'

def client_update(filename,value):
    res = server.update(filename,value)
    res.wait(2)
    print '\n'
    print(res.value)
    print '\n'

def client_delete(filename):
    res = server.delete(filename)
    res.wait(2)
    print '\n'
    print(res.value)
    print '\n'

def client_show():
    res = server.show();
    res.wait(2)
    print '\n'
    print '\n'.join(res.value)
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

# ===============================
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

def job_heartbeat_failure_all_to_all(id):
    server_heartbeat = get_server('heartbeat-{}'.format(id))
    while True:
        try:
            summary = server_heartbeat.get_summary_heartbeat(id)
            summary = summary.split(',')
            if summary[1] == 'none':
                pass
            else:
                if time.time() - float(summary[2]) > 2*interval:
                    print("\n{} is down [DETECT BY all heartbeat]\n> ".format(id))
                    # break
            time.sleep(interval)
        except:
            # print("\n{} is down [DETECT BY all heartbeat]\n> ".format(id))
            break

def expose_function_heartbeat(heartbeat, id):
    __host = "localhost"
    __port = 7777
    daemon = Pyro4.Daemon(host = __host)
    ns = Pyro4.locateNS(__host, __port)
    uri_server = daemon.register(heartbeat)
    ns.register("heartbeat-{}".format(id), uri_server)
    daemon.requestLoop()

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
                print("\nSERVER DOWN ( DETECT BY PING ACK )")
                break
        time.sleep(interval)
    gracefully_exits()

def get_connected_device_from_server():
    try:
        conn_device = server.connected_device_ls()
        conn_device.ready
        conn_device.wait(1)
        conn_device = clear_connected_device(conn_device.value.split(','), id)
    except:
        return None
    return conn_device

def job_ping_server_ping_ack():
    t = threading.Thread(target=ping_server)
    t.start()
    return t

def register_new_clients(heartbeat):
    while True:
        conn_device = get_connected_device_from_server()
        all_to_al_heartbeat_job(heartbeat, conn_device)
        time.sleep(interval)

def job_check_updated_device_from_server(heartbeat):
    t = threading.Thread(target=register_new_clients, args=(heartbeat,))
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
        if device not in connected_device:
            connected_device.append(device)
            heartbeat.new_thread_job(device)

            t1 = threading.Thread(target=job_heartbeat_failure_all_to_all, args=(device,))
            t1.start()

if __name__=='__main__':

    # core
    server = get_server('server')
    try:
        interval = server.ping_interval()
    except:
        print('server not running')
        sys.exit(0)
    server._pyroTimeout = interval
    server._pyroAsync()

    # device id
    id = str(uuid.uuid4())
    print('---------- registered id : {}'.format(id))
    #COMMENT DARI SINI
    # register device on server (heartbeat)
    server.connected_device_add(id)

    heartbeat, thread_heartbeat, thread_heartbeat_detector = job_heartbeat()
    thread_ping_ack = job_ping_server_ping_ack()

    # register failure detector on server
    server.new_thread_job(id)

    conn_device = get_connected_device_from_server()

    all_to_al_heartbeat_job(heartbeat, conn_device)

    thread_get_connected_device_list = job_check_updated_device_from_server(heartbeat)
    # COMMENT SAMPE SINI
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