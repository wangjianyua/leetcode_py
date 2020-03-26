import abc  # abstract base class
from enum import Enum
from enum import unique
from random import shuffle
from collections import Counter  # Counter is convenient for counting objects (a specialized dictionary)


@unique
class Suit(Enum):
    Spade = 1
    Heart = 2
    Dimond = 3
    Club = 4

    def __str__(self):
        return self.name


@unique
class Number(Enum):
    N2 = 2
    N3 = 3
    N4 = 4
    N5 = 5
    N6 = 6
    N7 = 7
    N8 = 8
    N9 = 9
    N10 = 10
    J = 11
    Q = 12
    K = 13
    Ace = 14

    def __int__(self):
        if self.value <= 10:
            return int(self.value)


class PlayingCard(metaclass=abc.ABCMeta):
    def __init__(self, suit: Suit):
        self.suit = suit

    @abc.abstractmethod
    def get_value(self):
        pass

    """
        Compare the cards with numbers and suit
    """

    def __lt__(self, other):
        if self.get_value() < other.get_value():
            return True
        if self.get_value() > other.get_value():
            return False

        return self.suit < other.suit


class NumberedCard(PlayingCard):

    def __init__(self, value: int, suit: Suit):
        self.value = value
        super().__init__(suit)

    def get_value(self):
        return self.value

    def output(self):
        return self.get_value(), str(self.suit) + str(self.get_value())


class JackCard(PlayingCard):
    def get_value(self):
        return 11

    def output(self):
        return self.get_value(), str(self.suit) + 'J'


class QueenCard(PlayingCard):
    def get_value(self):
        return 12

    def output(self):
        return self.get_value(), str(self.suit) + 'Q'


class KingCard(PlayingCard):
    def get_value(self):
        return 13

    def output(self):
        return self.get_value(), str(self.suit) + 'K'


class AceCard(PlayingCard):
    def get_value(self):
        return 14

    def output(self):
        return self.get_value(), str(self.suit) + 'Ace'


class StandardDeck:
    def __init__(self):
        self.cards = []
        for suit in Suit:
            for value in range(2, 11):
                self.cards.append(NumberedCard(value, suit).output())
            self.cards.append(JackCard(suit).output())
            self.cards.append(QueenCard(suit).output())
            self.cards.append(KingCard(suit).output())
            self.cards.append(AceCard(suit).output())

    def shuffle(self):

        shuffle(self.cards)
        return self.cards

    def top_card(self):
        return self.cards.pop(0)


class TheHand():
    def __init__(self):
        self.hand = []

    def add_new(self, card):
        card.shuffle()
        self.hand.append(card.top_card())
        return self.hand

    def drop_cards(self, ka, index_list):
        ny_ka = []
        for index, element in enumerate(ka.hand):
            if index not in index_list:
                ny_ka.append(element)
        return ny_ka

    def sort(self):
        self.hand.sort()
        return self.hand

    def best_poker_hand(self, cards):
        if check_straight_flush(cards):
            self.type = PokerHand('check_straight_flush')
        elif check_four_of_a_kind(cards):
            self.type = PokerHand('check_four_of_a_kind')
        elif check_full_house(cards):
            self.type = PokerHand('check_full_house')
        elif check_flush(cards):
            self.type = PokerHand('check_flush')
        elif check_straight(cards):
            self.type = PokerHand('check_straight')
        elif check_three_of_a_kind(cards):
            self.type = PokerHand('check_three_of_a_kind')
        elif check_two_pair(cards):
            self.type = PokerHand('check_two_pair')
        elif check_one_pair(cards):
            self.type = PokerHand('check_one_pair')
        elif check_high_card(cards):
            self.type = PokerHand('check_high_card')


class PokerHand:
    dictionary = {'check_straight_flush': 9,
                  'check_four_of_a_kind': 8,
                  'check_full_house': 7,
                  'check_flush': 6,
                  'check_straight': 5,
                  'check_three_of_a_kind': 4,
                  'check_two_pair': 3,
                  'check_one_pair': 2,
                  'check_high_card': 1}

    def __init__(self, type) :#value, suit):
        self.type = type

    def __lt__(self, other):
        """
            Compare the type of of the cards
        """
        return self.dictionary[self.type] < other.dictionary[other.type]


def check_straight_flush(cards):
    """
    Checks for the best straight flush in a list of cards

    :param cards: A list of playing cards.
    :return: None if no straight flush is found, else the value of the top card.
    """

    vals = [(c.give_value(), c.suit) for c in cards]
    for c in reversed(cards):  # Starting point (high card)
        # Check if we have the value - k in the set of cards:
        found_straight = True
        for k in range(1, 5):
            if (c.give_value() - k, c.suit) not in vals:
                found_straight = False
                break
        if found_straight:
            return c.give_value(), c.suit


