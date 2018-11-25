import time, json
from envirophat import light, motion, weather, leds, analog
import automationhat
import paho.mqtt.client as mqtt

cid = "undefined-pi"
mqtt_server = "dockerhost"
sbc_type = "unknown"
hass_autogen_topic = "homeassistant_autogen"

# Test for computer & board types
try:
    temp=weather.temperature()
    print("weather.temperature() read successfully, envirophat is attached :-)")
    sbc_type = "envirophat"
    cid = "plant-pi"
except:
       print("weather.temperature() read FAIL, envirophat is not attached or cannot be communicated with")

try:
    input1=automationhat.input.one.is_on()
    print("automationhat.input.one.is_on() read successfully, automationphat is attached :-)")
    sbc_type = "automationphat"
    cid = "plant-pi"
except:
    print("automationhat.input.one.is_on() read FAIL, automationphat is not attached or cannot be communicated with")

# configure and connect to MQTT server
mqttc=mqtt.Client(client_id=cid)
mqttc.connect(mqtt_server,1883,60)
mqttc.loop_start()

# Function definitions
def sbc_rpi0_envirophat_setup():
    # configure MQTT config topics so that discovery can be used with Hass
    cfg_phatlightrgb = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "LightRGB", "qos" : 1, "unit_of_measurement" : "RGB", "value_template": "{{ value_json.phatlightrgb}}"}
    cfg_phatlight = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "Light", "qos" : 1, "unit_of_measurement" : "Lux", "device_class" : "illuminance", "value_template": "{{ value_json.phatlight}}"}
    cfg_phattemperature = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "Temperature", "qos" : 1, "unit_of_measurement" : "°C", "device_class" : "temperature", "value_template": "{{ value_json.phattemperature}}"}
    cfg_phatpressure = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "Pressure", "qos" : 1, "unit_of_measurement" : "hPa", "device_class" : "pressure", "value_template": "{{ value_json.phatpressure}}"}
    cfg_phataltitude = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "Altitude", "qos" : 1, "unit_of_measurement" : "m", "value_template": "{{ value_json.phataltitude}}"}
    cfg_phatanalog = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "Analog", "qos" : 1, "unit_of_measurement" : "V",  "value_template": "{{ value_json.phatanalog}}"}
    cfg_phatmagnetometer = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "Magnetometer", "qos" : 1, "unit_of_measurement" : "m", "value_template": "{{ value_json.phatmagnetometer}}"}
    cfg_phataccelerometer = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "Accelerometer", "qos" : 1, "unit_of_measurement" : "G", "value_template": "{{ value_json.phataccelerometer}}"}
    cfg_phatheading = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "Heading", "qos" : 1, "unit_of_measurement" : "°", "value_template": "{{ value_json.phatheading}}"}
    
    # Since I really wanted the converted values of the analog read I publish them after conversion directly 
    ## ORIGINAL, to remove
    cfg_soiltemp = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/soiltemp/state", "name": "Temperature", "qos" : 1, "unit_of_measurement" : "°C", "device_class" : "temperature"}
    cfg_soilmoist = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/soilmoist/state", "name": "Moisture", "qos" : 1, "unit_of_measurement" : "%", "device_class" : "humidity"}
    cfg_relhum = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/relhum/state", "name": "Humidity", "qos" : 1, "unit_of_measurement" : "%", "device_class" : "humidity"}
    ## Discovery Config, to validate and to replace
    #cfg_soiltemp = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "Temperature", "qos" : 1, "unit_of_measurement" : "°C", "device_class" : "temperature", "value_template": "{{ value_json.soiltemp}}"}
    #cfg_soilmoist = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "Moisture", "qos" : 1, "unit_of_measurement" : "%", "device_class" : "humidity", "value_template": "{{ value_json.soilmoist}}"}
    #cfg_relhum = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "Humidity", "qos" : 1, "unit_of_measurement" : "%", "device_class" : "humidity", "value_template": "{{ value_json.relhum}}"}

    (result,mid)=mqttc.publish(hass_autogen_topic + "/sensor/" + cid + "/phatlightrgb/config", json.dumps(cfg_phatlightrgb), qos=1, retain=True)
    (result,mid)=mqttc.publish(hass_autogen_topic + "/sensor/" + cid + "/phatlight/config", json.dumps(cfg_phatlight), qos=1, retain=True)
    (result,mid)=mqttc.publish(hass_autogen_topic + "/sensor/" + cid + "/phattemperature/config", json.dumps(cfg_phattemperature), qos=1, retain=True)
    (result,mid)=mqttc.publish(hass_autogen_topic + "/sensor/" + cid + "/phatpressure/config", json.dumps(cfg_phatpressure), qos=1, retain=True)
    (result,mid)=mqttc.publish(hass_autogen_topic + "/sensor/" + cid + "/phataltitude/config", json.dumps(cfg_phataltitude), qos=1, retain=True)
    (result,mid)=mqttc.publish(hass_autogen_topic + "/sensor/" + cid + "/phatanalog/config", json.dumps(cfg_phatanalog), qos=1, retain=True)
    (result,mid)=mqttc.publish(hass_autogen_topic + "/sensor/" + cid + "/phatmagnetometer/config", json.dumps(cfg_phatmagnetometer), qos=1, retain=True)
    (result,mid)=mqttc.publish(hass_autogen_topic + "/sensor/" + cid + "/phataccelerometer/config", json.dumps(cfg_phataccelerometer), qos=1, retain=True)
    (result,mid)=mqttc.publish(hass_autogen_topic + "/sensor/" + cid + "/phatheading/config", json.dumps(cfg_phatheading), qos=1, retain=True)

    (result,mid)=mqttc.publish(hass_autogen_topic + "/sensor/" + cid + "/soiltemp/config", json.dumps(cfg_soiltemp), qos=1, retain=True)
    (result,mid)=mqttc.publish(hass_autogen_topic + "/sensor/" + cid + "/soilmoist/config", json.dumps(cfg_soilmoist), qos=1, retain=True)
    (result,mid)=mqttc.publish(hass_autogen_topic + "/sensor/" + cid + "/relhum/config", json.dumps(cfg_relhum), qos=1, retain=True)
    
