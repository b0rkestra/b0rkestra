import OSC
c = OSC.OSCClient()
c.connect(('192.168.1.6', 7110))  
oscmsg = OSC.OSCMessage()
oscmsg.setAddress("/user/1")
oscmsg.append('HELLO')
c.send(oscmsg)