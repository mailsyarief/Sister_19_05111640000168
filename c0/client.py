import Pyro4
import base64
import json
import sys

namainstance = "fileserver"

def get_backend_object():
    uri = "PYRONAME:{}@localhost:7777" . format(namainstance)
    fserver = Pyro4.Proxy(uri)
    return fserver

if __name__=='__main__':
    f = get_backend_object()
    f.create('slide1.txt')

    print(f.list())

    # #kembalikan ke bentuk semula ke dalam file name slide1-kembali.pdf
    # open('slide1-kembali.pdf','w+b').write(base64.b64decode(d['data']))
    #
    # k = f.read('slide2.pptx')
    # #kembalikan ke bentuk semula ke dalam file name slide2-kembali.pptx
    # open('slide2-kembali.pptx','w+b').write(base64.b64decode(k['data']))


