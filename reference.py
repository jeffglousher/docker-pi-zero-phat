import time
import automationhat
#import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as mqtt

mqttc=mqtt.Client(client_id="garage-pi")

##
def on_message(client, userdata, message):
    if str(message.payload) == "ON":
        automationhat.relay.one.on()
    elif str(message.payload) == "OFF":
        automationhat.relay.one.off()
##
mqttc.on_message=on_message #attach function to callback
mqttc.will_set("estates/garage-pi/automation-phat/relay1/available", "offline",2)
mqttc.connect("blackbox-ubuntu-server16",1883,60)
mqttc.loop_start()

mqttc.subscribe("estates/garage-pi/automation-phat/relay1/command")

try:
    (result,mid)=mqttc.publish("estates/garage-pi/automation-phat/relay1/available","online",2)
    while 1:
        if automationhat.input.one.is_on():
            (result,mid)=mqttc.publish("estates/garage-pi/automation-phat/input1","ON",1)
        elif automationhat.input.one.is_off():
            (result,mid)=mqttc.publish("estates/garage-pi/automation-phat/input1","OFF",1)

        if automationhat.relay.one.is_on():
            (result,mid)=mqttc.publish("estates/garage-pi/automation-phat/relay1","ON",1)
        elif automationhat.relay.one.is_off():
            (result,mid)=mqttc.publish("estates/garage-pi/automation-phat/relay1","OFF",1)


        if automationhat.input.one.is_on():
            (result,mid)=mqttc.publish("estates/garage-pi/automation-phat/output1","ON",1)
        elif automationhat.input.one.is_off():
            (result,mid)=mqttc.publish("estates/garage-pi/automation-phat/output1","OFF",1)

#        print(automationhat.input.one.is_on())

        time.sleep(0.5)

except Exception as e:
    print (e.message, e.args)
    (result,mid)=mqttc.publish("estates/garage-pi/automation-phat/relay1/available","offline",2)
    mqttc.loop_stop()
    mqttc.disconnect()
    print("cleanup done?")