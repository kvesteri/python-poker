from .deal import Deal


class Seat(object):
    def __init__(self, table):
        self.table = table


class Table(object):
    def __init__(self, big_blind_size=2):
        self.deals = []
        self.player_dict = {}
        self.balances = {}
        self.seats = []
        self.button_index = -1
        self.big_blind_size = big_blind_size

    def add_player(self, player, buyin):
        self.player_dict[player.name] = player
        self.balances[player.name] = buyin
        self.seats.append(player)

    @property
    def button_player(self):
        """
        Returns the player who is currently on the button
        """
        return self.seats[self.button_index]

    def move_button(self):
        """
        Moves button to the next available seat
        """
        self.button_index += 1
        if self.button_index == len(self.seats):
            self.button_index = 0

    def new_deal(self):
        if not self.player_dict:
            raise Exception("Can't deal new hand. No players at the table")
        if len(self.player_dict.keys()) == 1:
            raise Exception(
                "Can't deal new hand. Only one player present at the table"
            )
        deal = Deal(self)
        self.deals.append(deal)
        self.move_button()
        return deal

    def get_balance(self, player_name):
        return self.balances[player_name]

    def get_player(self, player_name):
        return self.player_dict[player_name]
