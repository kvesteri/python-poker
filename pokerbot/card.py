class Card:
    RANKS = {
        2: '2',
        3: '3',
        4: '4',
        5: '5',
        6: '6',
        7: '7',
        8: '8',
        9: '9',
        10: 'T',
        11: 'J',
        12: 'Q',
        13: 'K',
        14: 'A'
    }

    RANKS_REVERSED = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'T': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14
    }

    SUITS = {
        1: 's',
        2: 'h',
        3: 'd',
        4: 'c'
    }

    def __init__(self, rank, suit=None):
        """Create a card. Rank is 2-14, representing 2-A,
        while suit is 1-4 representing spades, hearts, diamonds, clubs"""
        if isinstance(rank, basestring):
            for key, value in self.RANKS.items():
                if value == rank[0]:
                    self.rank = key
            for key, value in self.SUITS.items():
                if value == rank[1]:
                    self.suit = key
        else:
            self.rank = rank
            if suit is None:
                raise Exception()
            self.suit = suit

    @property
    def str_rank(self):
        return self.RANKS[self.rank]

    def __str__(self):
        return "{0}{1}".format(self.RANKS[self.rank], self.SUITS[self.suit])

    def __repr__(self):
        return "{0}({1}, {2})".format(
            self.__class__.__name__,
            self.rank,
            self.suit
        )

    def __eq__(self, other):
        return self.rank == other.rank

    def __gt__(self, other):
        return self.rank > other.rank

    def __hash__(self):
        return hash((self.suit, self.rank))
