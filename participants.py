class Participants():
    
    def __init__(self, bankroll = 1000):
        self.card_total = 0
        self.bankroll = bankroll
        self.cards = []

    def add_card(self, this_card):
        self.cards.append(this_card)
        self.card_total += this_card[1]

class Player(Participants):
    
    def __init__(self):
        super().__init__(self)

    def wager(self):
        pass

class Dealer(Participants):

    def __init__(self):
        super().__init__(self)
