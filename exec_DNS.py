#!/usr/bin/env python
from dnslib import *
#from IPy import IP
import threading, operator, time
import SocketServer, socket, sys, os
import imp
ovsDB = imp.load_source('ovsDB', '/home/faucet/ryu/ryu/app/my_ovs_db.py')
import binascii


class DNSHandler():
    def fakeResponse(self, data, dominio, ip):
        packet=''
        if dominio:
            packet+=data[:2] + "\x81\x80"
            packet+=data[4:6] + data[4:6] + '\x00\x00\x00\x00'   # Questions and Answers Counts
            packet+=data[12:]                                         # Original Domain Name Question
            packet+='\xc0\x0c'                                             # Pointer to domain name
            packet+='\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'             # Response type, ttl and resource data length -> 4 bytes
            packet+=str.join('',map(lambda x: chr(int(x)), ip.split('.'))) # 4bytes of IP
        return packet

    def parse(self,data,client_address):
        ip_src = ""
        if client_address:
            if client_address[0]:
                ip_src = client_address[0]
        response = ""

        qname=""

        try:
            # Parse data as DNS
            d = DNSRecord.parse(data)
            qname = str(d.q.qname)
            print '[',qname,']'
        except Exception, e:
            print "[%s] %s: ERROR: %s" % (time.strftime("%H:%M:%S"), self.client_address[0], "Invalid DNS request")

        else:
            if qname=="prodaptive-net.com.":
                print "Faking"
                response =self.fakeResponse(data,qname, "192.168.163.130")
            elif ip_src:
            #response =self.fakeResponse(data,qname, "192.168.163.44")
                mydb = ovsDB.Ovsdb()
                print "Checking ",ip_src
                if mydb.isTrustedPCbyIP(ip_src):
                    response = self.proxyrequest(data)
                else:
                    print "Faking"
                    response =self.fakeResponse(data,qname, "192.168.163.130")
            else:
                print "Faking"
                response =self.fakeResponse(data,qname, "192.168.163.130")
        return response

# Obtain a response from a real DNS server.
    def proxyrequest(self, request, port="53"):
        print "proxyreq"
        reply = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(3.0)
            # Send the proxy request to a randomly chosen DNS server
            sock.sendto(request, ('192.168.137.2', int(port)))
            reply = sock.recv(1024)
            sock.close()

        except Exception, e:
            print "[!] Could not proxy request: %s" % e
        else:
            return reply

# UDP DNS Handler for incoming requests
class UDPHandler(DNSHandler, SocketServer.BaseRequestHandler):
    #def setup(self):
    #    print "starting a new UDPHandler"
    #    print self.server.mydb.getVersion()
         
    def handle(self):
        #print self.client_address
        (data,socket) = self.request
        response = self.parse(data,self.client_address)

        if response:
            socket.sendto(response, self.client_address)
    def finish(self):
        print "Terminating an UDPHandler"
         

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):

    # Override SocketServer.UDPServer to add extra parameters
    def __init__(self, server_address, RequestHandlerClass):
      
        self.address_family =  socket.AF_INET
        # mydb is not thread safe, so cannot use.
        #self.mydb = ovsdb.Ovsdb()
        #self.trustedPC = {}
        SocketServer.UDPServer.__init__(self,server_address,RequestHandlerClass)            


try:
        
	server = ThreadedUDPServer(("0.0.0.0", 53), UDPHandler)

    # Start a thread with the server -- that thread will then start one
    # more threads for each request
	print "Starting server"
	server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
	server_thread.daemon = True
	server_thread.start()

        # Loop in the main thread
	while True: time.sleep(100)

except (KeyboardInterrupt, SystemExit):
    server.shutdown()
    print "[*] DNS Proxy is shutting down."
    sys.exit()
