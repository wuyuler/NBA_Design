import pandas as pd
import math
import csv
import random
import numpy as np
from sklearn import linear_model
from sklearn.model_selection import cross_val_score
from sklearn.externals import joblib
import sys
import pypyodbc

# 当每支队伍没有elo等级分时，赋予其基础elo等级分
base_elo = 1600
team_elos = {}
team_stats = {}
X = []
y = []
folder = 'data' #存放数据的目录

team_name={'火箭': 'Houston Rockets', '马刺': 'San Antonio Spurs', '鹈鹕': 'New Orleans Pelicans', '灰熊': 'Memphis Grizzlies', '独行侠': 'Dallas Mavericks',
										'勇士': 'Golden State Warriors', '快船': 'Los Angeles Clippers', '湖人': 'Los Angeles Lakers', '国王': 'Sacramento Kings', '太阳': 'Phoenix Suns',
										'掘金': 'Denver Nuggets', '雷霆': 'Oklahoma City Thunder', '开拓者': 'Portland Trail Blazers', '爵士': 'Utah Jazz', '森林狼': 'Minnesota Timberwolves',
										'猛龙': 'Toronto Raptors', '76人': 'Philadelphia 76ers', '凯尔特人': 'Boston Celtics', '篮网': 'Brooklyn Nets', '尼克斯': 'New York Knicks',
										 '热火': 'Miami Heat', '黄蜂': 'Charlotte Hornets', '魔术': 'Orlando Magic', '奇才': 'Washington Wizards', '老鹰': 'Atlanta Hawks', '雄鹿': 'Milwaukee Bucks',
										  '步行者': 'Indiana Pacers', '活塞': 'Detroit Pistons', '公牛': 'Chicago Bulls', '骑士': 'Cleveland Cavaliers'}
# 根据每支队伍的Miscellaneous Opponent，Team统计数据csv文件进行初始化
def initialize_data(Mstat, Ostat, Tstat):
    #综合数据
    new_Mstat = Mstat.drop(['Rk', 'Arena'], axis=1)
    #每场对手得分等的平均数据
    new_Ostat = Ostat.drop(['Rk', 'G', 'MP'], axis=1) #G 参加的比赛常数,MP 平均比赛时间
    #球队的得分等数据的平均值
    new_Tstat = Tstat.drop(['Rk', 'G', 'MP'], axis=1)

    team_stats1 = pd.merge(new_Mstat, new_Ostat, how='left', on='Team')
    team_stats1 = pd.merge(team_stats1, new_Tstat, how='left', on='Team')
    return team_stats1.set_index('Team', inplace=False, drop=True)

def get_elo(team):
    try:
        return team_elos[team]
    except:
    # 当最初没有elo时，给每个队伍最初赋base_elo
        team_elos[team] = base_elo
        return team_elos[team]

# 计算每个球队的elo值
def calc_elo(win_team, lose_team):
    winner_rank = get_elo(win_team)
    loser_rank = get_elo(lose_team)

    rank_diff = winner_rank - loser_rank
    exp = (rank_diff  * -1) / 400
    odds = 1 / (1 + math.pow(10, exp))
    # 根据rank级别修改K值
    if winner_rank < 2100:
        k = 32
    elif winner_rank >= 2100 and winner_rank < 2400:
        k = 24
    else:
        k = 16

    # 更新 rank 数值
    new_winner_rank = round(winner_rank + (k * (1 - odds)))
    new_loser_rank = round(loser_rank + (k * (0 - odds)))
    return new_winner_rank, new_loser_rank


def  build_dataSet(all_data):
    #print("Building data set..")
    X = []
    for index, row in all_data.iterrows():

        Wteam = row['WTeam']
        Lteam = row['LTeam']

        # 获取最初的elo或是每个队伍最初的elo值
        team1_elo = get_elo(Wteam)
        team2_elo = get_elo(Lteam)

        # 给主场比赛的队伍加上100的elo值
        if row['WLoc'] == 'H':
            team1_elo += 100
        else:
            team2_elo += 100

        # 把elo当为评价每个队伍的第一个特征值
        team1_features = [team1_elo]
        team2_features = [team2_elo]

        # 添加我们从basketball reference.com获得的每个队伍的统计信息
        for key, value in team_stats.loc[Wteam].iteritems():
            team1_features.append(value)
        for key, value in team_stats.loc[Lteam].iteritems():
            team2_features.append(value)

        # 将两支队伍的特征值随机的分配在每场比赛数据的左右两侧
        # 并将对应的0/1赋给y值
        if random.random() > 0.5:
            X.append(team1_features + team2_features)
            y.append(0)
        else:
            X.append(team2_features + team1_features)
            y.append(1)
        # 根据这场比赛的数据更新队伍的elo值
        new_winner_rank, new_loser_rank = calc_elo(Wteam, Lteam)
        team_elos[Wteam] = new_winner_rank
        team_elos[Lteam] = new_loser_rank

    return np.nan_to_num(X), y
def predict_winner(team_1, team_2, model):
    features = []

    # team 1，客场队伍
    features.append(get_elo(team_1))
    for key, value in team_stats.loc[team_1].iteritems():
        features.append(value)

    # team 2，主场队伍
    features.append(get_elo(team_2) + 100)
    for key, value in team_stats.loc[team_2].iteritems():
        features.append(value)

    features = np.nan_to_num(features)
    return model.predict_proba([features])

if __name__ == '__main__':
    Mstat = pd.read_csv(r'F:\Course_project\NBA_Design\back_py\crawHuPu\data\Miscellaneous.csv')
    Ostat = pd.read_csv(r'F:\Course_project\NBA_Design\back_py\crawHuPu\data\Opponent.csv')
    Tstat = pd.read_csv(r'F:\Course_project\NBA_Design\back_py\crawHuPu\data\TeamPer.csv')

    team_stats = initialize_data(Mstat, Ostat, Tstat)
    print(team_stats.loc["Boston Celtics"])
    result_data = pd.read_csv(r'F:\Course_project\NBA_Design\back_py\crawHuPu\data\result.csv')
    X, y = build_dataSet(result_data)

    训练网络模型
    print("Fitting on %d game samples.." % len(X))
    model = linear_model.LogisticRegression()
    # while True:
    #     model.fit(X, y)
    #     # 利用10折交叉验证计算训练正确率
    #     acc=cross_val_score(model, X, y, cv=10, scoring='accuracy', n_jobs=-1).mean()
    #     print(acc)
    #     if acc>0.7:
    #         joblib.dump(model,'rf2.model')
    #         break
    model=joblib.load(r'F:\Course_project\NBA_Design\back_py\crawHuPu\rf.model')

    conn = pypyodbc.connect(driver='{SQL Server}', server='localhost', database='crawHuPu', uid='sa',
                            pwd='admin1600200010')
    cur = conn.cursor()
    for h_team in team_name.values():
        for g_team in team_name.values():
            res = predict_winner(h_team,g_team, model)
            print(res)
            result=[]
            result.append(h_team)
            result.append(g_team)
            result.append(str(round(res[0][0],2)))
            cur.execute('insert into winning_rate values(?,?,?)', result)
            cur.commit()
    #res=predict_winner(sys.argv[1],sys.argv[2],model)
    #res=predict_winner('Houston Rockets','San Antonio Spurs',model)
    #print(round(res[0][0],2))