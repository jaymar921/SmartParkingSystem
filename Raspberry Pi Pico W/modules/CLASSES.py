class Card:
    def __init__(self, uid, name, balance):
        self.uid = str(uid)
        self.balance = balance
        self.name = name
        self.time_parked = -1