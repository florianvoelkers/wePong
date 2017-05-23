import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ""#socket.gethostname()
port=5000
s.bind((host,port))

s.listen(5)

while True:
    c,addr = s.accept()
    print("Got connection",addr)
    data = c.recv(1024)
    print ("got data",data)
    c.send("Thank you for connecting") 
    c.close()
