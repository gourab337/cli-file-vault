import Alarm_integration
import json


token = Alarm_integration.Login("192.168.124.27", 7001, "admin", "s6840334")
Alarm_integration.save_rules(token,"Graymatics","7.7.7.7","showOnAlarmLayoutAction",["8e8bd26a-fa1f-69b3-a8f5-8d5d2929aed9"])
print(Alarm_integration.Alarm_trigger("192.168.124.27",7001,token,"2.2.2.2","Graymatics","crowd"))
