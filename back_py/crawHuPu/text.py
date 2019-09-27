import requests
import pyodbc
from lxml import etree
def winlose():
    namelist=['ATL','SAS','DAL','MEM','NOP','GSW','LAC','SAC','PHO','LAL','OKC','POR','UTA','DEN','MIN',
              'TOR','BOS','NYK','BKN','PHI','MIA','HOU','CHA','WAS','ORL','CLE','IND','DET','CHI','MIL'];
    for name in namelist:
        r = requests.get("http://www.stat-nba.com/query_team.php?crtcol=date_out&order=0&QueryType=game&GameType=season&Team_id="+name+"&PageNum=1000&Season0=2016&Season1=2017");
        r.encoding = 'utf-8'
        i = 0;
        while i< 83:
            team = etree.HTML(r.text).xpath("//tbody/tr["+str(i+1)+"]/td[@class='normal tm_out change_color col1 row"+str(i)+"']/a/text()")
            if len(team) == 0:
                break
            date = etree.HTML(r.text).xpath("//td[@class='current date_out change_color col2 row"+str(i)+"']/text()");
            result = etree.HTML(r.text).xpath("//td[@class='normal wl change_color col3 row"+str(i)+"']/text()");
            homeorguest = etree.HTML(r.text).xpath("//td[@class='normal ha change_color col4 row"+str(i)+"']/text()");
            score = etree.HTML(r.text).xpath("////td[@class='normal result_out change_color col5 row" + str(i) + "']/a/text()");
            swishpercent = etree.HTML(r.text).xpath("//td[@class='normal fgper change_color col6 row"+str(i)+"']/text()")
            swish = etree.HTML(r.text).xpath("//td[@class='normal fg change_color col7 row"+str(i)+"']/text()")
            shoot = etree.HTML(r.text).xpath("//td[@class='normal fga change_color col8 row"+str(i)+"']/text()");
            tpoint= etree.HTML(r.text).xpath("//td[@class='normal threepper change_color col9 row"+str(i)+"']/text()");
            triswish= etree.HTML(r.text).xpath("//td[@class='normal threep change_color col10 row"+str(i)+"']/text()")
            trishoot= etree.HTML(r.text).xpath("//td[@class='normal threepa change_color col11 row"+str(i)+"']/text()");
            filedgoalpercent = etree.HTML(r.text).xpath("//td[@class='normal ftper change_color col12 row"+str(i)+"']/text()")
            filedgoalswish = etree.HTML(r.text).xpath("//td[@class='normal ft change_color col13 row" + str(i) + "']/text()")
            filedgoalshoot = etree.HTML(r.text).xpath("//td[@class='normal fta change_color col14 row" + str(i) + "']/text()")
            bound= etree.HTML(r.text).xpath("//td[@class='normal trb change_color col15 row"+str(i)+"']/text()");
            frebound= etree.HTML(r.text).xpath("//td[@class='normal orb change_color col16 row"+str(i)+"']/text()");
            postbound= etree.HTML(r.text).xpath("//td[@class='normal drb change_color col17 row"+str(i)+"']/text()");
            assit= etree.HTML(r.text).xpath("//td[@class='normal ast change_color col18 row"+str(i)+"']/text()");
            steal= etree.HTML(r.text).xpath("//td[@class='normal stl change_color col19 row"+str(i)+"']/text()");
            block= etree.HTML(r.text).xpath("//td[@class='normal blk change_color col20 row"+str(i)+"']/text()");
            turnover= etree.HTML(r.text).xpath("//td[@class='normal tov change_color col21 row"+str(i)+"']/text()");
            foul= etree.HTML(r.text).xpath("//td[@class='normal pf change_color col22 row"+str(i)+"']/text()");
            list = (str(team[0]),str(date[0]),str(result[0]),str(homeorguest[0]),str(score[0]),str(swishpercent[0]),str(swish[0]),
                    str(shoot[0]),str(tpoint[0]),str(triswish[0]),str(trishoot[0]),str(filedgoalpercent[0]),str(filedgoalswish[0]),
                    str(filedgoalshoot[0]),str(bound[0]),str(frebound[0]),str(postbound[0]),str(assit[0]),str(steal[0]),str(block[0]),
                    str(turnover[0]),str(foul[0]))
            conn = pyodbc.connect(driver='{SQL Server}', host="localhost", user="sa", password="jjh123",
                                  database="NBAinfo");
            cursor = conn.cursor();
            cursor.execute('insert into gamehistory VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',list);
            cursor.commit();
            i = i+1;
            print(list)
def test():
    r = requests.get("http://www.stat-nba.com/query_team.php?crtcol=date_out&order=0&QueryType=game&GameType=season&Team_id=LAL&PageNum=1000&Season0=2018&Season1=2019")
    r.encoding = 'utf-8'
    print(r.text)
    teamname = etree.HTML(r.text).xpath("//tbody/tr[1]/td[@class='normal tm_out change_color col1 row0']/a/text()");
    print(teamname)
winlose()