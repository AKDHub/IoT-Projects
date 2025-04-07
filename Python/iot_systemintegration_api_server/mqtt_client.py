import json
import paho.mqtt.client as paho
import random
from database.locksmith_db import LocksmithDB
import base64


CLIENT_ID = f'locksmith-mqtt-{random.randint(0, 1000)}'
USERNAME = ''
PASSWORD = ''
BROKER = 'broker.hivemq.com'
PORT = 1883

locksmith_db = LocksmithDB()


class MQTTClient:
    """ MQTT Client instance for a topic and username. """
    def __init__(self, username, topic):
        self.username = username
        self.topic = topic
        self.client = None
        self.connect_mqtt()

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Connected to Locksmith Server.')
        else:
            print(f'Error connecting to Locksmith Server. Error code {rc}')

    def connect_mqtt(self):
        """ Set mqtt client parameters and connect to broker."""

        self.client = paho.Client(CLIENT_ID)
        self.client.username_pw_set(USERNAME, PASSWORD)
        self.client.on_connect = self.on_connect
        self.client.will_set(self.topic, f"{self.username} has disconnected from the MQTT Broker.")

        self.client.connect(BROKER, PORT)

    def on_message(self, client: paho.Client, userdata, message):
        """ Handling incoming messages on the subscribed topic. """
        if message.payload.decode("utf-8").startswith(f'{self.username}'):
            pass
        else:
            self.decode_message(message.payload.decode("utf-8"))

    def init_client(self):
        """ Initiate client and start listening. """
        # Subscribe to selected topic
        self.client.subscribe(self.topic)
        # Set the on_message callback function
        self.client.on_message = self.on_message

        # Start the paho client loop
        self.client.loop_start()

        self.client.publish(topic=self.topic, payload=f"{self.username} is listening.", qos=0, retain=False)

    def publish(self, msg_to_send):
        """ Publish message to subscribed topic. """
        self.client.publish(topic=self.topic, payload=msg_to_send, qos=0, retain=False)

    def run(self):
        """ Start mqtt client """
        self.init_client()

    def decode_message(self, message64):
        """ Decodes a message received on subscribed topic. """
        try:
            msg = self.decode_txt64(message64)
            msg_json = json.loads(msg)
            print(type(msg_json))
            print(msg)

            if msg_json['header']['type'] == 'check_code':
                code = int(msg_json['body']['text'])
                door_id = int(msg_json['header']['door_id'])
                print(f"Received code: {code}")
                # Check if code is valid and return its user
                valid_code, username = locksmith_db.valid_code(door_id, code)

                # Open door with door_id if code is valid
                if valid_code:
                    print("Publish: open")
                    self.publish(msg_to_send=f"open_{door_id}")

                # Logg attempted access in database
                locksmith_db.logg_attempted_access(door_id=door_id,
                                                   username=username,
                                                   source='Keypad')

        except Exception as e:
            print(f"Unexpected error: {e}")

    @staticmethod
    def decode_txt64(txt64: str) -> str:
        """ Decodes a base64 string to ascii string."""
        base64_bytes = txt64.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        return message_bytes.decode('ascii')


if __name__ == '__main__':
    mqtt_client = MQTTClient("Simon", "api")
