from data import Data
import matplotlib.pyplot as plt
from scipy import stats

Data = Data()


class QB():
    def __init__(self, player):
        self.player = player
        self.career_stats = Data.career_stats(player)

    def career(self):
        print(self.career_stats)

        return self.career_stats

    def yards_per_attempts(self):
        self.career_stats['Yds'] = self.career_stats['Yds'].astype(float)
        self.career_stats['Att'] = self.career_stats['Att'].astype(float)
        self.career_stats['Y/Att'] = (self.career_stats['Yds'] /
                                      self.career_stats['Att'])

        return self.career_stats['Y/Att']

    def normality_test(self, sequence):
        return print(stats.kstest(sequence, 'norm'))

    def graph_stat(self, sequence):
        plt.hist(sequence, bins=20)
        plt.show()


Brady = QB('Tom Brady')
Brady.career()
y_tgt = Brady.yards_per_attempts()
# print(y_tgt)
# Brady.normality_test(y_tgt)
# Brady.graph_stat(y_tgt)
Brady.normality_test(Brady.career_stats['Yds'])
