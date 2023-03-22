import socket
from threading import Thread

BUFFER_SIZE = 1024

class Server():
    def __init__(self):
        #---------------------------------------------
        # TODO： 初始化服务端socket
        self.server=socket.socket()
        #---------------------------------------------
        self.ip = "127.0.0.1"         # 服务器IP为local host，即本机
        self.port = self.set_port()   # 通过命令行标准输入，设置服务器端口

        #---------------------------------------------
        # TODO： 为服务socket绑定IP与端口
        # self.server.XXXXXXXX(params)
        self.server.bind((self.ip,self.port))
        #---------------------------------------------
        self.mode = self.get_mode()

        #---------------------------------------------
        # TODO： 设置服务端默认timeout时间(必须有)
        # self.server.XXXXXXXX(params)
        self.server.settimeout(None)
        #---------------------------------------------
        self.max_clients = self.set_max_clients()  

        #---------------------------------------------
        # TODO： 设置服务端最大连接的客户端数量(必须有)
        # self.server.XXXXXXXX(params)
        self.server.listen(self.max_clients)
        #---------------------------------------------


        if self.mode == 'p2p':
            # 必做：实现p2p聊天
            self.start_p2p_listen()
        else:
            # 选做：实现聊天室服务器功能
            self.ip_client = {}
            self.start_hub_listen()

    def set_port(self):
        print("请输入聊天服务器端口")
        port = input()
        return int(port)

    def get_mode(self):
        print("请输入服务器工作模式(p2p,hub)")
        mode = input()
        return mode

    def set_max_clients(self):
        print("请输入最大允许连接的客户端数量")
        max_clients = input()
        return int(max_clients)

    ################################################################################
    # 工作方式1：p2p连接服务器
    def start_p2p_listen(self):
        #---------------------------------------------
        # TODO： 等待建立连接(必须有), 当用户连接时打印消息，如(ip, port)已成功连接
        # 提示：需要循环结构
        # self.server.XXXXXXXX(params)
        #---------------------------------------------
        cli,add=self.server.accept()
        print(str(add)+'已成功连接')
        #---------------------------------------------
        # TODO： 为接受消息和发送消息分别开启两个线程，实现双工聊天
        # 此处仅需替换param位置的参数；根据上一个位置的返回值仅需更改
        Thread(target=self.p2p_send_msg,args=(cli,)).start()
        Thread(target=self.p2p_recv_msg,args=(cli,)).start()
        #---------------------------------------------


    def p2p_send_msg(self,client):
        #---------------------------------------------
        # TODO： 实现发送消息功能
        # 提示1：字符串必须先encode才能发送
        # 提示2：获得标准输入参考本例程其他函数
        # 提示3：需要循环结构
        # 提示4：当recv_msg收到用户退出通知，并关闭socket后，此子进程会报错，需要通过try except进行异常处理
        #---------------------------------------------
        while(True):
            try:
                # 可能报错的语句
                msg=str(client.getsockname())+': '+input()
                client.send(msg.encode('utf-8'))
            except:
                # 如果报错了，则执行下面的内容（退出循环）
                break
    
    def p2p_recv_msg(self,client):
        #---------------------------------------------
        # TODO： 实现接受消息功能，客户端发送q则退出，并打印退出消息，如(ip, port)已退出聊天
        # 提示1：接收到的消息必须先decode才能转换为字符串
        # 提示2：打印到标准输出参考本例程其他函数
        # 提示3：需要循环结构
        #---------------------------------------------
        while(True):
            msg=client.recv(BUFFER_SIZE)
            msg=msg.decode('utf-8')
            if(msg=='q'):
                print(str(client.getpeername())+':'+' 已退出聊天')
                break
            else:
                print(str(client.getpeername())+':'+msg)

        ################################################################################
        # 工作方式2：hub聊天室服务器（广播各个用户发送的信息）

    def start_hub_listen(self):
        # ---------------------------------------------
        # 选做
        # TODO： 等待建立连接(必须有), 当用户连接时打印消息，如(ip, port)已成功连接
        # 提示1：需要循环结构
        # 提示2：推荐使用字典数据格式，利用self.ip_client将(ip,port)与client的键值对进行保存，方便管理多个用户
        # 提示3：在循环结构中，每个用户连接后利用此命令开启进程Thread(target=self.hub_msg_process,args=(parm1,parm2 self.ip_client)).start()
        # 提示4：各个线程之间不会对传入参数进行拷贝，因此ip_client会由主线程动态更新
        # self.server.XXXXXXXX(params)
        # ---------------------------------------------
        while(True):
            cli,add=self.server.accept()
            self.ip_client[cli]=add
            print(str(add)+"已成功连接")
            Thread(target=self.hub_msg_process, args=(cli, add ,self.ip_client)).start()


    def hub_msg_process(self, current_client, current_address, ip_client):
        # ---------------------------------------------
        # 选做
        # TODO： 接受当前client发送的消息，并广播给其他所有client；当某一用户发送q时，退出该用户，并将其退出消息广播至其他所有用户
        # 提示1：需要循环结构
        # 提示2：需要调用self.hub_close_client函数退出用户线程并实现上述退出消息广播至其他所有用户的功能
        # 提示3：利用ip_client字典进行广播；for key, value in ip_client.items()；广播时，不能广播到自己
        # ---------------------------------------------
        while(current_client in ip_client):
            msg=current_client.recv(BUFFER_SIZE)
            msg=msg.decode('utf-8')
            if(msg=='q'):
                msg=str(current_address)+"已退出"
                self.hub_close_client(current_client,current_address)
            else:
                msg=str(current_address)+': '+msg
            for key, value in ip_client.items():
                if(key!=current_client):
                    key.send(msg.encode('utf-8'))



    def hub_close_client(self, client, address):
        # ---------------------------------------------
        # 选做
        # TODO： 关闭该客户socket连接，将其退出消息广播至所有其他在线用户
        # 提示：从字典中删除元素:del(ip_client[key])
        # ---------------------------------------------
        client.close()
        del(self.ip_client[client])


if __name__ == '__main__':
    server = Server()
    