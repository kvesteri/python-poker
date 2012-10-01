class CardCollection(object):
    def __init__(self, cards=[]):
        self.cards = cards

    def __str__(self):
        return ''.join([str(card) for card in self.cards])


class Board(CardCollection):
    pass
