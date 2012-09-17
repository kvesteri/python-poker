from copy import copy
from itertools import combinations
from hand_eval import Two
from .card import Card
from .hand import Hand
from .deck import deck


def hyphen_range(s):
    """ yield each integer from a complex range string like "1-9,12, 15-20,23"

    >>> list(hyphen_range('1-9,12, 15-20,23'))
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 15, 16, 17, 18, 19, 20, 23]

    >>> list(hyphen_range('1-9,12, 15-20,2-3-4'))
    Traceback (most recent call last):
        ...
    ValueError: format error in 2-3-4

    http://code.activestate.com/recipes/577279
    """
    for x in s.split(','):
        elem = x.split('-')
        if len(elem) == 1:  # a number
            yield int(elem[0])
        elif len(elem) == 2:  # a range inclusive
            start, end = map(int, elem)
            for i in xrange(start, end + 1):
                yield i
        else:  # more than one hyphen
            raise ValueError('format error in %s' % x)


def hyphenize(numlist, maxvalue=14):
    """
    Hyphenize given number list

    [1, 2, 3, 6, 7] -> '1-3, 6-7'

    [1, 2, 3, 4, 9, 10, 11, 12, 13, 14] -> '1-4, 10+'
    """
    sublists = []
    last = None
    for value in numlist:
        if last and (last + 1) == value:
            sublists[-1].append(value)
        else:
            sublists.append([value])
        last = value

    def hyphen_sublist(sublist):
        first = Card.RANKS[sublist[0]] * 2
        if len(sublist) >= 2:
            if sublist[-1] == maxvalue:
                return '%s+' % first
            return '%s-%s' % (first, Card.RANKS[sublist[-1]] * 2)
        return first

    return ', '.join(map(hyphen_sublist, sublists))


def score_max_reversed(max_):
    def func(hand):
        percentile = Two.evaluate_percentile(hand)
        if (1 - percentile) <= max_:
            return True
        else:
            return False
    return func


def score_max(max_):
    def func(hand):
        percentile = Two.evaluate_percentile(hand)
        if percentile <= max_:
            return True
        else:
            return False
    return func


def score_min(min_):
    def func(hand):
        percentile = Two.evaluate_percentile(hand)
        if percentile >= min_:
            return True
        else:
            return False
    return func


def pairs_only(hand):
    if hand.is_pair:
        return True
    return False


def suited_only(hand):
    if hand[0].suit == hand[1].suit:
        return True
    return False


def offsuit_only(hand):
    if hand[0].suit != hand[1].suit:
        return True
    return False


def pair_combinations(rank):
    return map(Hand, combinations(
        [Card(rank, 1), Card(rank, 2), Card(rank, 3), Card(rank, 4)], 2
    ))


class Range(object):
    def __init__(self, hands):
        self.hands = set(hands)

    @classmethod
    def top(cls, max_):
        all_hands = combinations(deck, 2)
        # get all two card combinations from the deck
        hands = list(
            filter(score_max_reversed(max_), map(Hand, all_hands))
        )
        return Range(hands)

    @classmethod
    def bottom(cls, max_):
        all_hands = combinations(deck, 2)
        # get all two card combinations from the deck
        hands = list(
            filter(score_max(max_), map(Hand, all_hands))
        )
        return Range(hands)

    @classmethod
    def from_str(cls, range_str):
        all_hands = combinations(deck, 2)
        parts = range_str.split(', ')
        hands = []
        for part in parts:
            if '-' in part:
                pass
            else:
                if 's' in part:
                    hand = Hand(
                        [Card(part[0] + 'c'), Card(part[1] + 'c')]
                    )
                    filter_func = suited_only
                else:
                    hand = Hand(
                        [Card(part[0] + 'c'), Card(part[1] + 'd')]
                    )
                    if hand.is_pair:
                        filter_func = pairs_only
                    else:
                        filter_func = offsuit_only

                if '+' in part:
                    min_ = Two.evaluate_percentile(hand)
                    tmp = filter(score_min(min_), map(Hand, all_hands))
                else:
                    tmp = pair_combinations(hand[0].rank)
                hands.extend(filter(filter_func, tmp))

        return Range(hands)

    def __str__(self):
        hands = copy(self.hands)

        pairs = set()
        suited = set()
        offsuited = set()
        for hand in hands:
            if hand[0].rank == hand[1].rank:
                pairs.add(hand[0].rank)
            else:
                if hand[0].suit == hand[1].suit:
                    suited.add(hand)
                else:
                    offsuited.add(hand)
        pairs = list(pairs)
        pairs.sort()

        parts = []
        if pairs:
            parts.append(hyphenize(pairs))
        if suited:
            min_suited = min(suited)
            max_suited = max(suited)
            if max_suited[0].str_rank == 'A' and max_suited[1].str_rank == 'K':
                parts.append(
                    str(min_suited[0].str_rank) +
                    str(min_suited[1].str_rank) + 's+'
                )
        if offsuited:
            min_offsuited = min(offsuited)
            parts.append(
                str(min_offsuited[0].str_rank) +
                str(min_offsuited[1].str_rank) + 'o+'
            )
        return ', '.join(parts)

    def __len__(self):
        return len(self.hands)

    def __iter__(self):
        for hand in self.hands:
            yield hand

    def exclude(self):
        pass

    def polarize(self, percentage):
        pass
