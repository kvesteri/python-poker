class Player():
    def __init__(self, name, balance=1000):
        self.name = name
        self.balance = balance

    def bet(self, deal, amount):
        deal.add_action(self, 'bet', amount)

    def call(self, deal):
        deal.add_action(self, 'call')

    def check(self, deal):
        deal.add_action(self, 'check')

    def fold(self, deal):
        deal.add_action(self, 'fold')

    def join_table(self, table, buyin):
        table.players[self.name] = (self, buyin)

    def rebuy(self, table, buyin):
        pass


class RandomAIPlayer(Player):
    pass

