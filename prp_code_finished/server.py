import socket
import time
import serial
if __name__ == '__main__':
    sk = socket.socket()
    ip_port = ('192.168.1.110', 8888)
    sk.bind(ip_port)
    sk.listen(5)
    port = '/dev/ttyACM0'  
    baud_rate = 9600
    ser = serial.Serial(port, baud_rate, timeout=1)  
    ser.flushInput()  
    ser.flushOutput()
    time.sleep(1)
    
    while True:
        print("waiting......")
       	conn, address = sk.accept()
	msg = "socket connected"
        conn.send(msg.encode())
	data = conn.recv(1024)
        print(data.decode())
        data_list=list(data.decode())
        for i in data_list:
            if i>='0' or i<'10' and i!=' ' and i !='\n':
                print(int(i))
                cmd=int(i)
                if 0 <= cmd <= 10: 
                    ser.write(str(cmd).encode()) 
                    time.sleep(1)
                    msg = ser.read(ser.in_waiting).decode()
                    if msg:
                       print(msg)   
        ##conn.close()
