from dapr.clients import DaprClient
from flask import Flask, request, jsonify
import json
import time
import logging
from cloudevents.http import from_http
from cloudevents.conversion import  to_structured

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
client = DaprClient()

pubsub_name = 'orderpubsub'
publish_topic = "orders_request"
sub_topic = 'orders_response'

@app.route('/dapr/subscribe', methods=['GET'])
def subscribe():
    subscriptions = [
        {
            'pubsubname': pubsub_name,
            'topic': sub_topic,
            'route': sub_topic
        },
    ]
    print('Dapr pub/sub is subscribed to: ' + json.dumps(subscriptions))
    return jsonify(subscriptions)


@app.route('/', methods=['GET'])
def health():
    return json.dumps({'status': "Checkout is Running"}), 200, {'ContentType': 'application/json'}


@app.route("/publish", methods=['POST'])
def hello():
    data = request.get_json()
    value = data.get("orderId")
    # for i in range (1,4):
    order = {'orderId': (value)}
    print("=================Begin Checkout=====================", flush=True)
    # Publish an event/message using Dapr PubSub
    result = client.publish_event(
        pubsub_name=pubsub_name,
        topic_name=publish_topic,
        data=json.dumps(order),
        data_content_type='application/json',
    )
    print('Published data: ' , json.dumps(order, indent=4))
    print("====================End Checkout==================", flush=True)
    
    return jsonify(
            {
                "publish_order":order, 
            
            }        
        )

# Dapr subscription in /dapr/subscribe sets up this route
@app.route('/' + sub_topic, methods=['POST'])
def orders_response():
    event = from_http(request.headers, request.get_data())
    print("=================Begin Checkout=====================", flush=True)
    # print(str(request.headers))
    print("Receiving response from orders...")
    headers, data = to_structured(event)
    data_dict = json.loads(data)
    print("headers=> ", json.dumps(headers,indent=4))
    print("message=> ", json.dumps(data_dict,indent=4))  

    print("====================End Checkout==================", flush=True)
    return json.dumps({'success': True}), 200, {
        'ContentType': 'application/json'}



if __name__ == "__main__":
    app.run(port=3000)
