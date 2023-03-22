import socket
from threading import Thread

BUFFER_SIZE = 1024


class Client():
    def __init__(self):
        # ---------------------------------------------
        # TODO： 初始化客户端socket
        self.client = socket.socket()
        # ---------------------------------------------
        self.ip, self.port = self.set_ip_port()  # 通过命令行标准输入，设置服务器IP与端口

    def set_ip_port(self):
        print("请输入聊天服务器IP")
        ip = input()
        #ip = "127.0.0.1"
        print("请输入聊天服务器端口")
        port = input()
        return ip, int(port)

    def start_connection(self):
        # ---------------------------------------------
        # TODO： 通过socket连接至对应IP与端口
        # self.client.XXXXXXX
        self.client.connect((self.ip, self.port))
        # ---------------------------------------------
        print("与" + self.ip + "连接建立成功，可以开始聊天了！（输入q断开连接）")
        # 为接受消息和发送消息分别开启两个线程，实现双工聊天
        Thread(target=self.send_msg).start()
        Thread(target=self.recv_msg).start()

    def send_msg(self):
        # ---------------------------------------------
        # TODO： 在本函数中实现Socket消息的接收，并实现输入q退出的功能
        # 提示：需要循环结构
        while (True):
            msg=input()
            self.client.send(msg.encode('utf-8'))
            if msg=='q':
                self.client.close()
                break
        # ---------------------------------------------

    def recv_msg(self):
        # ---------------------------------------------
        # TODO： 在本函数中实现Socket消息的接收
        # 提示：需要循环结构
        # 提示：send_msg子进程退出并关闭socket时会报错，因此需要用try except结构进行异常处理
        # ---------------------------------------------
        while(True):
            try:
                #
                msg = self.client.recv(BUFFER_SIZE)
                msg=msg.decode('utf-8')
                print(msg)
            except:
                # 如果报错了，则执行下面的内容（退出循环）
                break


if __name__ == '__main__':
    client = Client()
    client.start_connection()
