import time, json
from envirophat import light, motion, weather, leds, analog
import automationhat
import paho.mqtt.client as mqtt
import logging
import sys
import signal
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

cid = "undefined-pi"
mqtt_server = "dockerhost"
sbc_type = "unknown"
hass_autogen_topic = "homeassistant_autogen"

# Test for computer & board types
try:
    temp=weather.temperature()
    logging.info("weather.temperature() read successfully, envirophat is attached :-)")
    sbc_type = "envirophat"
    cid = "plant-pi"
except:
       logging.warning("weather.temperature() read FAIL, envirophat is not attached or cannot be communicated with")

try:
    input1=automationhat.input.one.is_on()
    logging.info("automationhat.input.one.is_on() read successfully, automationphat is attached :-)")
    sbc_type = "automationphat"
    cid = "garage-pi"
except:
    logging.warning("automationhat.input.one.is_on() read FAIL, automationphat is not attached or cannot be communicated with")

# configure and connect to MQTT server
mqttc=mqtt.Client(client_id=cid)
mqttc.connect(mqtt_server,1883,60)
mqttc.loop_start()

def mqtt_bool(original_payload):
    if original_payload.decode('UTF-8') == 'ON':
        return True
    elif original_payload.decode('UTF-8') == 'OFF':
        return False
    else: return None

def on_message(client, userdata, message):
    logging.info(message.topic + " : " + message.payload.decode('UTF-8'))
    if message.topic == hass_autogen_topic + "/switch/" + cid + "/leds/command":
        if mqtt_bool(message.payload):
            leds.on()
        elif not mqtt_bool(message.payload):
            leds.off()
        else: logging.warning("Message recieved but no match " + mqtt_bool(message.payload))
    elif message.topic == hass_autogen_topic + "/switch/" + cid + "/phatrelay/command":
        if mqtt_bool(message.payload):
            automationhat.relay.one.on()
        elif not mqtt_bool(message.payload):
            automationhat.relay.one.off()
    elif message.topic == hass_autogen_topic + "/switch/" + cid + "/phatoutput0/command":
        if mqtt_bool(message.payload):
            automationhat.output.one.on()
        elif not mqtt_bool(message.payload):
            automationhat.output.one.off()
    elif message.topic == hass_autogen_topic + "/switch/" + cid + "/phatoutput1/command":
        if mqtt_bool(message.payload):
            automationhat.output.two.on()
        elif not mqtt_bool(message.payload):
            automationhat.output.two.off()
    elif message.topic == hass_autogen_topic + "/switch/" + cid + "/phatoutput2/command":
        if mqtt_bool(message.payload):
            automationhat.output.three.on()
        elif not mqtt_bool(message.payload):
            automationhat.output.three.off()
    else: logging.warning("Message recieved but no match")

mqttc.on_message=on_message #attach function to callback

def bool_state_format(original_state):
    if bool(original_state):
        return 'ON'
    elif not bool(original_state):
        return 'OFF'
    else: return 'NOT_BOOLEAN'

def add_standard_config_options(original_config):
    updated_config = original_config
    updated_config["qos"] = 1
    updated_config["availability_topic"] = "status/" + cid
    return updated_config

# Function definitions
def sbc_rpi0_envirophat_setup():
    # configure MQTT config topics so that discovery can be used with Hass
    cfg_phatlightrgb = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "LightRGB", "unit_of_measurement" : "RGB", "value_template": "{{ value_json.phatlightrgb}}"}
    cfg_phatlightrgb = add_standard_config_options(cfg_phatlightrgb)
    cfg_phatlight = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "Light", "unit_of_measurement" : "Lux", "device_class" : "illuminance", "value_template": "{{ value_json.phatlight}}"}
    cfg_phatlight = add_standard_config_options(cfg_phatlight)
    cfg_phattemperature = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "Temperature", "unit_of_measurement" : "°C", "device_class" : "temperature", "value_template": "{{ value_json.phattemperature}}"}
    cfg_phattemperature = add_standard_config_options(cfg_phattemperature)
    cfg_phatpressure = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "Pressure", "unit_of_measurement" : "hPa", "device_class" : "pressure", "value_template": "{{ value_json.phatpressure}}"}
    cfg_phatpressure = add_standard_config_options(cfg_phatpressure)
    cfg_phataltitude = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "Altitude", "unit_of_measurement" : "m", "value_template": "{{ value_json.phataltitude}}"}
    cfg_phataltitude = add_standard_config_options(cfg_phataltitude)
    cfg_phatanalog = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "Analog", "unit_of_measurement" : "V",  "value_template": "{{ value_json.phatanalog}}"}
    cfg_phatanalog = add_standard_config_options(cfg_phatanalog)
    cfg_phatmagnetometer = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "Magnetometer", "unit_of_measurement" : "m", "value_template": "{{ value_json.phatmagnetometer}}"}
    cfg_phatmagnetometer = add_standard_config_options(cfg_phatmagnetometer)
    cfg_phataccelerometer = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "Accelerometer", "unit_of_measurement" : "G", "value_template": "{{ value_json.phataccelerometer}}"}
    cfg_phataccelerometer = add_standard_config_options(cfg_phataccelerometer)
    cfg_phatheading = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "Heading", "unit_of_measurement" : "°", "value_template": "{{ value_json.phatheading}}"}
    cfg_phatheading = add_standard_config_options(cfg_phatheading)

    # Since I really wanted the converted values of the analog read I publish them after conversion directly 
    cfg_soiltemp = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "SoilTemperature", "unit_of_measurement" : "°C", "device_class" : "temperature", "value_template": "{{ value_json.soiltemp}}"}
    cfg_soiltemp = add_standard_config_options(cfg_soiltemp)
    cfg_soilmoist = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "SoilMoisture", "unit_of_measurement" : "%", "device_class" : "humidity", "value_template": "{{ value_json.soilmoist}}"}
    cfg_soilmoist = add_standard_config_options(cfg_soilmoist)
    cfg_relhum = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "Humidity", "unit_of_measurement" : "%", "device_class" : "humidity", "value_template": "{{ value_json.relhum}}"}
    cfg_relhum = add_standard_config_options(cfg_relhum)
    cfg_leds = {"command_topic": hass_autogen_topic + "/switch/" + cid + "/leds/command", "name": "Leds", "optimistic" : "true"}
    cfg_leds = add_standard_config_options(cfg_leds)

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

    (result,mid)=mqttc.publish(hass_autogen_topic + "/switch/" + cid + "/leds/config", json.dumps(cfg_leds), qos=1, retain=True)
    leds.off()
    mqttc.subscribe(hass_autogen_topic + "/switch/" + cid + "/leds/command")
    
