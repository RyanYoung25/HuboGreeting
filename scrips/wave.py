#!/usr/bin/env python

from MaestroController import *
import time

ID_NUM = 987
SLEEP_TIME = .025 # 5 iterations
REPS = 2

def wave():
	maestro = MaestroController()
	maestro.setId_num(ID_NUM)

	# Hand to initial position
	maestro.publishMessage("RSR RSP REP RSY", "position position position position", "", "-1.25 0 -1.3 -1.57", ID_NUM)
	while(maestro.checkJointRequiresMotion("RSR") and maestro.checkJointRequiresMotion("RSP") and maestro.checkJointRequiresMotion("REP") and maestro.checkJointRequiresMotion("RSY")):
		time.sleep(SLEEP_TIME)

	# Wave
	for i in xrange REPS:
		maestro.publishMessage("REP", "position", "", "0", ID_NUM)
		while(maestro.checkJointRequiresMotion("REP")):
			time.sleep(SLEEP_TIME)
		maestro.publishMessage("REP", "position", "", "-1.3", ID_NUM)
		while(maestro.checkJointRequiresMotion("REP")):
			time.sleep(SLEEP_TIME)

	# Return arm to home position
	maestro.publishMessage("RSR RSP REP RSY", "position position position position", "", "0 0 0 0", ID_NUM)
	
	return True