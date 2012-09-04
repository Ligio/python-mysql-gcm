#!/usr/bin/python

from gcm_push_data import PushData
from gcm_logic import GCMLogic
from gcm_setup import AllSetup
import push_gcm

if __name__ == "__main__":
	push = PushData()
	setup = AllSetup()
	push.setData(data=None, collapse_key='push', delay_while_idle=False, time_to_live=86400)
	push.writeData(setup.push_file)

	logic = GCMLogic(1)
	devices = logic.getDevices()
        logic.sendPushToDevices(devices)