def sbc_rpi0_envirophat():
    update={}

    update["phatlightrgb"] = light.rgb()
    update["phatlight"] = light.light()
    update["phattemperature"] = round(weather.temperature(), 1)
    update["phatpressure"] = round(weather.pressure(unit='hPa'), 1)
    update["phataltitude"] = round(weather.altitude(qnh=1020), 1)
    update["phatanalog"] = analog.read_all()
    update["phatmagnetometer"] = str(motion.magnetometer())
    update["phataccelerometer"] = str(motion.accelerometer())
    update["phatheading"] = round(motion.heading(), 1)
    update["soiltemp"] = round(therm200_convert_analog(update["phatanalog"][2]), 1)
    update["soilmoist"] = round(vh400_convert_analog(update["phatanalog"][1]), 1)
    update["relhum"] = round(vghumid_convert_analog(update["phatanalog"][0]), 1)

    (result,mid)=mqttc.publish(hass_autogen_topic + "/sensor/" + cid + "/state", json.dumps(update), qos=1, retain=True)   

    return update

def sbc_rpi0_automationphat_setup():
    cfg_phatanalog0 = {"state_topic": hass_autogen_topic + cid + "/state", "name": "Analog0", "unit_of_measurement" : "V", "value_template": "{{ value_json.phatanalog0 }}"}
    cfg_phatanalog0 = add_standard_config_options(cfg_phatanalog0)
    cfg_phatanalog1 = {"state_topic": hass_autogen_topic + cid + "/state", "name": "Analog1", "unit_of_measurement" : "V", "value_template": "{{ value_json.phatanalog1 }}"}
    cfg_phatanalog1 = add_standard_config_options(cfg_phatanalog1)
    cfg_phatanalog2 = {"state_topic": hass_autogen_topic + "/sensor/" + cid + "/state", "name": "Analog2", "unit_of_measurement" : "V", "value_template": "{{ value_json.phatanalog2 }}"}
    cfg_phatanalog2 = add_standard_config_options(cfg_phatanalog2)

    cfg_phatinput0 = {"state_topic": hass_autogen_topic + cid + "/state", "name": "Input0", "value_template": "{{ value_json.phatinput0 }}"}
    cfg_phatinput0 = add_standard_config_options(cfg_phatinput0)
    cfg_phatinput1 = {"state_topic": hass_autogen_topic + cid + "/state", "name": "Input1", "value_template": "{{ value_json.phatinput1 }}"}
    cfg_phatinput1 = add_standard_config_options(cfg_phatinput1)
    cfg_phatinput2 = {"state_topic": hass_autogen_topic + cid + "/state", "name": "Input2", "value_template": "{{ value_json.phatinput2 }}"}
    cfg_phatinput2 = add_standard_config_options(cfg_phatinput2)

    cfg_phatrelay = {"command_topic": hass_autogen_topic + "/switch/" + cid + "/phatrelay/command", "state_topic": hass_autogen_topic + cid + "/state", "name": "Relay", "value_template": "{{ value_json.phatrelay }}"}
    cfg_phatrelay = add_standard_config_options(cfg_phatrelay)
    cfg_phatoutput0 = {"command_topic": hass_autogen_topic + "/switch/" + cid + "/phatoutput0/command", "state_topic": hass_autogen_topic + cid + "/state", "name": "Output0", "value_template": "{{ value_json.phatoutput0 }}"}
    cfg_phatoutput0 = add_standard_config_options(cfg_phatoutput0)
    cfg_phatoutput1 = {"command_topic": hass_autogen_topic + "/switch/" + cid + "/phatoutput1/command", "state_topic": hass_autogen_topic + cid + "/state", "name": "Output1", "value_template": "{{ value_json.phatoutput1 }}"}
    cfg_phatoutput1 = add_standard_config_options(cfg_phatoutput1)
    cfg_phatoutput2 = {"command_topic": hass_autogen_topic + "/switch/" + cid + "/phatoutput2/command", "state_topic": hass_autogen_topic + cid + "/state", "name": "Output2", "value_template": "{{ value_json.phatoutput2 }}"}
    cfg_phatoutput2 = add_standard_config_options(cfg_phatoutput2)

    (result,mid)=mqttc.publish(hass_autogen_topic + "/sensor/" + cid + "/phatanalog0/config", json.dumps(cfg_phatanalog0), qos=1, retain=True)
    (result,mid)=mqttc.publish(hass_autogen_topic + "/sensor/" + cid + "/phatanalog1/config", json.dumps(cfg_phatanalog1), qos=1, retain=True)
    (result,mid)=mqttc.publish(hass_autogen_topic + "/sensor/" + cid + "/phatanalog2/config", json.dumps(cfg_phatanalog2), qos=1, retain=True)

    (result,mid)=mqttc.publish(hass_autogen_topic + "/binary_sensor/" + cid + "/phatinput0/config", json.dumps(cfg_phatinput0), qos=1, retain=True)
    (result,mid)=mqttc.publish(hass_autogen_topic + "/binary_sensor/" + cid + "/phatinput1/config", json.dumps(cfg_phatinput1), qos=1, retain=True)
    (result,mid)=mqttc.publish(hass_autogen_topic + "/binary_sensor/" + cid + "/phatinput2/config", json.dumps(cfg_phatinput2), qos=1, retain=True)

    (result,mid)=mqttc.publish(hass_autogen_topic + "/switch/" + cid + "/phatrelay/config", json.dumps(cfg_phatrelay), qos=1, retain=True)
    (result,mid)=mqttc.publish(hass_autogen_topic + "/switch/" + cid + "/phatoutput0/config", json.dumps(cfg_phatoutput0), qos=1, retain=True)
    (result,mid)=mqttc.publish(hass_autogen_topic + "/switch/" + cid + "/phatoutput1/config", json.dumps(cfg_phatoutput1), qos=1, retain=True)
    (result,mid)=mqttc.publish(hass_autogen_topic + "/switch/" + cid + "/phatoutput2/config", json.dumps(cfg_phatoutput2), qos=1, retain=True)

    mqttc.subscribe(hass_autogen_topic + "/switch/" + cid + "/phatrelay/command")
    mqttc.subscribe(hass_autogen_topic + "/switch/" + cid + "/phatoutput0/command")
    mqttc.subscribe(hass_autogen_topic + "/switch/" + cid + "/phatoutput1/command")
    mqttc.subscribe(hass_autogen_topic + "/switch/" + cid + "/phatoutput2/command")

