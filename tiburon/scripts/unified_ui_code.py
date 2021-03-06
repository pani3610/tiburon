#!/usr/bin/env python
from unified_ui import Ui_MainWindow
import sys
from PyQt4 import QtGui,QtCore
import rospy
import os
import signal
import thrustercontrol 
from std_msgs.msg import String

class Panel(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        text_str=""
        #self.connect(self.thread, SIGNAL("finished()"), self.updateUi)
        self.button()
    def button(self):
        self.ui.thruster_button.clicked.connect(self.thruster)
        self.ui.joystick_button.clicked.connect(self.joystick)
        self.ui.pid_Button.clicked.connect(self.pid)
        self.ui.camera_Button.clicked.connect(self.camera)
        self.ui.enterButton.clicked.connect(self.textBox)
    def thruster(self):
        os.system('rosrun tiburon thrustercontrol.py &')
    def joystick(self):
	os.system('rosrun tiburon joystick_ui_code.py &')
    def pid(self):
	    os.system('rosrun tiburon pid_ui_code.py &')	
	    os.system('rosrun tiburon server_yaw.py & rosrun tiburon server_depth.py & rosrun tiburon server_pitch.py &')
	    os.system('rosrun rqt_reconfigure rqt_reconfigure &') 
    def camera(self):
        os.system('rosrun tiburon show.py &')
    def textBox(self):
        self.text_str=""
        self.text_str=self.ui.textbox_lineEdit.text() #find on net how to extract data
        print self.text_str
        self.textboxpub=rospy.Publisher("what_is_up",String,queue_size=1)
        self.textboxpub.publish(str(self.text_str))

def main():
    rospy.init_node("unified_ui_code")
    signal.signal(signal.SIGINT,signal.SIG_DFL) #for ctrl+c to cut the ui window
    #SIG_DFL : default action(dump core+exit)
    #SIGINT: keyboard interrupt exception
    app=QtGui.QApplication(sys.argv) 
    ui = Panel() 
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
