import  math


class PopulationPyramid:
    def __init__(self, brackets=None, proportion=None):
        """

        :param brackets: list of tuples for the range of age for each bracket
        :param proportion: list of tuple of female and male proportion of population of a bracket
        """
        if brackets is None and proportion is None:
            # population pyramid of the world in 2016
            self.brackets = [(start, start + 4) for start in range(0, 101, 5)]
            self.proportion = [(4.4, 4.7), (4.2, 4.5), (4.0, 4.3), (3.8, 4.1), (3.9, 4.2), (4.0, 4.2), (3.7, 3.8),
                               (3.3, 3.4), (3.2, 3.3), (3.1, 3.1), (2.8, 2.8), (2.4, 2.3), (2.1, 2.0), (1.6, 1.4),
                               (1.1, 1.0), (0.9, 0.7), (0.6, 0.4), (0.3, 0.2), (0.1, 0.0), (0.0, 0.1), (0.0, 0.0)]

        elif brackets is None or proportion is None:
            raise Exception('bracket and proportion must both be defined or undefined')

        else:
            self.brackets = brackets
            self.proportion = proportion

        if len(self.brackets) != len(self.proportion):
            raise Exception('brackets and proportion must have same length')

        if not math.isclose(sum(t[0] + t[1] for t in self.proportion), 100.0):
            raise Exception('sum of proportion is not 100')