def sbc_rpi0_automationphat():
    update={}
    update["phatanalog0"] = automationhat.analog.one.read()
    update["phatanalog1"] = automationhat.analog.two.read()
    update["phatanalog2"] = automationhat.analog.three.read()
    update["phatinput0"] = bool_state_format(automationhat.input.one.read())
    update["phatinput1"] = bool_state_format(automationhat.input.two.read())
    update["phatinput2"] = bool_state_format(automationhat.input.three.read())

    update["phatrelay"] = bool_state_format(automationhat.relay.one.is_on())
    update["phatoutput0"] = bool_state_format(automationhat.output.one.is_on())
    update["phatoutput1"] = bool_state_format(automationhat.output.two.is_on())
    update["phatoutput2"] = bool_state_format(automationhat.output.three.is_on())

    (result,mid)=mqttc.publish(hass_autogen_topic + cid + "/state", json.dumps(update), qos=1, retain=True)
    
    return update

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

def sigterm_handler(signal, frame):
    # save the state here or do whatever you want
    logging.info('booyah! bye bye')
    print("sigterm handler")
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)

def sigint_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)
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
            details = sbc_rpi0_envirophat()
        if sbc_type == "automationphat":
            details = sbc_rpi0_automationphat()
            #print(str(time.time()) + " : " + str(details)) # needs a real logger here
        time.sleep(0.5)
except Exception as e:
    logging.critical("Exception while running: " + repr(e))
finally:
    (result,mid)=mqttc.publish("status/" + cid, "offline", qos=1, retain=True)
    mqttc.loop_stop()
    mqttc.disconnect()
    logging.info("Program shutting down, MQTT client cleaned up and disconnected")
logging.info("Goodnight...")
print("after finally")