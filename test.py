import unittest
from blackjack import Play_Blackjack

class Test_Blackjack(unittest.TestCase):

    # test dealt two aces right off the bat
    def test_dealt_aces(self):
        test_game = Play_Blackjack()
        test_game.the_player.add_card(["Ah",11])
        test_game.the_player.add_card(["As",11])
        test_game.the_dealer.add_card(["Ad",11])
        test_game.the_dealer.add_card(["Ac",11])
        test_game.first_two_are_aces()
        self.assertEquals(test_game.the_player.cards, [["Ah",1],["As",11]])
        self.assertEquals(test_game.the_player.card_total, 12)
        self.assertEquals(test_game.the_dealer.cards, [["Ad",1],["Ac",11]])
        self.assertEquals(test_game.the_dealer.card_total, 12)

    def test_dealer_aces_reduce(self):
        test_game = Play_Blackjack()
        test_game.the_dealer.add_card(["As",11])
        test_game.the_dealer.add_card(["4c",4])
        test_game.dealer_turn()


if __name__ == '__main__':
    unittest.main()