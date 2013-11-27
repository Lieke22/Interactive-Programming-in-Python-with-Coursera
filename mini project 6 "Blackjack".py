# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")

# initialize some useful global variables
in_play = False
outcome = "Hit or stand?"
player_score = 0
dealer_score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# Student should insert code for Hand class here
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):

        result = ""
        for card in self.cards:
            result += " " + card.__str__()

        return "Hand contains" + result

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        contains_ace = False

        for card in self.cards:
            rank = card.get_rank()
            value += VALUES[rank]

            if(rank == 'A'):
                contains_ace = True

        if(value < 11 and contains_ace):
            value += 10

        return value


    def draw(self, canvas, pos):
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += 80



# define deck class
class Deck:
    def __init__(self):
        self.cards = []

        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop(0)

    def __str__(self):
        result = ""
        for card in self.cards:
            result += " " + card.__str__()

        return "Deck contains" + result



#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, deck, dealer_score

    if(in_play == True):
        outcome = "Player lost because of re-deal! New deal?"
        dealer_score += 1
        in_play = False
    else:
        deck = Deck()
        outcome
        # your code goes here
        deck.shuffle()

        player_hand = Hand()
        dealer_hand = Hand()

        player_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())

        dealer_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())

        print "Player: %s" % player_hand
        print "Dealer: %s" % dealer_hand

        in_play = True

def hit():
    #Implement the handler for a "Hit" button. If the value of the
    #hand is less than or equal to 21, clicking this button adds an
    #extra card to player's hand. If the value exceeds 21 after being hit, print "You have busted".
    global outcome, in_play

    if in_play:
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())

        print "Player hand %s" % player_hand

        if player_hand.get_value() > 21:
            outcome = "You have busted. New deal?"
            in_play = False
            print "You have busted"

def stand():
    global outcome, player_score, dealer_score, in_play

    in_play = False

    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.deal_card())

    print "Dealer: %s" % dealer_hand

    if dealer_hand.get_value() > 21:
        outcome = "Dealer busted. Congratulations!"
        print "Dealer is busted. Player wins."
        player_score += 1
    else:
        if dealer_hand.get_value() >= player_hand.get_value() or player_hand.get_value() > 21:
            print "Dealer wins"
            outcome = "Dealer wins. New deal?"
            dealer_score += 1
        else:
            print "Player wins. New deal?"
            outcome = "Player wins"
            player_score += 1


# draw handler
def draw(canvas):
    global outcome, in_play, card_back, card_loc, player_score, dealer_score

    canvas.draw_text("Blackjack", [220, 50], 50 ,"Pink")

    player_hand.draw(canvas, [100, 300])
    dealer_hand.draw(canvas, [100, 150])

    canvas.draw_text(outcome, [10, 100], 30 ,"Pink")

    canvas.draw_text("Dealer: %s" % dealer_score, [10, 150], 20 ,"Black")
    canvas.draw_text("Player: %s" % player_score, [10, 300], 20 ,"Black")

    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (136,199), CARD_BACK_SIZE)

#    card = Card("S", "A")
#    card.draw(canvas, [300, 300])



# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
#use this code in CodeSkulptor.org