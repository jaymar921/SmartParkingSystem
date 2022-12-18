from models import Card
class DataHolder:
    def __init__(self):
        self.CARDS: list = []
        self.CARDS.append(Card('1068049966', 'Jayharron Mar Abejar', 0.0))
        self.CARDS.append(Card('1068049963', 'Hello World', 0.0))

    def registerCard(self, card: Card):
        self.CARDS.append(card)

    def getAllCards(self):
        return self.CARDS
    
    def removeCard(self, uid: str):
        to_remove: Card = None
        for card in self.CARDS:
            if card.uid == uid:
                to_remove = card
        self.CARDS.remove(to_remove)
    
    def getCard(self, uid: str) -> Card:
        for card in self.CARDS:
            if card.uid == uid:
                return card
        return None
