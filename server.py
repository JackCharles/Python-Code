# coding=utf-8
import socket
import threading
import json
import pymysql
import logging

__author__ = 'zj2011@live.com'

MAXBUFFER = 2048
recv_port = 9999
mysql_info = ('127.0.0.1', 3306, 'root', 'root', 'android_im_server')
server_addr = ('', recv_port)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 接收消息
server_socket.bind(server_addr)

log = logging.getLogger('server')
log.setLevel(logging.INFO)
ch = logging.StreamHandler()  # 输出到控制台
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  # 输出格式
ch.setFormatter(formatter)
log.addHandler(ch)  # 设置输出方式


# ======================================================================================#
def getjson(tag, uf, ut, con, sid="0", ex="0"):
    d = {"TAG": tag, "USERFROM": uf, "USERTO": ut, "SESSIONID": sid, "CONTEXT": con, "EXTRA": ex}
    return json.dumps(d)


class sqlopt(object):
    def __init__(self, host, port, user, passwd, db):
        self.__host__ = host
        self.__port__ = port
        self.__user__ = user
        self.__passwd__ = passwd
        self.__database__ = db
        self.__conn__ = None
        self.__cursor__ = None

    def Connect(self):
        try:
            self.__conn__ = pymysql.connect(host=self.__host__,
                                            port=self.__port__,
                                            user=self.__user__,
                                            passwd=self.__passwd__,
                                            db=self.__database__,
                                            charset='utf8')
            self.__cursor__ = self.__conn__.cursor()
            return True
        except:
            log.error('连接数据库失败...')
            return False

    def Update(self, sql):  # insert update delete
        if self.__conn__ and self.__cursor__:
            try:
                self.__cursor__.execute(sql)
                self.__conn__.commit()
                return True
            except:
                self.__conn__.rollback()
                log.error('执行数据库更新操作失败...')
                return False
        else:
            log.error('数据库连接不可用，更新操作失败...')
            return False

    def Query(self, sql):
        if self.__conn__ and self.__cursor__:
            try:
                self.__cursor__.execute(sql)
                return self.__cursor__.fetchall()
            except:
                log.error('查询数据库失败...')
                return None
        else:
            log.error('数据库连接不可用，查询操作失败...')
            return False

    def Close(self):
        if self.__cursor__:
            self.__cursor__.close()
        if self.__conn__:
            self.__conn__.close()


