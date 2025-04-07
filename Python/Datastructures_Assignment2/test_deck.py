from deck import Deck, Card
import pytest


@pytest.mark.parametrize("rank, suite, expected_error, expected_emsg",
                         [(0, "Hearts", ValueError, "Card must have value 1-13"),
                          (24, "Hearts", ValueError, "Card must have value 1-13"),
                          (1, "Spade", ValueError, "Card must have suite 'Hearts', 'Diamonds', 'Spades' or 'Clubs'"),
                          (13, "hearts", ValueError, "Card must have suite 'Hearts', 'Diamonds', 'Spades' or 'Clubs'")])
def test_card_init(rank, suite, expected_error, expected_emsg):
    """ Testar om vi "raise:ar" ett ValueError om man försöker skapa en instans
    av klassen Card med ogiltiga värden. Vi har också lagt till en kontroll
    för detta i init-metoden för Card.
    Vi vill testa detta så inga ogiltiga kort kan skapas."""
    with pytest.raises(expected_error, match=expected_emsg):
        c = Card(rank, suite)


@pytest.mark.parametrize("rank1, suite1, rank2, suite2, expected",
                          [(1, "Hearts", 1, "Spades", True),
                           (13, "Diamonds", 13, "Hearts", True),
                           (10, "Clubs", 11, "Clubs", False),
                           (5, "Hearts", 5, "Spades", True),
                           (1, "Hearts", 2, "Hearts", False),
                           (13, "Spades", 12, "Spades", False)])
def test_card_eq(rank1, suite1, rank2, suite2, expected):
    """ Testar om två kort med samma värde "rank" jämförs som lika.
    Nödvändigt så vi jämför kort på rätt sätt under vår sortering."""
    assert (Card(rank1, suite1) == Card(rank2, suite2)) == expected


@pytest.mark.parametrize("rank1, suite1, rank2, suite2, expected",
                          [(1, "Hearts", 1, "Spades", False),
                           (13, "Diamonds", 13, "Hearts", False),
                           (10, "Clubs", 11, "Clubs", True),
                           (2, "Hearts", 5, "Spades", True),
                           (1, "Hearts", 2, "Hearts", True),
                           (13, "Spades", 12, "Spades", False)])
def test_card_lt(rank1, suite1, rank2, suite2, expected):
    """ Testar om en instans av klassen Card är "less than" en annan instans av Card.
    Nödvändigt så vi kan jämför kort på rätt sätt under vår sortering."""
    assert (Card(rank1, suite1) < Card(rank2, suite2)) == expected


@pytest.mark.parametrize("rank1, suite1, rank2, suite2, expected",
                          [(1, "Hearts", 1, "Spades", False),
                           (13, "Diamonds", 12, "Hearts", True),
                           (6, "Clubs", 1, "Clubs", True),
                           (5, "Hearts", 5, "Spades", False),
                           (1, "Hearts", 2, "Hearts", False),
                           (1, "Spades", 13, "Spades", False)])
def test_card_gt(rank1, suite1, rank2, suite2, expected):
    """ Testar om en instans av klassen Card är "greater than" en annan instans av Card.
     Nödvändigt så vi kan jämför kort på rätt sätt under vår sortering. """
    assert (Card(rank1, suite1) > Card(rank2, suite2)) == expected


def test_deck_len():
    """ Test för att kolla att längden på kortleken är 52 """
    d = Deck()
    assert len(d) == 52


def test_take():
    """ Test för att kontrollera att take() returnerar översta kortet i leken
    och minskar längden med 1 """
    d = Deck()
    d.shuffle()
    length = len(d)
    while len(d.cards) > 0:
        length -= 1
        top_card = d.cards[len(d)-1]
        assert (d.take() == top_card) and (len(d) == length)


@pytest.mark.parametrize("card",
                         [Card(1, "Hearts"),
                          Card(3, "Spades"),
                          Card(4, "Diamonds"),
                          Card(4, "Clubs")])
def test_put(card):
    """ Test för att kontrollera att put()-metoden lägger ett kort överst i kortleken."""
    d = Deck()
    new_card = card
    d.put(new_card)
    assert d.cards[len(d.cards)-1] == new_card and len(d.cards) == 53


def test_sort():
    """ Test för att kontrollera att korten sorteras med metoden sort() """
    d = Deck()
    d.shuffle()
    d.sort()
    for i in range(0, len(d.cards) - 1):
        assert d.cards[i] < d.cards[i + 1] or d.cards[i] == d.cards[i + 1]


@pytest.mark.parametrize("card_list, card, expected_index",
                         [([Card(1, "Hearts"), Card(3, "Hearts"), Card(7, "Hearts"), Card(10, "Hearts")], Card(6, "Spades"), 2),
                          ([Card(1, "Diamonds"), Card(3, "Spades"), Card(7, "Clubs"), Card(10, "Hearts")], Card(13, "Spades"), 4),
                          ([Card(2, "Hearts"), Card(3, "Diamonds"), Card(3, "Clubs"), Card(7, "Hearts")], Card(3, "Spades"), 3)])
def test_insert(card_list, card, expected_index):
    """ Test som kontrollerar att insert()-metoden placerar ett kort 'card'
    på rätt position i kortleken 'card_list'. Förutsatt att 'card_list' är en sorterad lista.
     Testet ser till så att 'card_list' är fortsatt sorterad när vi returnerar listan """
    inserted_card = Deck.insert(card_list, card)[expected_index]
    assert card.rank == inserted_card.rank and card.suite == inserted_card.suite


if __name__ == '__main__':
    pytest.main()
