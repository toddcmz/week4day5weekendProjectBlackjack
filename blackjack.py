from deck import Deck
from participants import *
from os import system, name
import time

class Play_Blackjack():
    
    def __init__(self):
        self.game_deck = Deck()
        self.the_dealer = Dealer()
        self.the_player = Player()
        self.player_win_count = 0
        self.dealer_win_count = 0
        self.total_pushes = 0

    def main(self):
        while True:
            keep_playing = self.input_player_continues_playing()
            if keep_playing in ("2", "q"):
                return self.game_summary()
            self.continue_playing() # this method has 3 internal methods that reset player, reset dealer, and reset the deck
            self.start_next_hand()
            is_blackjack = self.check_blackjack()
            if is_blackjack == "tie":
                self.pushed()
                continue
            elif is_blackjack == "dealer":
                self.dealer_wins()
                continue
            elif is_blackjack == "player":
                self.player_wins()
                continue
            after_hitting_result = "under"                                                        # this whole block could
            hit_or_stay_result = "1"                                                              # turn into a single method.
            while after_hitting_result == "under" and hit_or_stay_result == "1":                  # The method would be player_turn(),
                hit_or_stay_result = self.player_turn()                                           # and would in that case have to be
                if hit_or_stay_result == "q":                                                     # just one complicated method, sort of
                    return self.game_summary()                                                    # like dealer turn, but with input calls
                elif hit_or_stay_result == "1":                                                   # or it would need to have multiple hidden
                    self.chooses_hit()                                                            # method calls that don't show up in the driver
                    after_hitting_result = self.player_checks_total()                             # what's the best option for this?
                # if we're here in while loop, this is where hit_or_stay_result                   # keep complicated driver code, or convert to one method?
                # could equal "2", meaing move on,
                # or after_hitting_result could equal "bust," which would also move us on. otherwise
                # we're still in while loop and ask if you want to hit again.
            if after_hitting_result == "busts":
                self.player_busts()
                self.dealer_wins()
                continue 
            self.chooses_stay()
            dealer_result = self.dealer_turn()
            if dealer_result == "dealer_busts":
                self.dealer_busts()
                self.player_wins()
                continue
            final_result = self.compare_totals()
            if final_result == "player_wins":
                self.player_wins()
                continue
            elif final_result == "pushed":
                self.pushed()
                continue
            self.dealer_wins()

    def input_player_continues_playing(self):
        user_choice = "0"
        while user_choice not in ("1","2","q"):
            try:
                user_choice = input("1 to play another hand, 2 or 'q' to quit playing: ")
                if user_choice not in ("1","2","q"):
                    self.one_or_two_input_error()
            except:
                self.one_or_two_input_error()
        return(user_choice)

    def continue_playing(self):
        time.sleep(0.3)
        self.reset_player()
        self.reset_dealer()
        # if we're low on cards, also reset the deck
        if len(self.game_deck.deck) < 18:
            self.reset_deck()

    def start_next_hand(self):
        # deal two cards to each player, in proper dealing order
        self.clear()
        self.the_player.add_card(self.deal_single_card())
        self.the_dealer.add_card(self.deal_single_card())
        self.the_player.add_card(self.deal_single_card())
        self.the_dealer.add_card(self.deal_single_card())
    
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
                return "tie" 
            else:
                print("Player was not dealt blackjack, player automatically loses.")
                time.sleep(0.3)
                self.show_player_cards()
                return "dealer"
        elif self.the_player.card_total == 21:
            print("Player was dealt blackjack and dealer was not dealt blackjack, player wins.")
            time.sleep(0.3)
            self.show_player_cards()
            return "player"
        else:
            return # I think this will allow my flow to work properly after this stage in main
            
    def player_turn(self):
        self.show_player_cards()
        self.show_player_total()
        time.sleep(0.3)
        self.show_public_dealer_cards()
        time.sleep(0.3)
        hit_or_stay = self.input_hit_or_stay()
        return hit_or_stay
        
    def input_hit_or_stay(self):
        user_choice = "0"
        while user_choice not in ("1","2","q"):
            try:
                user_choice = input("1 to hit, 2 to stay, 'q' to quit playing: ")
                if user_choice not in ("1","2","q"):
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

    def player_checks_total(self):
        if self.the_player.card_total < 22:
            return("under")
        else:
            return("busts")

    def player_busts(self):
        print("You've busted. You lose.")
        time.sleep(0.3)
        self.show_player_cards()
        time.sleep(0.3)
        self.show_player_total()

    def chooses_stay(self):
        print("Player stays with:")
        time.sleep(0.3)
        self.show_player_cards()
        time.sleep(0.3)
        self.show_player_total()
        time.sleep(0.3)
        print("Dealer takes their turn:")
        time.sleep(0.3)

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
            return("dealer_busts")
        else:
            print("Dealer stays.")
            time.sleep(0.6)
            return("dealer_stays")

    def dealer_busts(self):
        print("Dealer busts, you win!")
        time.sleep(0.6)
        self.show_all_dealer_cards()
        time.sleep(0.6)
        self.show_all_dealer_total()
        time.sleep(0.6)
    
    def compare_totals(self):
        print(f"Dealer's first card was {self.the_dealer.cards[0][0]}")
        time.sleep(0.6)
        self.show_all_dealer_total()
        time.sleep(0.6)
        self.show_all_dealer_cards()
        time.sleep(0.6)
        if self.the_player.card_total > self.the_dealer.card_total:
            return("player_wins")
        elif self.the_player.card_total == self.the_dealer.card_total:
            return("pushed")
        else:
            return("dealer_wins")

    def player_wins(self):
        print("Congratulations, you won!")
        time.sleep(0.3)
        self.player_win_count +=1

    def dealer_wins(self):
        print("The dealer won that one.")
        time.sleep(0.3)
        self.dealer_win_count +=1

    def pushed(self):
        print("You and the dealer pushed. This hand is a draw.")
        time.sleep(0.3)
        self.total_pushes +=1

    def game_summary(self):
        print("Thanks for playing.")
        print(f"Player won {self.player_win_count} game(s).")
        print(f"Dealer won {self.dealer_win_count} game(s).")
        print(f"{self.total_pushes} game(s) resulted in a tie.")

    def one_or_two_input_error(self):
        print("You didn't enter 1, 2, or q. Try again.")
        time.sleep(0.3)

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