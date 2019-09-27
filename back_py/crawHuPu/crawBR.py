import requests
from lxml import etree
import os
import pypyodbc

import re
conn = pypyodbc.connect(driver='{SQL Server}',server='localhost',database='crawHuPu', uid='sa', pwd='admin1600200010')
cur=conn.cursor()

s=requests
teams=[]
games=[]
def crawdata():
    global teams
    url = 'https://www.basketball-reference.com/leagues/NBA_2018.html#all_team-stats-per_game'
    response = s.get(url)
    home_content = response.content
    home_content=re.sub('<!--', '', str(home_content))
    home_content=re.sub('-->', '', str(home_content))
    # 获取队伍主页网址
    teams = etree.HTML(home_content).xpath('//*[@id="team-stats-per_game"]/tbody//text()')
    teams=list(teams)
    del_list=['\\n','\\n\\n   ','*']
    teams=[x for x in teams if x not in del_list]

def crawGame():
    global games
    year=['2016','2017','2018']
    for y in year:
        url = 'https://www.basketball-reference.com/leagues/NBA_'+y+'_games.html'
        response = s.get(url)
        home_content = response.content
        # 获取队伍主页网址
        t_games = etree.HTML(home_content).xpath("//table[@id='schedule']/tbody//text()")
        del_list = ['\n', '\n\n', 'OT','2OT']
        t_games = [x for x in t_games if x not in del_list]
        print(len(t_games))
        games.extend(t_games)
    #print(len(games))


def parseGame():
    res=[]
    for i in range(int(len(games)/8)):
        temp=games[8*i:8*i+8]
        temp2=[]
        if int(temp[3])>int(temp[5]):
            temp2.append(temp[2])
            temp2.append(temp[4])
            temp2.append('V')
        else:
            temp2.append(temp[4])
            temp2.append(temp[2])
            temp2.append('H')
        res.append(temp2)
    return res
def insertResult():
    res=parseGame()
    for i in res:
        cur.execute('insert into result values (?,?,?)', i)
        cur.commit()
# def output():
#     a=0
#     for i in teams:
#         print(i,end=' ')
#         a=a+1
#         if a%25==0:
#             print('\n')


if __name__ == '__main__':
    # crawdata_17_18()
    # output()
    crawGame()
    insertResult()