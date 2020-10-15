from bs4 import BeautifulSoup
import pandas as pd
import requests

THIS_YEAR = "2020"
BASE_URL = "https://www.pro-football-reference.com"


class Data:

    def fant_raw(self, year=THIS_YEAR):
        F = f'https://www.pro-football-reference.com/years/{year}/fantasy.htm'
        r = requests.get(F)
        soup = BeautifulSoup(r.text, 'lxml')

        return soup

    def players(self, year=THIS_YEAR):
        soup = self.fant_raw(year=year)
        # table = soup.find(id="fantasy")

        players = soup.find_all("td", {"data-stat": "player"})

        player_dict = {}

        for player in players:
            name = player.text.strip()
            link = player.find('a')['href']
            player_dict[name] = link

        return player_dict

    def fantasy_df(self, year=THIS_YEAR):
        soup = self.fant_raw(year=year)
        table = soup.find(id="fantasy")

        df = pd.read_html(str(table), header=1)[0]

        return df

    def career_stats(self, player_name, advanced=False):
        player_dict = self.players()

        if player_name in player_dict:
            if advanced is True:
                prof_link = (BASE_URL + player_dict[player_name][:-4] +
                             '/gamelog/advanced')
            else:
                prof_link = (BASE_URL + player_dict[player_name][:-4] +
                             '/gamelog/')
        else:
            print('No player record!')

        df = pd.read_html(prof_link, header=1)[0]
        df = df[df['Age'] != 'Age']
        df.drop(df.tail(1).index, inplace=True)

        return df


# Data = Data()
# print(Data.fantasy_df())
# print(Data.players())
# Data.career_stats('Tom Brady')
