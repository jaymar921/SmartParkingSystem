from flask import Flask, request, json
from flask_cors import CORS
from dataholder import DataHolder
from models import Card

app = Flask(__name__)
CORS(app)

dataHolder = DataHolder()

@app.route("/")
def webapp():
    return "http://192.168.1.50:8000/"

@app.route("/api/cards", methods = ['GET', 'POST', 'PUT', 'DELETE'])
def api_allCards():
    if request.method.lower() == 'get':
        all_cards = dataHolder.getAllCards()
        parsed_cards: list = []
        for card in all_cards:
            parsed_cards.append(card.toJSON())
        response = app.response_class(
            response=json.dumps(parsed_cards, indent=4,
                                sort_keys=False, default=str),
            status=200,
            mimetype='application/json'
        )
        return response
    elif request.method.lower() == 'put':
        try:
            uid = str(request.get_json()['uid'])
            card: Card = dataHolder.getCard(uid)
            card.name = request.get_json()['name']
            card.balance = float(request.get_json()['balance'])
            print(f"updated - {card.toJSON()}")
        except Exception as e:
            print(f"error {e}")
            return {'status':'500'}
    elif request.method.lower() == 'delete':
        try:
            uid = str(request.get_json()['uid'])
            dataHolder.removeCard(uid)
            print(f"removed card - {uid}")
        except Exception as e:
            print(f"error {e}")
            return {'status':'500'}
    elif request.method.lower() == 'post':
        try:
            uid = str(request.get_json()['uid'])
            name = request.get_json()['name']
            balance = float(request.get_json()['balance'])
            dataHolder.registerCard(Card(uid, name, balance))
            print(f"registered - {uid}")
        except Exception as e:
            print(f"error {e}")
            return {'status':'500'}
    return {'status':'200'}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)