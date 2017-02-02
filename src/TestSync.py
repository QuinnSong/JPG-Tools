from time import sleep
from wx.lib.pubsub import pub

def theLoop():
    send("thisis one")
    sleep(3)
    send("this is two")
    sleep(5)
    send("this is three")
def send(msg):
    pub.sendMessage('update', msg = msg)