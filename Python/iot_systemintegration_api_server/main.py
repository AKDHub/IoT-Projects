import json
from flask import Flask, request, jsonify
from mqtt_client import MQTTClient
from database.locksmith_db import LocksmithDB
import locksmith_client
from flask_swagger_ui import get_swaggerui_blueprint
import threading


app = Flask(__name__)
# Initiate MQTT Client
topic = 'topic/APIGatewayAliSimon'
mqtt_client = MQTTClient("Flask-Server", topic=topic)
# Initiate Database
locksmithDB = LocksmithDB()

#region SWAGGER UI SETTINGS
SWAGGER_URL = "/locksmith/docs"
API_URL = "/static/locksmith_doc.yml"  # os.path.abspath(os.path.dirname(__file__)) +

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Coffee Review API"
    }
)
app.register_blueprint(swaggerui_blueprint)
#endregion

@app.route('/')
@app.route('/locksmith')
def home_page():
    return app.redirect('/locksmith/docs')


@app.route('/locksmith/doors', methods=['GET'])
def get_doors():
    username = request.json['header']['username']
    if request.method == 'GET':
        return app.response_class(
            response=json.dumps(locksmithDB.get_user_doors(username)),
            status=200,
            mimetype='application/json'
        )


@app.route('/locksmith/doors/<door_id>', methods=['POST'])
def get_door_id(door_id):

    if request.method == 'POST':

        content = request.json
        print(type(content))

        mqtt_client.publish(content['body']['text'])
        locksmithDB.logg_attempted_access(door_id=door_id,
                                          username=content['header']['username'], source='client')

        return app.response_class(
            response=json.dumps({'response': f'Door{door_id} is open'}),
            status=201,
            mimetype='application/json'
        )


@app.route('/locksmith/doors/<door_id>/loggs', methods=['GET'])
def get_loggs(door_id):

    if request.method == 'GET':
        return app.response_class(
            response=json.dumps(locksmithDB.get_loggs(door_id)),
            status=200,
            mimetype='application/json'
        )


if __name__ == '__main__':
    mqtt_client.run()
    thread = threading.Thread(target=locksmith_client.LocksmithClient.run)
    thread.start()
    app.run(host='0.0.0.0', port=5050, debug=False)



