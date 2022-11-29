import socket

s = socket.socket()
s.connect(("127.0.0.1", 3018))  

content = "今天过得还好吗？"
s.send(content.encode())  # 发送编码后的内容
content = "exit"
s.send(content.encode())
recive_content = s.recv(1024).decode()  
print(recive_content)
s.close()
