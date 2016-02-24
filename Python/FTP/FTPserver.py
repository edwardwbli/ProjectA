# -*- coding: utf-8 -*-
import time  
import socket,sys  
from thread import *  
import os  
__author__ = 'ksp'  
  
  
class FTPs():  
    def __init__(self,localip='127.0.0.1',path='c:/'):#接受本机ip以绑定socket，接受开放的目录  
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
        self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  
        #这是传输时分片的大小  
        self.PSIZE=4096  
        self.lip=localip  
        #绑定到FTP专用端口，21  
        try:  
            self.s.bind((self.lip,21))  
        except:  
            print 'ip error'  
            raise  
        self.path=path  
        #将工作目录改变到所设目录下  
        try:  
            os.chdir(path)  
        except ValueError:  
            print 'path Invalid'  
            raise  
        self.close=False  
        #文件属性中的日期时会用到  
        self._months_map = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul',  
                            8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}  
    def Run(self):#主函数，用于循环监听用户的登入请求  
        self.s.listen(1)  
        #self.s.settimeout(60)  
        print 'socket created server running...'  
        #设置之后创建的socket都只存活60秒，防止异常时卡死  
        socket.setdefaulttimeout(60)  
        while 1:  
            try:  
                conn,addr=self.s.accept()  
            #停止服务器  
            except KeyboardInterrupt:  
                self.close=True  
                conn.close()  
                self.s.close()  
                print 'KeyboardInterrupt'  
                break  
            print 'connect with '+addr[0]+':'+str(addr[1])  
            #开启新线程用于与该用户交互  
            start_new_thread(self.cftpcmd,(conn,))  
    def cftpcmd(self,cnn,):#与用户交互的主函数  
        cpath=self.path.replace('\\','//')  
        os.chdir(cpath)  
        #连接文件化，以访问文件的方式访问socket  
        cf=cnn.makefile('rw',0)  
        cf.write('220 ready for transfer\r\n')  
        print 'thread open and connected...'  
        #无用户验证机制，在此接受用户  
        print cf.readline().strip()  
        cf.write('331 name ok\r\n')  
        print cf.readline().strip()  
        cf.write('230 log in ok\r\n')  
        #保存用于数据传输的连接  
        dsocket=None  
        #用于处理用户请求关闭连接  
        selfclose=False  
        while 1:  
            #获取用户提交的命令和参数  
            try:  
                gets=cf.readline().strip()  
                if self.close or selfclose:  
                    break  
            except:  
                print '\r\ntimeout exit thread'  
                cnn.close()  
                break  
            print 'receive command:  "%s"'% gets  
            cmd=gets[:3].lower()  
            args=gets[3:]  
            #解析命令，使用对应的函数处理。以eval方式是为了在多个命令需要的处理函数相似的情况下简化  
            try:  
                if cmd in ['lis',]:  
                    ev='self.handle_%s(dsocket,cf)' % (cmd)  
                    print ev  
                    eval(ev)  
                elif cmd=='qui':  
                    selfclose=self.handle_qui(cf)  
                elif cmd=='ret':  
                    cf.write('125 dataconnection open\r\n')  
                    start_new_thread(self.handle_ret,(args,cf,dsocket))  
                elif cmd=='sto':  
                    cf.write('150 file status ok\r\n')  
                    start_new_thread(self.handle_sto,(args,cf,dsocket))  
                elif cmd=='pas':  
                    ev='self.handle_%s("%s",cf)' % (cmd,args)  
                    print ev  
                    dsocket,psocket=eval(ev)  
                elif cmd=='rnf':  
                    cf.write('350 ready for destination name\r\n')  
                    oldename=args[2:]  
                elif cmd=='rnt':  
                    cf.write('250 rename ok\r\n')  
                    newname=args[2:]  
                    try:  
                        os.rename(oldename,newname)  
                    except:  
                        print 'rename error'  
                elif hasattr(self,'handle_%s'% cmd):  
                    ev='self.handle_%s("%s",cf)' % (cmd,args)  
                    print ev  
                    eval(ev)  
                else:  
                    cf.write('501 Invaild command\r\n')  
                    print 'no handler for this command..'+'self.handle_%s("%s",cf)' % (cmd,args)  
            except:  
                print 'error...closing thread and conn'  
                if dsocket != None:  
                    dsocket.close()  
                    psocket.close()  
                cf.write('221 goodbye..\r\n')  
                cf.close()  
                cnn.close()  
                exit_thread()  
        print 'main thread exit'  
        cnn.close()  
    def handle_user(self,args,cf):  
        cf.write('331 username ok\r\n')  
        print '331 ok'  
    def handle_pass(self,args,cf):  
        cf.write('230 log in ok\r\n')  
        print '230 ok'  
    def handle_cwd(self,args,cf):#CWD函数，还包含了当目录不存在时创建目录的功能  
        try:  
            os.chdir(args[1:])  
        except:  
            print 'dir does not exit,make it'  
            os.mkdir(args[1:])  
            os.chdir(args[1:])  
        cf.write('250 "%s" is current directory\r\n'% os.getcwd())  
        print 'cwd'  
    def handle_pwd(self,args,cf):  
        cf.write('257 "%s" is current directory\r\n'% os.getcwd()[len(self.path)-1:].replace('\\','/'))  
        print 'pwd'  
    def handle_lis(self,ppsock,cf):#LIST函数，用于返回用户请求的目录下的文件列表  
        cf.write('125 Data connection already open \r\n')  
        res=''  
        for afile in os.listdir(os.getcwd()):  
            fpath=os.getcwd()+'\\'+afile  
            #文件的修改时间需要进行相应的格式化  
            tstr=self.format_time(fpath)  
            if os.path.isfile(fpath):  
                #获取文件大小  
                size=os.path.getsize(fpath)  
                res+= '-rw-rw-rw-   1 owner    group       %s %s %s\r\n' % (size,tstr,afile)  
            else:  
                res+= 'drwxrwxrwx   1 owner    group           0 %s %s\r\n' % (tstr,afile)  
        print res  
        ppsock.send(res)  
        cf.write('226 transfer complete\r\n')  
        ppsock.close()  
    def handle_pas(self,args,cf):#进入PASV模式，返回一个用于传输数据的socket  
        psock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
        psock.bind((self.lip,0))  
        pport=psock.getsockname()[1]  
        psock.listen(1)  
        cf.write('227 entering pasv mode (%s,%s,%s).\r\n' % (psock.getsockname()[0],pport//256,pport%256))  
        ppsock,addr=psock.accept()  
        print 'enter pasv mode port %s...'%pport  
        return [ppsock,psock]  
    def handle_typ(self,args,cf):  
        cf.write('200 \r\n')  
        print 'type a'  
    def handle_qui(self,cf):  
        cf.write('200 \r\n')  
        print 'quit...'  
        return True  
    def handle_noo(self,args,cf):  
        args=args[2:]  
        cf.write('200 \r\n')  
        print 'noop'  
    def handle_siz(self,args,cf):  
        filename=args[2:]  
        print filename  
        size=os.path.getsize(os.getcwd()+'\\'+filename)  
        cf.write('%s %s\r\n'%(213,size))  
    def handle_por(self,args,cf):#port mode pass  
        args=args[2:]  
        cf.write('200 \r\n')  
        print 'enter port mode'  
    def handle_ret(self,args,cf,psock):#RET命令，用于下载文件  
        try:  
            tpath=os.getcwd()+'\\'+args[2:]  
            print 'ret transfering now...path:%s'%tpath  
            f=open(tpath,'rb')  
            #对文件进行分片传输  
            while True:  
                data=f.read(self.PSIZE)  
                if not data:  
                    break  
                psock.send(data)  
            cf.write('226 ok\r\n')  
            print 'transport completed..'  
            psock.close()  
        except:  
            print 'ret error...'  
            cf.write('226 ok\r\n')  
            psock.close()  
            exit_thread()  
    def handle_sto(self,args,cf,psock):#STO命令，用于上传文件  
        try:  
            fname=os.getcwd()+'\\'+args[2:]  
            f=open(fname,'wb')  
            print 'make file ok'  
            buf=psock.recv(self.PSIZE)  
            while len(buf)==self.PSIZE:  
                f.write(buf)  
                buf=psock.recv(self.PSIZE)  
            cf.write('226 transfer complete\r\n')  
            f.write(buf)  
            f.close()  
            psock.close()  
        except:  
            print 'error in sto'  
            psock.close()  
            exit_thread()  
    def handle_mkd(self,args,cf):  
        cf.write('257 %s dir created\r\n'%args)  
        try:  
            os.mkdir(args[1:])  
        except:  
            print 'mkdir error'  
    def handle_del(self,args,cf):  
        cf.write('250 file removed\r\n')  
        fname=os.getcwd()+'\\'+args[2:]  
        try:  
            os.remove(fname)  
        except:  
            print 'dele error'  
    def handle_rmd(self,args,cf):  
        cf.write('250 dir remove\r\n')  
        try:  
            os.rmdir(args[1:])  
        except:  
            print 'remove dir error'  
    def format_time(self,file):#时间格式化  
        raw_ftime=os.stat(file).st_mtime  
        mtime=time.localtime(raw_ftime)  
        now=time.time()  
  
        if now-raw_ftime>180*24*60*60:  
            tstr='%d  %Y'  
        else:  
            tstr='%d %H:%M'  
        res='%s %s'%(self._months_map[mtime.tm_mon],time.strftime(tstr,mtime))  
        return res  
    def handle_sys(self,args,cf):  
        cf.write('215 UNIX Type:L8\r\n')  
        print 'syst'  
if __name__=='__main__':  
    abc=FTPs('192.168.1.4','/Users/wangshidi/ProjectA/Python/FTP/')  
    abc.Run() 
