from data import Data
import numpy as np
import pandas as pd
import time

''' what to do:
- perhaps efficiency metrics
    - yards per carry
'''

Data = Data()

MIN_GAMES = 30

# =============== POINTS ===============
PASSING_YARDS = 0.04
PASSING_TD = 4
PASSING_INT = -2
RUSHING_YARDS = 0.1
RUSHING_TD = 6
RECEIVING_YARDS = 0.1
RECEIVING_TD = 6


def main():
    players_dict = Data.players()
    fant_df = Data.fantasy_df()

    _check_if_in_fant_df(players_dict, fant_df)

    positions_dict = _get_positions(players_dict, fant_df)

    players_dict, dropped = _drop_no_pos_players(players_dict, positions_dict)

    pos_df = pd.DataFrame.from_dict(positions_dict, orient='index')

    main_df = pd.DataFrame.from_dict(players_dict, orient='index')

    main_df = pd.concat([main_df, pos_df], axis=1)
    main_df.dropna(inplace=True)
    main_df.columns = ['Link', 'Pos']

    qbs = main_df[main_df['Pos'] == 'QB'].index.tolist()
    rbs = main_df[main_df['Pos'] == 'RB'].index.tolist()
    wrs = main_df[main_df['Pos'] == 'WR'].index.tolist()

    # ========== QB ==========
    qb_dfs = []
    tot_qbs = len(qbs)
    i = 0
    for qb in qbs:
        qb_df = get_player_df(qb)
        if len(qb_df) >= MIN_GAMES:
            try:
                final_df = _qb(qb, qb_df)
                time.sleep(2)
                qb_dfs.append(final_df)
            except Exception:
                pass

        i += 1
        print(f'{round(i/tot_qbs, 2)*100}% of QBs complete')

    qb_df = pd.concat(qb_dfs)
    qb_df.to_csv('results/qbs.csv')
    # ========================

    # ========== RB ==========
    rb_dfs = []
    tot_rbs = len(rbs)
    i = 0
    for rb in rbs:
        rb_df = get_player_df(rb)
        if len(rb_df) >= MIN_GAMES:
            try:
                final_df = _rb(rb, rb_df)
                time.sleep(2)
                rb_dfs.append(final_df)
            except Exception:
                pass

        i += 1
        print(f'{round(i/tot_rbs, 2)*100}% of RBs complete')

    rb_df = pd.concat(rb_dfs)
    rb_df.to_csv('results/rbs.csv')
    # ========================

    # ========== WR ==========
    wr_dfs = []
    tot_wrs = len(wrs)
    i = 0
    for wr in wrs:
        wr_df = get_player_df(wr)
        if len(wr_df) >= MIN_GAMES:
            try:
                final_df = _wr(wr, wr_df)
                time.sleep(2)
                wr_dfs.append(final_df)
            except Exception:
                pass

        i += 1
        print(f'{round(i/tot_wrs, 2)*100}% of WRs complete')

    wr_df = pd.concat(wr_dfs)
    wr_df.to_csv('results/wrs.csv')


def _check_if_in_fant_df(players_dict, fant_df):
    for player in players_dict:
        if player not in fant_df['Player'].tolist():
            raise ValueError(f'{player} not in the fantasy df')


def _get_positions(players_dict, fant_df):
    positions_dict = {}
    fant_df['FantPos'] = fant_df['FantPos'].astype(str)

    for player in players_dict:
        player_entry = fant_df.loc[fant_df['Player'] == player]
        pos = player_entry.iloc[0]['FantPos']
        positions_dict[player] = pos.upper()

    return positions_dict


def _drop_no_pos_players(players_dict, positions_dict):
    dropped = []
    for player in players_dict:
        if positions_dict[player] == 'nan':
            dropped.append(player)

    for drop in dropped:
        del players_dict[drop]

    return players_dict, dropped


def _check_if_enough_games(player):
    if len(Data.career_stats(player)) >= MIN_GAMES:
        return True
    else:
        return False


def _drop_few_games_players(players_dict):
    dropped2 = []
    tot = len(players_dict)
    i = 0
    for player in players_dict:
        _good = _check_if_enough_games(player)
        print(f'{player} is {_good}')
        if _good is False:
            dropped2.append(player)

        i += 1
        time.sleep(2)
        print(f'{round(i/tot, 2)*100}% complete!')

    for drop in dropped2:
        del players_dict[drop]

    return players_dict, dropped2


