from flask import Flask, request, jsonify
from dapr.clients import DaprClient
from cloudevents.http import from_http
from cloudevents.conversion import  to_structured
import json
import os
import logging


app = Flask(__name__)
client = DaprClient()
app_port = os.getenv('APP_PORT', '5001')
pubsub_name = 'orderpubsub'
sub_topic = 'orders_request'
publish_topic = "orders_response"

# https://github.com/dapr/quickstarts/blob/master/pub_sub/python/sdk/order-processor/app.py
# Register Dapr pub/sub subscriptions
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
    return json.dumps({'status': "Order-processor is Running"}), 200, {'ContentType': 'application/json'}


# Dapr subscription in /dapr/subscribe sets up this route
@app.route('/' + sub_topic, methods=['POST'])
def orders_subscriber():
    event = from_http(request.headers, request.get_data())
    print("=================Begin Order Processor=====================", flush=True)
    # print(str(request.headers))
    print("Receiving message from publisher...")
    headers, data = to_structured(event)
    data_dict = json.loads(data)
    print('Received event from topic :', sub_topic)
    print('Subscriber received : %s' % event.data.get('orderId', "No order id found"), flush=True)
    print('Subscriber type : %s' % event.data.get("type","default-redis"), flush=True)
    print("headers=> ", json.dumps(headers,indent=4))
    print("message=> ", json.dumps(data_dict,indent=4))  

    data_dict['status'] = "Processed"
    print('Sending response to :', publish_topic)
    client.publish_event(
        pubsub_name=pubsub_name,
        topic_name=publish_topic,
        data=json.dumps(data_dict),
        data_content_type='application/json',
    )


    print("====================End Order Processor==================", flush=True)
    return json.dumps({'success': True}), 200, {
        'ContentType': 'application/json'}


app.run(port=app_port)