def sbc_rpi0_envirophat():
    update={}
    update["phatlightrgb"] = None
    update["phatlight"] = None
    update["phattemperature"] = None
    update["phatpressure"] = None
    update["phataltitude"] = None
    update["phatanalog"] = None
    update["phatmagnetometer"] = None
    update["phataccelerometer"] = None
    update["phatheading"] = None
    update["soiltemp"] = None
    update["soilmoist"] = None
    update["relhum"] = None

    readings = analog.read_all()

    update["phatlightrgb"] = light.rgb()
    update["phatlight"] = light.light()
    update["phattemperature"] = weather.temperature()
    update["phatpressure"] = weather.pressure()
    update["phataltitude"] = weather.altitude()
    update["phatanalog"] = readings
    update["phatmagnetometer"] = motion.magnetometer()
    update["phataccelerometer"] = motion.accelerometer()
    update["phatheading"] = motion.heading()
    update["soiltemp"] = therm200_convert_analog(readings[2])
    update["soilmoist"] = vh400_convert_analog(readings[1])
    update["relhum"] = vghumid_convert_analog(readings[0])

    (result,mid)=mqttc.publish(hass_autogen_topic + "/sensor/" + cid + "/state", json.dumps(update), qos=1, retain=True)   

    soiltemp = therm200_convert_analog(readings[2])
    relhum = vghumid_convert_analog(readings[0])
    soilmoist = vh400_convert_analog(readings[1])
    (result,mid)=mqttc.publish(hass_autogen_topic + "/sensor/" + cid + "/soiltemp/state",round(soiltemp,1), qos=1, retain=False)
    (result,mid)=mqttc.publish(hass_autogen_topic + "/sensor/" + cid + "/soilmoist/state",round(soilmoist,1), qos=1, retain=False)
    (result,mid)=mqttc.publish(hass_autogen_topic + "/sensor/" + cid + "/relhum/state",round(relhum,1), qos=1, retain=False)
    
    print(str(soiltemp) + " °C, Soil Temp")

def sbc_rpi0_automationphat_setup():
    print("foo im setup!")
    #(result,mid)=mqttc.publish("homeassistant_autogen/sensor/plant-pi/soiltemp/config", json.dumps(cfg_soiltemp), qos=1, retain=True)
    #(result,mid)=mqttc.publish("homeassistant_autogen/sensor/plant-pi/soilmoist/config", json.dumps(cfg_soilmoist), qos=1, retain=True)
    #(result,mid)=mqttc.publish("homeassistant_autogen/sensor/plant-pi/relhum/config", json.dumps(cfg_relhum), qos=1, retain=True)

def sbc_rpi0_automationphat():
    print("no measurements yet...")

def therm200_convert_analog(analog): #conversion from vegetronix.com for the THERM200
    return (analog * 41.67) - 40

def vghumid_convert_analog(analog): #conversion from vegetronix.com for the VG-HUMID
    return analog * 33.33

def vh400_convert_analog(analog): #conversion from vegetronix.com for the VH400
    if analog < 1.1:
        return (10 * analog) - 1
    elif analog < 1.3:
        return (25 * analog) - 17.5
    elif analog < 1.82:
        return (48.08 * analog) - 47.5
    elif analog < 2.2:
        return (26.32 * analog) - 7.89
    else:
        return (62.5 * analog) - 87.5

# actual code entry point and loop
try:
    mqttc.will_set("status/" + cid, "offline", qos=1, retain=True)
    (result,mid)=mqttc.publish("status/" + cid, "online", qos=1, retain=True)

    if sbc_type == "envirophat":
        sbc_rpi0_envirophat_setup()
    if sbc_type == "automationphat":
        sbc_rpi0_automationphat_setup()

    while True:
        if sbc_type == "envirophat":
            sbc_rpi0_envirophat()
        if sbc_type == "automationphat":
            sbc_rpi0_automationphat()
        time.sleep(0.5)
except Exception as e:
    print("Exception while running: " + repr(e))
finally:
    (result,mid)=mqttc.publish("status/" + cid, "offline", qos=1, retain=True)
    mqttc.loop_stop()
    mqttc.disconnect()
    print("Program shutting down, MQTT client cleaned up and disconnected")