# blackjack

# computer --> dealer
# you --> player
# player owns x-amount of money


# 2 cards each
# player can decide to HIT or STAY
# if player HIT:
#   player gets another card
# if player STAY:
#   they stop receiving cards, stays at the sum

# After player stays, dealer can HIT or STAY as well
# both party reveals cards, whoever is cloest to 21 w/o going over 21 wins


# Approach:
# 1. make a deck of cards and mark its values
# 2. give player 2 cards along w/ info on which cards
# 3. prompt player to HIT or STAY
# 4. If HIT, give new card along w/ info
#       repeat step three until they choose STAY
# 5. If STAY, reveal the dealer's hand
# 6. compare values and display winner
import random


suits = ('H','D','S','C')
rankings = ('A', '2','3','4','5','6','7','8','9','10','J','Q','K')
card_val = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}

chip_pool = 100
print("Your buy-in amount is ", chip_pool)
class Card:    # helps make a card
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    # makes sure what u return is in str format
    def __str__(self):
        return self.suit + self.rank
    def grab_suit(self):
        return self.suit
    def grab_rank(self):
        return self.rank
    def draw(self):
        print(self.suit + self.rank)
# this is an object of Card class
# suits and rankings are arguments to the Card() class
#       arguments are whatever you pass into the function to plug into the parameters
#       what u put into the function before the function like goes

class Hand: # find out whats in ur hand
    def __init__(self):
        self.cards = []
        self.value = 0

        # Aces can be 1 or 11
        # t or f r "flags"
        self.ace = False

    def __str__(self):
        # return a string of current hand composition
        hand_comp = ""

        for card in self.cards:
            card_name = card.__str__()
            # allows the return to be in str format
            hand_comp += " " + card_name
            # += is add the thing to self and  " " is just to put a space in between the cards
        return "the hand has" + hand_comp
    def card_add(self, card):
        # this will add a card to our hand
        self.cards.append(card)
        if card.rank == 'A': # if theres an ace
            self.ace = True
        # get the value of this card and add to total value
        value = card_val[card.rank]
        self.value += value
    def calc_val(self):
        # this function will calculate the value of hand (HINT: A = 1 or 11)!
        if(self.ace == True and self.value < 12):
            # goes through if you have an ace & total value w/ ace (which is one at the moment) is less than 12
            return self.value + 10
            # adds 10 instead of 11 bc u already have 1 in the total value from the og ace, and 1 + 10 is 11!
        else:
            return self.value
    def draw(self, hidden):
        if hidden == True:
            starting_card = 1
            # if theres a hidden card, print index number 1 only bc index 0 is now "hidden"
        else:
            starting_card = 0
            # prints both cards bc none of them r hidden
        for x in range(starting_card, len(self.cards)):
            self.cards[x].draw()
            # prints out hand

# hand = Hand()
# # print(hand)
# hand.card_add(Card("S","5"))
# hand.card_add(Card("H", "A"))
# hand.draw(True)
# hand.calc_val()
# print(hand)
# print(hand.calc_val())

class Deck:
    def __init__(self):
        # creating the deck in order
        self.deck = []
        for rank in rankings:
            for suit in suits:
                card = Card(suit, rank)
                self.deck.append(card)
    def shuffle(self):
        # This function will shuffle the deck
        random.shuffle(self.deck)
    def deal(self):
        # This function will spit out one card from the top of deck
        single_card = self.deck.pop()
        # pop takes a card out of the deck and gives the function info abt the card
        return single_card
# deck.__init__()   --> call init function

# END OF CLASSES

# BETTING TIME
def make_bet():
    global bet_amount, chip_pool
    bet_amount = (input("What amount of chips would you like to bet? "))
    # ask the player for bet amount
    if bet_amount.isnumeric(): # checks if its number
        if int(bet_amount) <= chip_pool: # compares integer version of number to chip_pool
            bet_amount = int(bet_amount)  # turns it into an integer
        else:
            print("Invalid amount entered, please try again!!")
            make_bet()
    else:
        print("Invalid amount entered, please try again!!")
        make_bet()
