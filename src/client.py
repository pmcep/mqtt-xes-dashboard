import paho.mqtt.client as mqtt
import psycopg2


MQTT_TOPIC = "pmcep/#"
MQTT_HOST = "broker.mqttdashboard.com"
MQTT_PORT = 1883
MQTT_TIMEOUT = 60

con = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="postgres", port="5432")

# Setup database
cur = con.cursor()
#cur.execute('''DROP TABLE IF EXISTS event''')
cur.execute('''CREATE TABLE IF NOT EXISTS event
      (
        date            TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
        source          TEXT    NOT NULL,
        processinstance TEXT    NOT NULL,
        activity        TEXT    NOT NULL
      );''')
con.commit()

# Mqtt connect
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)

# Mqtt on message
def on_message(client, userdata, msg):
    # Read data from topic name
    [base, source_id, processinstance_id, activity_name] = msg.topic.split("/")

    # Store message
    cur = con.cursor()
    cur.execute('INSERT INTO event (source, processinstance, activity) VALUES (%s, %s, %s)', (str(source_id), str(processinstance_id), str(activity_name)))
    con.commit()

    # Log message
    print(source_id, processinstance_id, activity_name)


# Setup mqtt client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT, MQTT_TIMEOUT)
client.loop_forever()
