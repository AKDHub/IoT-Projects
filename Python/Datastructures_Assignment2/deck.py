import random


class Card:
    def __init__(self, rank: int, suite: str):
        if rank < 1 or rank > 13:
            raise ValueError("Card must have value 1-13")
        self.rank = rank  # 1-13
        if suite not in ['Hearts', 'Diamonds', 'Spades', 'Clubs']:
            raise ValueError("Card must have suite 'Hearts', 'Diamonds', 'Spades' or 'Clubs'")
        self.suite = suite  # Hearts, Diamonds, Spades, Clubs

    def __str__(self):
        """ Make a string from the card's rank and suite. E.g. 5 of Clubs will be '5C'"""
        r = self.rank
        str_r = None

        if r == 1:
            str_r = 'A'
        elif r == 11:
            str_r = 'J'
        elif r == 12:
            str_r = 'Q'
        elif r == 13:
            str_r = 'K'
        else:
            str_r = str(r)

        return f'{str_r}{self.suite[0].upper()}'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        """ Compare if this card and 'other' card has the same rank """
        if not isinstance(other, Card):
            return False
        return self.rank == other.rank

    def __lt__(self, other):
        """ Compare if the rank of this card is lower than 'other' """
        if not isinstance(other, Card):
            return False
        return self.rank < other.rank

    def __gt__(self, other):
        """ Compare if the rank of this card is higher than 'other' """
        return other.rank < self.rank  # Just invert the check


class Deck:
    def __init__(self):
        """ Create a deck of 52 cards """

        self.cards = []

        for suite in ['Hearts', 'Diamonds', 'Spades', 'Clubs']:
            for rank in range(1, 14):
                self.cards.append(Card(rank, suite))

    def __str__(self):
        return str(self.cards)

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    @staticmethod
    def insert(card_list, card):
        """ Inserts a 'card' in the correct spot in the deck 'card_list' """

        if len(card_list) == 0:
            return card_list.append(card)

        for index in range(0, len(card_list)):
            if card_list[index] > card:
                card_list.insert(index, card)
                return card_list
            elif index == len(card_list)-1:
                card_list.append(card)
                return card_list

    def sort(self):
        """ Sort the deck according to card rank. All aces, the all two's, then all threes, ... """

        sorted_deck = []  # Create a temporary deck

        while len(self.cards) > 0:
            # Go through the deck from left to right, insert the deck in the appropriate spot
            self.insert(sorted_deck, self.take())  # Take a card from the old deck, insert it into the new one

        self.cards = sorted_deck  # Replace the old (empty) deck with the new (sorted) one

    def take(self):
        """ Take the top card from the deck """
        return self.cards.pop()

    def put(self, card):
        """ Put a card on top of the deck """
        self.cards.append(card)


if __name__ == '__main__':
    deck = Deck()
    print('Fresh deck:', deck)
    deck.shuffle()
    print('Shuffled deck:', deck)
    deck.sort()
    print('Sorted deck:', deck)