def remaining_amount(win):  # parameter is false or true -> written in hit or stand
    global chip_pool, bet_amount
    if win == True: # bascially if they win or not
        chip_pool += bet_amount
    else:
        chip_pool -= bet_amount
# ALL OF THESE NOW R FUNCTIONS
# make the process of dealing cards to player/computer
# this function will deal out cards each new game DONT GET CONFUSED WITH CARD.DEAL

def deal_cards():
    global deck, player_hand, dealer_hand, playing, chip_pool, bet_amount

    # shared: deck of cards, value of cards
    # developer view: each hand
    deck = Deck()
    deck.shuffle()
    # sets up a bet
    make_bet()
    # set up both the player and dealer hand
    player_hand = Hand()
    dealer_hand = Hand()
    # deal out initial hand to both dealer and player
    player_hand.card_add(deck.deal())
    player_hand.card_add(deck.deal())

    dealer_hand.card_add(deck.deal())
    dealer_hand.card_add(deck.deal())
    # result = input("Would you like to hit or stand? Press h for hit, s for stand ")
    playing = True
    game_step()

def hit():
    global deck, player_hand, playing, chip_pool, bet_amount
    if player_hand.calc_val() < 21:
        player_hand.card_add(deck.deal())
    else:
        print("Sorry, cannot hit :(")
    if player_hand.calc_val() > 21:
        print("Busted!")
        playing = False
        remaining_amount(False)
        # game_exit()

    game_step()

def stand():
    global deck, player_hand, dealer_hand, playing, chip_pool, bet_amount
    # dealer hit or stand
    if playing == True:
        while(dealer_hand.calc_val() < 19):
            dealer_hand.card_add(deck.deal())
        print("Dealer's hand is: "), dealer_hand.draw(hidden=False)
        print("The dealer's hand total is: " + str(dealer_hand.calc_val()))
        if dealer_hand.calc_val() > 21:
            print("Dealer busted! You win!")
            remaining_amount(True)
        elif player_hand.calc_val() > dealer_hand.calc_val():
            print("You beat the dealer. You win!!")
            remaining_amount(True)
        else:
            print("The dealer has won. You have lost :(")
            remaining_amount(False)
    playing = False
    player_input()


def game_step(): # the gamemaster ish, says the things
    global playing
    if playing == False:
        player_input()
    else:
        print("The player's hand is: "), player_hand.draw(hidden=False)
        print("The player's hand total is: " + str(player_hand.calc_val()))
        print(" ")
        print("Dealer's hand is: "), dealer_hand.draw(hidden=True)
        player_input()
# this function will be in charge of processing all player inputs (hit, stand, quit, play again, etc)

def game_exit():
    print("Thanks for playing!")
    exit()

def player_input():
    # receives user input and makes it lowercase
    global playing, chip_pool

    if playing == True:
        plin = input("Would you like to hit, stand, quit, or play again enter h for hit, s for stand, q for quit: ").lower()
    # check if its h or s (hit or stand)
        if plin == "h":
            hit()

        elif plin == "s":
            stand()
        elif plin == "q":
            game_exit()
        else:
            print("Invalid Inputs. Enter h or s")
            player_input()

    else:
        print("Your buy_in amount is now: $", chip_pool)
        if chip_pool == 0:
            game_exit()
        plin = input("Would you like to playing again or quit? p for play again and q for quit.").lower()
        if plin == 'p':
            deal_cards()
        elif plin == 'q':
            game_exit()
        else:
            print("Invalid input. Enter p or q")
            player_input()

# introduction to game
def intro():
    print("Welcome to the game of black jack! Your starting amount, called buy-in amount, is 100 dollars")
    print(" This buy-in amount is what you start with in the beginning of the game. You can bet any amount of money")
    print(" from your buy-in amount and gain double if you win or lose it if you lose. The goal of the game is to get as close to ")
    print(" 21 as possible without going over it. Hit means to draw a new card, Stand means to end your turn and")
    print(" see whether or not you have beat the dealer. The cards are referenced as ex: S5, which is 5 of spades. Ace is 1 or 11.")
intro()
deal_cards()
