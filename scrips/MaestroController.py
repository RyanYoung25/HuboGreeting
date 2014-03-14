#!/usr/bin/env python

import roslib; roslib.load_manifest('maestro')
import rospy
import time
import threading
import subprocess
from hubomsg.msg import *

class MaestroController:
    def __init__(self):
        print "Init"
        self.newVal = False
        self.value = 0.0
        #self.startMaestro()
        rospy.init_node("Maestro_Commands")
        self.pub = rospy.Publisher('Maestro/Control', MaestroCommand)
        rospy.Subscriber("Maestro/Message", MaestroMessage, self.update)
        rospy.sleep(2)
        self.id_num = 0

    def startMaestro(self):
        subprocess.call([""])

    def setId_num(self, num):
        self.id_num = num

    def update(self, message):
        self.newVal = True
        self.value = message.value
        #print self.value

    def test(self):
        pyMessage = MaestroCommand("RSP", "position", 1.5, "", self.id_num)
        self.pub.publish(pyMessage)
        print "Published a message"
        time.sleep(.01)

    def setJointPosition(self, joint, value):
        pyMessage = MaestroCommand(joint, "position", value, "", self.id_num)
        self.pub.publish(pyMessage)
        time.sleep(.01)

    def setJointVelocity(self, joint, value):
        pyMessage = MaestroCommand(joint, "velocity", value, "", self.id_num)
        self.pub.publish(pyMessage)
        time.sleep(.01)

    def enableAll(self):
        pyMessage = MaestroCommand("", "EnableAll"," 0", "", self.id_num)
        self.pub.publish(pyMessage)
        time.sleep(.01)

    def homeAll(self):
        pyMessage = MaestroCommand("", "HomeAll", "0", "", self.id_num)
        self.pub.publish(pyMessage)
        print "Homeing All Joints"
        time.sleep(10)

    def initRobot(self):
        pyMessage = MaestroCommand("", "initRobot", "0", "", self.id_num)
        self.pub.publish(pyMessage)
        time.sleep(.01)

    def initSensors(self):
        pyMessage = MaestroCommand("", "InitializeSensors", "0", "", self.id_num)
        self.pub.publish(pyMessage)
        time.sleep(.01)

    def publishMessage(self, joint, command, value, target):
        pyMessage = MaestroCommand(joint, command, value, target, self.id_num)
        self.pub.publish(pyMessage)
        time.sleep(.01)

    def executeCommonStartUp(self):
        self.initRobot()
        self.homeAll()
        self.enableAll()
        self.initSensors()

    def home(self, target):
        pyMessage = MaestroCommand("", "Home", "0", target, self.id_num)
        self.pub.publish(pyMessage)
        time.sleep(.01)

    def enable(self, target):
        pyMessage = MaestroCommand("", "Enable", "0", target, self.id_num)
        self.pub.publish(pyMessage)
        time.sleep(.01)

    def waitForJoint(self, joint):
        flag = True
        while bool(flag):
            flag = self.checkJointRequiresMotion(joint)
            time.sleep(.05)
            if(flag == None):
                flag = True

    def checkJointRequiresMotion(self, joint):
        pyMessage = MaestroCommand(joint, "Check", "0", "", self.id_num)
        self.pub.publish(pyMessage)
        time.sleep(.01)
        if self.newVal:
            self.newVal = False
            if self.value == None:
                #print "true"
                return True
            else:
                if self.value == "True":
                    return True
                else:
                    return False
                       

    def get(self, joint, target):
        pyMessage = MaestroCommand(joint, "Get", "0", target, self.id_num)
        self.pub.publish(pyMessage)

        if self.newVal:
            self.newVal = False
            time.sleep(.01)
            return self.value
        else:
             time.sleep(.01)
    def doWhen(self, wait, joint, command, value, target):
        try:
            timer = threading.Timer(wait, self.publishMessage, (joint, command, value, target, self.id_num))
            timer.start()
        except Exception:
            pass