def get_player_df(player):
    return Data.career_stats(player)


def _qb(qb, df):
    df['Yds'] = df['Yds'].astype(float)
    df['TD'] = df['TD'].astype(float)
    df['Yds.2'] = df['Yds.2'].astype(float)
    df['TD.1'] = df['TD.1'].astype(float)
    df['Int'] = df['Int'].astype(float)

    df['FantPts'] = ((df['Yds']*PASSING_YARDS) + (df['TD']*PASSING_TD) +
                     (df['Int']*PASSING_INT) + (df['Yds.2']*RUSHING_YARDS) +
                     (df['TD.1']*RUSHING_TD))

    fant_pts_median = df['FantPts'].median()
    fant_pts_mean = df['FantPts'].mean()
    fant_pts_std = df['FantPts'].std()
    fant_pts_30_percentile = np.percentile(df['FantPts'], 30)
    fant_pts_plus_std = fant_pts_mean + fant_pts_std
    fant_pts_minus_std = fant_pts_mean - fant_pts_std
    fant_pts_skew = fant_pts_median - fant_pts_mean

    data = {'Name': [qb], 'FantPts MEDIAN': [fant_pts_median],
            'FantPts SKEW': [fant_pts_skew],
            'FantPts +SD': [fant_pts_plus_std],
            'FantPts -SD': [fant_pts_minus_std],
            'FantPts 30 Percentile': [fant_pts_30_percentile]}
    final_df = pd.DataFrame.from_dict(data=data)
    final_df.set_index('Name', inplace=True)

    return final_df


def _rb(rb, df):
    df['Yds'] = df['Yds'].astype(float)
    df['TD'] = df['TD'].astype(float)
    df['Yds.1'] = df['Yds.1'].astype(float)
    df['TD.1'] = df['TD.1'].astype(float)

    df['FantPts'] = ((df['Yds']*RUSHING_YARDS) + (df['TD']*RUSHING_TD) +
                     (df['TD.1']*RECEIVING_TD) + (df['Yds.1']*RECEIVING_YARDS))

    fant_pts_median = df['FantPts'].median()
    fant_pts_mean = df['FantPts'].mean()
    fant_pts_std = df['FantPts'].std()
    fant_pts_30_percentile = np.percentile(df['FantPts'], 30)
    fant_pts_plus_std = fant_pts_mean + fant_pts_std
    fant_pts_minus_std = fant_pts_mean - fant_pts_std
    fant_pts_skew = fant_pts_median - fant_pts_mean

    data = {'Name': [rb], 'FantPts MEDIAN': [fant_pts_median],
            'FantPts SKEW': [fant_pts_skew],
            'FantPts +SD': [fant_pts_plus_std],
            'FantPts -SD': [fant_pts_minus_std],
            'FantPts 30 Percentile': [fant_pts_30_percentile]}
    final_df = pd.DataFrame.from_dict(data=data)
    final_df.set_index('Name', inplace=True)

    return final_df


def _wr(wr, df):
    df['Yds'] = df['Yds'].astype(float)
    df['TD'] = df['TD'].astype(float)
    df['Yds.1'] = df['Yds.1'].astype(float)
    df['TD.1'] = df['TD.1'].astype(float)

    df['FantPts'] = ((df['Yds.1']*RUSHING_YARDS) + (df['TD.1']*RUSHING_TD) +
                     (df['TD']*RECEIVING_TD) + (df['Yds']*RECEIVING_YARDS))

    fant_pts_median = df['FantPts'].median()
    fant_pts_mean = df['FantPts'].mean()
    fant_pts_std = df['FantPts'].std()
    fant_pts_30_percentile = np.percentile(df['FantPts'], 30)
    fant_pts_plus_std = fant_pts_mean + fant_pts_std
    fant_pts_minus_std = fant_pts_mean - fant_pts_std
    fant_pts_skew = fant_pts_median - fant_pts_mean

    data = {'Name': [wr], 'FantPts MEDIAN': [fant_pts_median],
            'FantPts SKEW': [fant_pts_skew],
            'FantPts +SD': [fant_pts_plus_std],
            'FantPts -SD': [fant_pts_minus_std],
            'FantPts 30 Percentile': [fant_pts_30_percentile]}
    final_df = pd.DataFrame.from_dict(data=data)
    final_df.set_index('Name', inplace=True)

    return final_df


if __name__ == "__main__":
    main()
