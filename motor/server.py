# Illusion Games Server
# Copyright (C) 2021  Guillaume MODARD

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Contributors :
# Guillaume MODARD <guillaumemodard@gmail.com>

# This program has been modified for RollArt Unchain. The original version of
# Illusion Games Server can be found on https://github.com/Guillaume35/Illusion-Games-Server/

import socket, threading, re

class ServerClient(threading.Thread):
    """Accept and manage connection with a new client"""
    
    def __init__(self, server, client, addr):
        threading.Thread.__init__(self)
        self.client = client
        self.server = server
        self.alive = True
        self.addr = addr

    def _stop(self, error_level, error_msg):
 
        self.alive = False
        self.close_connection()
        self.server.client_handling_stopped(self, error_level, error_msg)

    def close_connection(self):
 
        self.alive = False
        self.client.close()
        print(f"End of communication with {self.addr}")
    
    def run(self):
        # Dialog with the client

        try:
 
            response = self.client.recv(1024)
 
            while response:
                print(response.decode("utf-8"))
                response = self.client.recv(1024)
 
        except ZeroDivisionError:
 
            self._stop('ERROR', "Zero division has been attempt")
 
        except ConnectionAbortedError:
 
            if self.alive: # unexpected aborted connection
                self._stop('ERROR', "Connection aborted")
 
            else: # manager has stoped connection
                return # we stop all process
 
        self._stop('OK', "Client has closed connection")


class Server(threading.Thread):
    """Start and manage server part"""

    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.clients = []

        self.runing = False
        self.sock = None
    
    def client_handling_stopped(self, client, error_level, error_msg):

        print(f"Le gérant de {client.addr} s'est arrêté avec le niveau d'erreur {error_level} ({error_msg})")
 
        self.clean_up()

    def log_connection_amount(self):
 
        print(f"Il y a maintenant {len(self.clients)} client(s) connecté(s)")

    def clean_up(self):
        """
        Remove all inactive clients form clients list
        """
 
        self.clients = [client for client in self.clients if client.alive]

    def run(self):
        """Initialize and start IGS"""
        
        print ("* START IGS ON %s:%s *" % (self.host, str(self.port)))
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.sock.bind((self.host, self.port))
        except socket.error:
            print ("ER: Connection with server fail")
            return 0
        
        self.sock.settimeout(0.5)
        
        print ('Ready...')

        self.running = True
        self.sock.listen(5)
        
        # Waiting for client connection
        
        while self.running:

            try:
 
                client, addr = self.sock.accept()
 
            except socket.timeout:
                continue # Continue until a client is connected
            
            # New object with that manage the client
            client_thread = ServerClient(self, client, addr)
            client_thread.start()
            
            # Save connection 
            self.clients.append(client_thread)
            
            print ("Client %s is connected (%s:%s)" % (client_thread.getName(), addr[0], addr[1]))

            #client.send (b"connected")

        for client in self.clients:
            client.close_connection()
        
        print("* IGS STOPED")

    def stop(self):

        print("* STOP IGS, CLOSE CONNECTIONS")

        self.runing = False

        # Send exit; signal
        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # sock.connect((self.host,self.port))
        # sock.send('exit;'.encode('UTF-8'))
        # sock.close()