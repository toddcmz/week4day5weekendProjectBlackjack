from random import shuffle

class Deck():
    
    def __init__(self):
        self.deck = []
        self.generate_deck()

    def generate_deck(self):
        # define suits, cards, and numeric value of each card, card will be a tuple.
        suits = ["c", "d", "h", "s"]
        ranks = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
        values = [2,3,4,5,6,7,8,9,10,10,10,10,11]
        # loop through each suit and card
        for suit in suits:
            for index_rank in range(len(ranks)):
                this_card = ranks[index_rank]+suit
                self.deck.append([this_card, values[index_rank], "./cardFaces/"+this_card+".png"])
        # shuffle resulting deck
        shuffle(self.deck)

