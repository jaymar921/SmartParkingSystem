class Card:
    def __init__(self, uid, name, balance):
        self.uid: str = uid
        self.name: str = name
        self.balance: float = balance
    
    def toJSON(self):
        return {
            "uid":self.uid,
            "name":self.name,
            "balance":self.balance
        }