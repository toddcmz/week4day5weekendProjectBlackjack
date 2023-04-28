from deck import Deck
from participants import *
from os import system, name
import time

class Play_Blackjack():
    
    def __init__(self):
        self.game_deck = Deck()
        self.the_dealer = Dealer()
        self.the_player = Player()

    def main(self):
        self.continue_playing()

    def continue_playing(self):
        user_choice = self.input_player_continues_playing()
        time.sleep(0.3)
        if user_choice == "1":
            self.reset_player()
            self.reset_dealer()
            # if we're low on cards, also reset the deck
            if len(self.game_deck.deck) < 18:
                self.reset_deck()
            self.start_next_hand()
        else:
            return

    def start_next_hand(self):
        # deal two cards to each player, in proper dealing order
        self.clear()
        self.the_player.add_card(self.deal_single_card())
        self.the_dealer.add_card(self.deal_single_card())
        self.the_player.add_card(self.deal_single_card())
        self.the_dealer.add_card(self.deal_single_card())
        self.check_blackjack()
    
    def deal_single_card(self):
        return self.game_deck.deck.pop()

    def check_blackjack(self):
        if self.the_dealer.card_total == 21:
            print("Dealer was dealt blackjack")
            time.sleep(0.3)
            self.show_all_dealer_cards()
            if self.the_player.card_total == 21:
                print("Player was also dealt blackjack, it's a tie.")
                time.sleep(0.3)
                self.show_player_cards()
                self.pushed()
            else:
                print("Player was not dealt blackjack, player automatically loses.")
                time.sleep(0.3)
                self.show_player_cards()
                self.dealer_wins()
        elif self.the_player.card_total == 21:
            print("Player was dealt blackjack and dealer was not dealt blackjack, player wins.")
            time.sleep(0.3)
            self.show_player_cards()
            self.player_wins()
        else:
            self.player_turn()

    def show_player_cards(self):
        # print just the face and not the value
        temp_cards = []
        for ele in self.the_player.cards:
            temp_cards.append(ele[0])
        print(f'Player cards: {temp_cards}')
        time.sleep(0.3)

    def show_player_total(self):
        print(f'Player has {self.the_player.card_total}')
        time.sleep(0.3)

    def show_all_dealer_cards(self):
        # print just the face and not the value
        temp_cards = []
        for ele in self.the_dealer.cards:
            temp_cards.append(ele[0])
        print(f'Dealer cards: {temp_cards}')
        time.sleep(0.3)

    def show_public_dealer_cards(self):
        # print just face and not value, and don't show the first card
        temp_cards = ["??"]
        for i in range(1,len(self.the_dealer.cards)):
            temp_cards.append(self.the_dealer.cards[i][0])
        print(f'Dealer cards: {temp_cards}')
        time.sleep(0.3)

    def show_all_dealer_total(self):
        print(f'Dealer has {self.the_dealer.card_total}')
        time.sleep(0.3)

    def show_public_dealer_total(self):
        # public total is grand total minus the value of the dealer's first card, which is hidden
        public_total = self.the_dealer.card_total - self.the_dealer.cards[0][1]
        print(f'Dealer is showing {public_total}')
        time.sleep(0.3)

    def player_turn(self):
        self.show_player_cards()
        self.show_player_total()
        time.sleep(0.3)
        self.show_public_dealer_cards()
        time.sleep(0.3)
        user_choice = self.input_hit_or_stay()
        self.player_choice_handler(user_choice)

    def player_choice_handler(self, user_choice):
        if user_choice == "1":
            self.chooses_hit()
        else:
            print("Player stays with:")
            time.sleep(0.3)
            self.show_player_cards()
            time.sleep(0.3)
            self.show_player_total()
            time.sleep(0.3)
            print("Dealer takes their turn:")
            time.sleep(0.3)
            self.dealer_turn()
        
    def input_hit_or_stay(self):
        user_choice = "0"
        while user_choice not in ("1","2"):
            try:
                user_choice = input("1 to hit, 2 to stay: ")
                if user_choice not in ("1","2"):
                    self.one_or_two_input_error()
            except:
                self.one_or_two_input_error()
        return(user_choice)

    def chooses_hit(self):
        print("Player hits.")
        time.sleep(0.3)
        hit_card = self.game_deck.deck.pop()
        print(f'Player draws: {hit_card[0]}')
        time.sleep(0.3)
        self.the_player.add_card(hit_card)
        self.player_checks_total()

    def player_checks_total(self):
        if self.the_player.card_total < 22:
            self.player_turn()
        else:
            self.player_busts()

    def player_busts(self):
        print("You've busted. You lose.")
        time.sleep(0.3)
        self.show_player_cards()
        time.sleep(0.3)
        self.show_player_total()
        self.dealer_wins()

    def dealer_turn(self):

        while self.the_dealer.card_total < 16:
            print("Dealer hits")
            time.sleep(0.6)
            self.the_dealer.add_card(self.game_deck.deck.pop())
            print("Dealer now has:")
            time.sleep(0.6)
            self.show_public_dealer_cards()
            time.sleep(0.6)
            self.show_public_dealer_total()
            time.sleep(0.6)
        if self.the_dealer.card_total > 21:
            self.dealer_busts()
        else:
            print("Dealer stays.")
            time.sleep(0.6)
            self.compare_totals()

    def dealer_busts(self):
        print("Dealer busts, you win!")
        time.sleep(0.6)
        self.show_all_dealer_cards()
        time.sleep(0.6)
        self.show_all_dealer_total()
        time.sleep(0.6)
        self.player_wins()
    
    def compare_totals(self):
        print(f"Dealer's first card was {self.the_dealer.cards[0][0]}")
        time.sleep(0.6)
        self.show_all_dealer_total()
        time.sleep(0.6)
        self.show_all_dealer_cards()
        time.sleep(0.6)
        if self.the_player.card_total > self.the_dealer.card_total:
            self.player_wins()
        elif self.the_player.card_total == self.the_dealer.card_total:
            self.pushed()
        else:
            self.dealer_wins()

    def player_wins(self):
        print("Congratulations, you won!")
        time.sleep(0.3)
        self.continue_playing()

    def dealer_wins(self):
        print("The dealer won that one.")
        time.sleep(0.3)
        self.continue_playing()

    def pushed(self):
        print("You and the dealer pushed. This hand is a draw.")
        time.sleep(0.3)
        self.continue_playing()

    def input_player_continues_playing(self):
        user_choice = "0"
        while user_choice not in ("1","2"):
            try:
                user_choice = input("1 to play another hand, 2 to quit playing: ")
                if user_choice not in ("1","2"):
                    self.one_or_two_input_error()
            except:
                self.one_or_two_input_error()
        return(user_choice)

    def one_or_two_input_error(self):
        print("You didn't enter 1 or 2. Try again.")
        time.sleep(0.3)

    def reset_player(self):
        self.the_player.card_total = 0
        self.the_player.cards = []

    def reset_dealer(self):
        self.the_dealer.card_total = 0
        self.the_dealer.cards = []

    def reset_deck(self):
        print("Running low on cards, reshuffling the deck.")
        time.sleep(0.6)
        self.game_deck = Deck()
        print("Deck reshuffled.")
        time.sleep(0.6)

    def clear(self):
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')