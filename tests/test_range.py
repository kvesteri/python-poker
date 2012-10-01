from pokerbot import Range


class TestRange(object):
    def test_top_5_percent_range_as_string(self):
        range_ = Range.top(0.05)
        assert str(range_) == '77+, AJs+, AKo+'

    def test_top_10_percent_range_as_string(self):
        range_ = Range.top(0.10)
        assert str(range_) == '66+, A8s+, ATo+'

    def test_top_20_percent_range_as_string(self):
        range_ = Range.top(0.20)
        assert str(range_) == '55+, A3s+, K9o+'

    def test_top_30_percent_range_as_string(self):
        range_ = Range.top(0.30)
        assert str(range_) == '44+, J9s+, Q9o+'

    def test_top_40_percent_range_as_string(self):
        range_ = Range.top(0.40)
        assert str(range_) == '33+, T8s+, K4o+'

    def test_top_50_percent_range_as_string(self):
        range_ = Range.top(0.50)
        assert str(range_) == '22+, J5s+, T8o+'

    def test_paired_range_from_string(self):
        range_ = Range.from_str('66+')
        assert str(range_) == '66+'

    def test_suited_range_from_string(self):
        range_ = Range.from_str('79s+')
        assert str(range_) == '97s+'

    def test_supports_length(self):
        range_ = Range.from_str('97s+')
        assert len(range_) == 176

    def test_all_hands(self):
        range_ = Range.top(1)
        assert len(range_) == 1326

    def test_range_of_AA(self):
        range_ = Range.from_str('AA')
        assert len(range_) == 6

    def test_bottom_10_percent_range_as_string(self):
        range_ = Range.bottom(0.1)
        assert str(range_) == '32-42s, 32-82o'


class TestRangeOperators(object):
    def test_substraction(self):
        range_ = Range.from_str('79+')
        sub = range_ - Range.top(0.05)
        assert str(sub) == '22-66, 97-AQo'
