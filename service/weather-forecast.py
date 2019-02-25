from flask import Flask, request, Response
import os
import requests
import logging
import json
import time

app = Flask(__name__)
logger = None
format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger('weather-forecast-service')

# Log to stdout

stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(logging.Formatter(format_string))
logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)

def stream_json(testing):
    first = True
    yield '['
    for i, row in enumerate(testing):
        if not first:
            yield ','
        else:
            first = False
        yield json.dumps(row)
    yield ']'

@app.route("/get", methods=["POST"])
def get():
    testing = []
    entities= request.get_json()
    for entity in entities:

        zip = entity['difi-postnummer:postnummer']
        country = 'no'
        url = os.environ.get('baseurl')+ zip + ',' + country + os.environ.get('appid')

        r = requests.get(url)
        res = json.loads(r.text)
        time.sleep(1)
    for i in range(len(entities)):
        testing.append(res)
        i += 1


    return Response(stream_json(testing),
                    mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True, port=os.environ.get('port',5000))