def check_full_house(cards):
    """
    Checks for the best full house in a list of cards

    :param cards: A list of playing cards
    :return: None if no full house is found, else a tuple of the values of the triple and pair.
    """
    value_count = Counter()
    for c in cards:
        value_count[c.give_value()] += 1
    # Find the card ranks that have at least three of a kind
    threes = [v[0] for v in value_count.items() if v[1] >= 3]
    threes.sort()
    # Find the card ranks that have at least a pair
    twos = [v[0] for v in value_count.items() if v[1] >= 2]
    twos.sort()

    # Threes are dominant in full house, lets check that value first:
    for three in reversed(threes):
        for two in reversed(twos):
            if two != three:
                return three, two


def check_high_card(cards):
    """
        Checks for the highest card in a list of cards

        :param cards: A list of playing cards
        :return: None if no highest card is found, else the value of the card.
    """
    vals = [(c.give_value()) for c in cards] \
           + [(1) for c in cards if c.give_value() == 14]  # Add the aces!
    vals.sort()
    return vals[-1]


def check_two_pair(cards):
    """
        Checks for the best two pairs in a list of cards

        :param cards: A list of playing cards
        :return: None if no two pairs are found, else a tuple of the values of the pairs.
    """
    value_count = Counter()
    for c in cards:
        value_count[c.give_value()] += 1
    # Find the card ranks that have at least one pair
    twos1 = [v[0] for v in value_count.items() if v[1] >= 2]
    twos1.sort()
    # Find the card ranks that have at least another pair
    twos2 = [v[0] for v in value_count.items() if v[1] >= 2]
    twos2.sort()

    # Threes are dominant in full house, lets check that value first:
    for two1 in reversed(twos1):
        for two2 in reversed(twos2):
            if two1 != two2:
                return two1, two2


def check_one_pair(cards):
    """
            Checks for the best one pair in a list of cards

            :param cards: A list of playing cards
            :return: None if no one pair is found, else return True.
    """
    vals = [(c.give_value()) for c in cards] \
           + [(1) for c in cards if c.give_value() == 14]  # Add the aces!
    for c in reversed(cards):  # Starting point (high card)
        counter = 0
        for _ in range(1, 3):
            if c.give_value() in vals:
                counter += 1
                vals.remove(c.give_value())
                if counter == 2:
                    found_two = True
                    return found_two


def check_three_of_a_kind(cards):
    """
            Checks for the best three of a kind in a list of cards

            :param cards: A list of playing cards
            :return: None if no three of a kind is found, else return True
    """
    vals = [c.give_value() for c in cards]
    for c in reversed(cards):  # Starting point (high card)
        counter = 0
        found_three = False
        for _ in range(1, 4):
            if c.give_value() in vals:
                counter += 1
                vals.remove(c.give_value())
                if counter == 3:
                    found_three = True
                    return found_three


def check_four_of_a_kind(cards):
    """
            Checks for the best four of a kind in a list of cards

            :param cards: A list of playing cards
            :return: None if no four of a kind is found, else return True
    """
    vals = [(c.give_value()) for c in cards] \
           + [(1) for c in cards if c.give_value() == 14]  # Add the aces!
    for c in reversed(cards):  # Starting point (high card)
        counter = 0
        found_four = False
        for _ in range(1, 5):
            if c.give_value() in vals:
                counter += 1
                vals.remove(c.give_value())
                if counter == 4:
                    found_four = True
                    return found_four


def check_straight(cards):
    """
            Checks for the best straight in a list of cards

            :param cards: A list of playing cards
            :return: None if no best straight is found, else return the highest value of the card
    """
    vals = [(c.give_value()) for c in cards]
    for c in reversed(cards):  # Starting point (high card)
        # Check if we have the value - k in the set of cards:
        found_straight = True
        for k in range(1, 5):
            if (c.give_value() - k) not in vals:
                found_straight = False
                break
        if found_straight:
            return c.give_value()


def check_flush(cards):
    """
            Checks for the best flush of a kind in a list of cards

            :param cards: A list of playing cards
            :return: None if no flush is found, else return the suit of the flush
    """
    vals = [c.suit for c in cards]

    for suit in vals:
        counter = 0
        # Check if we have the value - k in the set of cards:
        for _ in range(5):
            if suit in vals:
                counter += 1
                vals.remove(suit)
                if counter == 5:
                    return suit


class Card(object):
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

    def give_value(self):
        return self.number


cards = []

for number in Number:
    for suit in Suit:
        cards.append(Card(suit, number.value))

card_case = [Card(Suit.Spade, Number.Ace.value), Card(Suit.Heart, Number.Ace.value),
                   Card(Suit.Dimond, Number.Ace.value),
                   Card(Suit.Club, Number.N2.value), Card(Suit.Spade, Number.N2.value)]
ans = check_two_pair(card_case)
print(ans)

