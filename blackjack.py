from base64 import standard_b64decode
import random

ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
suits = ('\u2663', '\u2660', '\u2666', '\u2665')
play_again = True

values = {'2': 2,
          '3': 3,
          '4': 4,
          '5': 5,
          '6': 6,
          '7': 7,
          '8': 8,
          '9': 9,
          '10': 10,
          'J': 10,
          'Q': 10,
          'K': 10,
          'A': 11}

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return self.rank + '' + self.suit

class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(rank, suit))

    def __str__(self):
        full_deck = ''
        for card in self.deck:
            full_deck += '\n' + card.__str__()
        return 'The deck has: ' + full_deck
    
    def shuffle_deck(self):
        random.shuffle(self.deck)

    def deal(self):
        one_card = self.deck.pop()
        return one_card

class Hand:
    def __init__(self, dealer):
        self.cards = []
        self.value = 0
        self.ace = False
        self.dealer = dealer

    def show_cards(self, stand):
        if self.dealer and stand == False:
            card_out = ''
            card_out += '[hidden] '
            card_out += self.cards[1].__str__()
        elif self.dealer and stand == True:
            card_out = ''
            for card in self.cards:
                card_out += card.__str__() + ' '
        else:
            card_out = ''
            for card in self.cards:
                card_out += card.__str__() + ' '
        return card_out

    def deal_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'A':
            self.ace = True
    
    def if_ace(self):
        while self.value > 21:
            self.value -= 10
            self.ace = False

class Play:
    def __init__(self, player_hand, dealer_hand):
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand

    def show_hand(self):
        print("\nPlayer's Hand: " + self.player_hand.show_cards(False))
        print("Player's Hand Value: " + str(self.player_hand.value) + "\n")
        print("Dealers's Showing: " + self.dealer_hand.show_cards(False))
    
    def show_full_hand(self):
        print("\nPlayer's Hand: " + self.player_hand.show_cards(False))
        print("Player's Hand Value: " + str(self.player_hand.value) + "\n")
        print("Dealer's Hand: " + self.dealer_hand.show_cards(True))
        print("Dealer's Hand Value: " + str(self.dealer_hand.value))

    def hit_or_stand(self):
        good_answer = False

        if self.player_hand.value == 21:
            return 'won'
        
        while good_answer == False:
            hit_or_stand_selection = input("\nWould you like to hit or stand (H/S): ")

            if hit_or_stand_selection.lower() == 'h':
                good_answer = True
                return 'hit'
            elif hit_or_stand_selection.lower() == 's':
                good_answer = True
                return 'stand'
            else:
                good_answer = False
                print("\nInvalid input try again!")

    def find_winner(self):
        if self.player_hand.value > self.dealer_hand.value:
            print("\nYou have WON!! Congratulations!\n")
        elif self.dealer_hand.value > 21:
            print('\nDealer has BUSTED! You WIN!!!\n')
        elif self.player_hand.value == self.dealer_hand.value:
            print("\nIt's a tie!! No winner.\n")
        else: 
            print("\nDealer WINS!!! Sorry :(\n")

while play_again:
    print("\n----------------------------------")
    print("| Welcome to the Blackjack table |")
    print("----------------------------------")
    
    deck = Deck()
    deck.shuffle_deck()

    p_hand = Hand(False)
    p_hand.deal_card(deck.deal())
    p_hand.deal_card(deck.deal())

    d_hand = Hand(True)
    d_hand.deal_card(deck.deal())
    d_hand.deal_card(deck.deal())

    playing = True

    play_game = Play(p_hand, d_hand)

    while playing == True:
        if play_game.player_hand.ace:
            play_game.player_hand.if_ace()
        elif play_game.player_hand.ace: 
            play_game.dealer_hand.if_ace()

        play_game.show_hand()
        if play_game.player_hand.value > 21:
            print("\nYou have busted!\nDealer WINS!!! Sorry :(\n")
            break
        elif play_game.player_hand.value == 21 and play_game.player_hand.value != play_game.dealer_hand.value and len(play_game.player_hand.cards) == 2:
            print("\nBLACKJACK!! You WIN!\n")
            break
        elif play_game.player_hand.value == 21 and play_game.player_hand.value == play_game.dealer_hand.value:
            play_game.find_winner()
            break
        else:
            user_selection = play_game.hit_or_stand()

            if user_selection == 'hit':
                play_game.player_hand.deal_card(deck.deal())
            elif user_selection == 'stand' or 'won':
                play_game.show_full_hand()
                while play_game.dealer_hand.value < 17:
                    print("\nDealer hits")
                    play_game.dealer_hand.deal_card(deck.deal())
                    if play_game.dealer_hand.ace:
                        play_game.dealer_hand.if_ace()
                    play_game.show_full_hand()

                play_game.find_winner()
                break
    bad_input = True
    while bad_input:
        user_play_again = input("Would you like to play again (Y/N): ")

        if user_play_again.lower() == 'n':
            play_again = False
            bad_input = False
        elif user_play_again.lower() == 'y':
            play_again = True
            bad_input = False
        else:
            print("\nInvalid input try again!\n")
        
    
