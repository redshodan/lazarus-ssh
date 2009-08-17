import os, pwd, socket, sys, commands, re, random, types, struct
import tty, termios, signal, select, fcntl, errno, time, threading
from lssh import sendfd

timeout = 5
muxpath = "/home/baron/.ssh/master-baron@myth:22"

#class SSHMuxClient(threading.Thread):
class SSHMuxClient(object):
    SSHMUX_VER = 2
    SSHMUX_COMMAND_OPEN = 1
    SSHMUX_COMMAND_ALIVE_CHECK = 2
    SSHMUX_COMMAND_TERMINATE = 3
    SSHMUX_FLAG_TTY = 1
    SSHMUX_FLAG_SUBSYS = 1<<1
    SSHMUX_FLAG_X11_FWD = 1<<2
    SSHMUX_FLAG_AGENT_FWD = 1<<3
    PING_CMD = "/bin/true"

    def putU32(self, val):
        buff = struct.pack("B", (val >> 24) & 0xff)
        buff = buff + struct.pack("B", (val >> 16) & 0xff)
        buff = buff + struct.pack("B", (val >> 8) & 0xff)
        buff = buff + struct.pack("B", val & 0xff)
        return buff

    def getU32(self, buff):
        bytes = [0,0,0,0]
        bytes[3] = struct.unpack("B", buff[0:1])[0]
        bytes[2] = struct.unpack("B", buff[1:2])[0]
        bytes[1] = struct.unpack("B", buff[2:3])[0]
        bytes[0] = struct.unpack("B", buff[3:4])[0]
        return struct.unpack("I", struct.pack("BBBB", bytes[0], bytes[1],
                                              bytes[2], bytes[3]))[0]

    def ping(self):
        sock = None
        try:
            try:
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                sock.connect(muxpath)
            except Exception, e:
                print "Failed to connect to master:", e
                return False

            # send: length, ver, cmd, flags
            buff = self.putU32(9)
            buff = buff + struct.pack("B", self.SSHMUX_VER)
            buff = buff + self.putU32(self.SSHMUX_COMMAND_OPEN)
            buff = buff + self.putU32(0)
            sock.send(buff)
            # recv: length, ver, allowed, pid
            buff = sock.recv(1024)
            length = self.getU32(buff[:4])
            (ver,) = struct.unpack("B", buff[4:5])
            allowed = self.getU32(buff[5:9])
            flags = self.getU32(buff[9:])
            if ver != self.SSHMUX_VER:
                print "Bad version ssh mux:",ver
                return False
            if allowed != 1:
                print "Connection to master refused"
                return False
            # send: len, ver, len, term, esc char, len, cmd, environ=0
            buff = struct.pack("B", self.SSHMUX_VER)
            buff = buff + self.putU32(5)
            buff = buff + "vt100"
            buff = buff + self.putU32(0xffffffff)
            buff = buff + self.putU32(len(self.PING_CMD))
            buff = buff + self.PING_CMD
            buff = buff + self.putU32(0)
            buff = self.putU32(len(buff)) + buff
            sock.send(buff)
            # Send the fds
            sendfd.sendfd(sock.fileno(), 0)
            sendfd.sendfd(sock.fileno(), 1)
            sendfd.sendfd(sock.fileno(), 2)
            # recv: ver
            buff = []
            while len(buff) < 8:
                ret = sock.recv(1)
                if len(ret):
                    buff.append(ret)
                else:
                    break
            print "len", len(buff)
            for b in buff:
                print len(b),
                if len(b):
                    print ord(b)
                else:
                    print
            ret = self.getU32("".join(buff[:4]))
            ret2 = self.getU32("".join(buff[4:]))
            print "ret:", ret, ret2
            return ret
        finally:
            if sock:
                sock.close()

    def run(self):
        #time.sleep(timeout)
        print "pinging..."
        if not self.ping():
            pass

cli = SSHMuxClient()
cli.run()
