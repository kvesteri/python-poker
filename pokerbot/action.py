class Action(object):
    types = ('bet', 'check', 'fold')
    phases = ('pre-flop', 'flop', 'turn', 'river')

    def __init__(self, deal, player, type, amount, phase):
        self.deal = deal
        self.player = player
        self.type = type
        self.amount = amount
        self.phase = phase