# =======================================================================================#
class ProcessMessage(threading.Thread):
    def __init__(self, data, client_ip, client_port):
        threading.Thread.__init__(self)
        self.__jsdata__ = data
        self.__addr__ = (client_ip, client_port)
        self.fip = client_ip
        self.cport = client_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 发送消息

    def __UserRegister__(self):
        res = self.db.Query("select id from users where id='%s'" % self.fid)
        if res:
            log.error('新用户 ' + self.fid + ' 注册失败，用户名已存在...')
            rd = getjson("REGF", "SERVER", "", "注册失败，用户名已存在")
            self.client_socket.sendto(rd.encode("utf-8"), self.__addr__)
            return False
        else:
            s = self.db.Update("insert into users() values('%s','%s','%s','%s')" % (self.fid, self.con, self.fip, 'DOWN'))
            if s:
                log.info('新用户 ' + self.fid + ' 注册成功...')
                rd = getjson("REGS", "SERVER", "", "注册成功")
                self.client_socket.sendto(rd.encode("utf-8"), self.__addr__)
                return True
            else:
                log.error('新用户 ' + self.fid + ' 注册失败，发生未知错误...')
                rd = getjson("REGF", "SERVER", "", "注册失败，未知错误")
                self.client_socket.sendto(rd.encode("utf-8"), self.__addr__)
                return False

    def __UserLogin__(self):  # 登录一次，返回两次+一次群发
        res = self.db.Query("select id,password from users where id='%s'" % self.fid)
        if res and res[0][1] == self.con:
            # Alice的IP和状态
            self.db.Update("update users set ip='%s', stat='UP' where id='%s'" % (self.fip, self.fid))
            log.info('用户 ' + self.fid + ' 登录成功...')

            # 返回Alice的好友列表[(id,ip,stat),...]
            fds = self.db.Query(
                "select users.id ,users.ip ,users.stat from friends,users where users.id=friends.friend and friends.id = '%s'" % self.fid)
            rd = getjson("LGIS", "SERVER", self.fid, fds)
            log.debug("返回Alice的好友列表...")
            self.client_socket.sendto(rd.encode("utf-8"), self.__addr__)
            log.debug("返回Alice的好友列表成功...")

            # 给Alice推送离线消息{[id:id1,msg:[msg1,msg2...]], [id:id2,[msg1,msg2...]]...}
            ofmsg = self.db.Query("select friend,offlinemsg from friends where id='%s' and offlinemsg!=''" % self.fid)
            msglist = []
            for msg in ofmsg:
                # 这里subdict={}不能放在外面，xxx={}表示声明一个dict对象,list只能添加不同对象(添加相同对象值会一样)
                # subdict放在外面表示只申请了一个对象，重复添加到list最终会使得list中的所有dict值一样，因为他们是一个对象
                subdict = {}
                subdict['id'] = msg[0]
                subdict['msg'] = json.loads(msg[1])
                msglist.append(subdict)
            rd = getjson("OFLMSG", "SERVER", self.fid, msglist)
            log.debug("推送离线消息...")
            self.client_socket.sendto(rd.encode('utf-8'), self.__addr__)
            log.debug("推送离线消息成功...")
            self.db.Update("update friends set offlinemsg='' where id='%s'" % self.fid)  # 清空已推送消息

            # 通知好友Alice上线[id, ip]
            olfds = self.db.Query(
                "select users.id, users.ip from users, friends where users.id = friends.friend and friends.id = '%s' and users.stat = 'UP'" % self.fid)
            for user in olfds:
                rd = getjson("FRDLGI", "SERVER", user[0], (self.fid, self.fip))  # [0]is id
                self.client_socket.sendto(rd.encode('utf-8'), (user[1], self.cport))  # [1] is ip
            return True
        else:
            log.error('用户 ' + self.fid + ' 登录失败，用户名或密码错误...')
            rd = getjson("LGIF", "SERVER", "", "登录失败，用户名或密码错误")
            self.client_socket.sendto(rd.encode("utf-8"), self.__addr__)
            return False

    def __UserLogout__(self):
        res = self.db.Update("update users set stat='DOWN' where id='%s'" % self.fid)
        if res:
            log.info('用户 ' + self.fid + ' 注销成功...')
            rd = getjson("LGOS", "SERVER", self.fid, "注销成功")
            self.client_socket.sendto(rd.encode("utf-8"), self.__addr__)

            # 通知好友,Alice下线[id]
            olfds = self.db.Query(
                "select users.id, users.ip from users, friends where users.id = friends.friend and friends.id = '%s' and users.stat = 'UP'" % self.fid)
            for user in olfds:
                rd = getjson("FRDLGO", "SERVER", user[0], self.fid)  # [0]is id
                self.client_socket.sendto(rd.encode('utf-8'), (user[1], self.cport))  # [1] is ip
            return True
        else:
            log.error('用户 ' + self.fid + ' 注销失败，发生未知错误...')
            rd = getjson("LGOF", "SERVER", self.fid, "注销失败，未知错误")
            self.client_socket.sendto(rd.encode("utf-8"), self.__addr__)
            return False

    def __ReceiveMessage__(self):
        cmsg = self.db.Query("select offlinemsg from friends where id='%s' and friend='%s'" % (self.tid, self.fid))
        if cmsg[0][0] != '':
            cmsg = json.loads(cmsg[0][0])
            cmsg.append(self.con)
            cmsg = json.dumps(cmsg, ensure_ascii=False)
        else:
            cmsg = json.dumps([self.con], ensure_ascii=False)
        res = self.db.Update(
            "update friends set offlinemsg='%s' where id='%s' and friend='%s'" % (cmsg, self.tid, self.fid))
        if res:
            log.info('来自 ' + self.fid + ' 的离线消息保存成功...')
            rd = getjson("MSGS", "SERVER", self.fid, "发送成功")
            self.client_socket.sendto(rd.encode("utf-8"), self.__addr__)
            return True
        else:
            log.error('来自 ' + self.fid + ' 的离线消息保存失败...')
            rd = getjson("MSGF", "SERVER", self.fid, "发送失败")
            self.client_socket.sendto(rd.encode("utf-8"), self.__addr__)
            return False

    def __AddFriend__(self):
        fd = self.db.Query("select id,ip,stat from users where id='%s'" % self.con)
        res = self.db.Query("select id from friends where id='%s' and friend='%s'" % (self.fid, self.con))
        if fd and (not res):
            self.db.Update("insert into friends() values('%s','%s','')" % (self.fid, self.con))
            self.db.Update("insert into friends() values('%s','%s','')" % (self.con, self.fid))
            log.info('用户 ' + self.fid + ' 添加好友成功...')
            rd = getjson("ADDS", "SERVER", self.fid, fd[0])
            self.client_socket.sendto(rd.encode("utf-8"), self.__addr__)

            # 通知目标好友
            rd = getjson("NFRD", "SERVER", self.con, (self.fid, self.fip, "UP"))
            self.client_socket.sendto(rd.encode("utf-8"), (fd[0][1], self.cport))
            return True
        else:
            log.error('用户 ' + self.fid + ' 添加好友失败，目标id不存在或重复添加...')
            rd = getjson("ADDF", "SERVER", self.fid, "ID不存在或重复添加")
            self.client_socket.sendto(rd.encode("utf-8"), self.__addr__)
            return False

    def __DeleteFriend__(self):
        res1 = self.db.Update("delete from friends where id='%s' and friend='%s'" % (self.fid, self.con))
        res2 = self.db.Update("delete from friends where id='%s' and friend='%s'" % (self.con, self.fid))
        if res1 and res2:
            log.info('用户 ' + self.fid + ' 删除好友成功...')
            rd = getjson("DELS", "SERVER", self.fid, "删除好友成功")
            self.client_socket.sendto(rd.encode("utf-8"), self.__addr__)

            # 通知目标好友
            bdf = self.db.Query("select ip from users where id='%s'" % self.con)
            rd = getjson("BEDEL", "SERVER", self.con, self.fid)
            self.client_socket.sendto(rd.encode("utf-8"), (bdf[0][0], self.cport))
            return True
        else:
            log.error('用户 ' + self.fid + ' 删除好友失败，发生未知错误...')
            rd = getjson("DELF", "SERVER", self.fid, "删除好友失败")
            self.client_socket.sendto(rd.encode("utf-8"), self.__addr__)
            return False

    def run(self):
        try:
            __data__ = json.loads(self.__jsdata__.decode('utf-8'))
            self.tag = __data__['TAG']
            self.fid = __data__['USERFROM']
            self.tid = __data__['USERTO']
            self.sid = __data__['SESSIONID']
            self.con = __data__['CONTEXT']
        except:
            log.error('无法解析来自 ' + self.fip + ' 的JSON数据...')
            rd = getjson("KEYE", "SERVER", "", "JSON数据格式或主键错误")
            self.client_socket.sendto(rd.encode('utf-8'), self.__addr__)
            return None

        try:
            self.db = sqlopt(*mysql_info)
            self.db.Connect()
        except:
            return None

        if self.tag == 'REG':
            self.__UserRegister__()
        elif self.tag == 'LGI':
            self.__UserLogin__()
        elif self.tag == 'LGO':
            self.__UserLogout__()
        elif self.tag == 'MSG':
            self.__ReceiveMessage__()
        elif self.tag == 'ADDFRD':
            self.__AddFriend__()
        elif self.tag == 'DELFRD':
            self.__DeleteFriend__()
        else:
            log.error('无法识别来自 ' + self.fip + ' 的数据类型...')
            rd = getjson("VALE", "SERVER", "", "JSON数据值错误")
            self.client_socket.sendto(rd.encode('utf-8'), self.__addr__)
        self.client_socket.close()
        self.db.Close()


# =======================================================================================#
def main():
    log.info('Life is short, you need Python.')
    log.info('服务端已启动...')
    log.info('正在监听UDP端口:%s...' % recv_port)
    while True:
        data, addr = server_socket.recvfrom(MAXBUFFER)
        # if addr[0]=='127.0.0.1' or addr[0]=='49.140.86.246':
        # log.error("非法IP: "+addr[0])
        if not data:
            log.error('来自客户端 ' + addr[0] + ' 的数据无效或损坏...')
            rd = getjson("DATAE", "SERVER", "", "数据无效或损坏")
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client_socket.sendto(rd.encode('utf-8'), (addr[0], 8888))
            client_socket.close()
        else:
            ProcessMessage(data, addr[0], 8888).start()

    server_socket.close()


if __name__ == '__main__':
    main()
