class And:
    def __init__(self, *matchers):
        self._matchers = matchers

    def test(self, player):
        for matcher in self._matchers:
            if not matcher.test(player):
                return False

        return True


class PlaysIn:
    def __init__(self, team):
        self._team = team

    def test(self, player):
        return player.team == self._team


class HasAtLeast:
    def __init__(self, value, attr):
        self._value = value
        self._attr = attr

    def test(self, player):
        player_value = getattr(player, self._attr)

        return player_value >= self._value


class All:
    def __init__(self):
        pass

    def test(self, player):
        # Always returns True for all players
        return True


class Not:
    def __init__(self, condition):
        self._condition = condition

    def test(self, player):
        # Negation of the condition
        return not self._condition.test(player)


class HasFewerThan:
    def __init__(self, value, attr):
        self._value = value
        self._attr = attr

    def test(self, player):
        # Negation of the HasAtLeast condition
        player_value = getattr(player, self._attr)
        return player_value < self._value
    

class Or:
    def __init__(self, *conditions):
        self._conditions = conditions

    def test(self, player):
        # True if at least one condition is true
        for condition in self._conditions:
            if condition.test(player):
                return True
        return False

class QueryBuilder:
    def __init__(self):
        self._matchers = []

    def build(self):
        return And(*self._matchers)

    def playsIn(self, team):
        self._matchers.append(PlaysIn(team))
        return self

    def hasAtLeast(self, value, attr):
        self._matchers.append(HasAtLeast(value, attr))
        return self

    def hasFewerThan(self, value, attr):
        self._matchers.append(HasFewerThan(value, attr))
        return self

    def orElse(self):
        # Combine the previously added matchers with logical OR
        previous_matchers = self._matchers[:-1]
        last_matcher = self._matchers[-1]
        or_condition = Or(*previous_matchers, last_matcher)
        self._matchers = [or_condition]
        return self

    def oneOf(self, *matchers):
        return Or(*self._matchers)
