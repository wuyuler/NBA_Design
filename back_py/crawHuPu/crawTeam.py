import requests
from lxml import etree
import os
import pypyodbc


conn = pypyodbc.connect(driver='{SQL Server}',server='localhost',database='crawHuPu', uid='sa', pwd='admin1600200010')
cur=conn.cursor()
#球队基本信息
team_baseinfo=[]
s=requests
teamUrl = []
teamname=[]

#获取队伍标志,和各个主页的url
def getTeam():
    global teamUrl,teamname
    url='https://nba.hupu.com/teams'
    response = s.get(url)
    home_content=response.content

    #获取队伍主页网址
    teamUrl=etree.HTML(home_content).xpath("//a[@class='a_teamlink']/@href")
    teamname = etree.HTML(home_content).xpath("//a[@class='a_teamlink']//h2/text()")
    imgUrl=etree.HTML(home_content).xpath("//a[@class='a_teamlink']//img/@src")
    size=len(teamUrl)

    #h获取队伍标志
    for i in range(size):
        img_url=imgUrl[i]
        imageres = s.get(img_url, stream=True)
        image = imageres.content
        workDir = os.getcwd() + "\\"
        with open(workDir + teamname[i]+".png", 'wb') as jpg:  # 以二进制方式写入code.jpg w模式若文件存在,首先要清空
            # with语句不必自己jpg.close()
            jpg.write(image)

    team_chToEng={}
    for i in range(0,len(teamUrl)):
        team_chToEng[teamname[i]]=teamUrl[i][27:]


#球队的基本信息
def getBaseInfo():
    for url2 in teamUrl:
        res=s.get(url2).content
        #队伍简介
        temp_team_baseinfo = {}
        temp_team_baseinfo['t_name']=url2[27:]
        temp_team_baseinfo['intro']=etree.HTML(res).xpath("//div[@class='team_data']/div[@class='content']/div[@class='content_a']/div[@class='txt']/text()")[0].strip()
        temp_team_baseinfo['dateToNBA']=etree.HTML(res).xpath("//div[@class='team_data']//div[@class='font']/p[1]/text()")[0].strip()
        temp_team_baseinfo['home']=etree.HTML(res).xpath("//div[@class='team_data']//div[@class='font']/p[2]/text()")[0].strip()
        temp_team_baseinfo['website']=etree.HTML(res).xpath("//div[@class='team_data']//div[@class='font']/p[3]/a/@href")[0].strip()
        temp_team_baseinfo['coach']=etree.HTML(res).xpath("//div[@class='team_data']//div[@class='font']/p[4]/text()")[0].strip()
        team_baseinfo.append(temp_team_baseinfo)
#插入数据库的队伍的基本信息
def insert_team_base():
    for base in team_baseinfo:
        cur.execute('insert into team_base(t_name,intro,dateToNBA,home,website,coach) values (?,?,?,?,?,?)',
                    (base['t_name'],base['intro'],base['dateToNBA'],base['home'],base['website'],base['coach']))
        cur.commit()

#获取今年球队的比赛数据
def getTeam_data():
    url = 'https://nba.hupu.com/stats/teams'
    response = s.get(url)
    home_content = response.content
    # 获取队伍主页网址
    teamtoulan = etree.HTML(home_content).xpath("//table[@id='data_js_sort']/tbody//td/text()")
    teams=etree.HTML(home_content).xpath("//tbody//td[2]/a/text()")
    teams =[str(t) for t in teams]
    teams_temp={}
    i=0
    while 20+i*19<len(teamtoulan):
        temp1=[]
        for j in range(19):
            temp1.append(teamtoulan[20+i*19+j])
        teams_temp[teams[i+1]]=temp1[1:]
        i=i+1
    print(teams_temp)
    return teams_temp

def insert_team_data():
    teams_data=getTeam_data()
    cur.execute('delete from team_data')
    cur.commit()
    for t_name,t_data in teams_data.items():
        temp=[]
        temp.append(t_name)
        temp.extend(t_data)
        cur.execute('insert into team_data values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', temp)
        cur.commit()

#获取今年各个球队的
def crawGameCondition():
    url = 'https://nba.hupu.com/standings'
    response = s.get(url)
    home_content = response.content
    gameCon = etree.HTML(home_content).xpath("//table[@class='players_table']/tbody//text()")
    del_list = ['\n','东部', '排名', '队名', '胜', '负', '胜率', '胜场差', '主场', '客场', '赛区', '西部', '得分', '失分', '净胜', '连胜/负']
    gameCon = [x for x in gameCon if x not in del_list]
    return gameCon
def insertGameCondition():
    cur.execute('delete from game_conditon')
    cur.commit()
    gameCon=crawGameCondition()
    for i in range(0,len(gameCon),14):
        temp=gameCon[i:i+14]
        cur.execute('insert into game_conditon values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',temp)
        cur.commit()

def crawPlayerData():
    playerdata=[]
    for i in range(1,3):
        url = 'https://nba.hupu.com/stats/players/pts/'+str(i)
        response = s.get(url)
        home_content = response.content
        temp = etree.HTML(home_content).xpath("//table[@class='players_table']/tbody//text()")
        del_list = ['\n','排名', '球员', '球队', '得分', '命中-出手', '命中率', '命中-三分', '三分命中率', '命中-罚球', '罚球命中率', '场次', '上场时间']
        temp = [x for x in temp if x not in del_list]
        playerdata.extend(temp)
    print(playerdata)
    return playerdata
def insertPlayerData():
    cur.execute('delete from PlayerData')
    cur.commit()
    playerdata=crawPlayerData()
    playerdata.insert(361,'_')
    for i in range(0,len(playerdata),12):
        temp=playerdata[i:i+12]
        print(i)
        print(temp)
        cur.execute('insert into PlayerData values (?,?,?,?,?,?,?,?,?,?,?,?)', temp)
        cur.commit()

def updatePlayerData_team():
    s = requests.session()
    url1 = 'https://nba.hupu.com/teams'
    reponse1 = s.get(url1)
    selector1 = etree.HTML(reponse1.content)
    # 每个球队的网址
    URL = selector1.xpath(
        "/html[@class='expanded']/body/div[@class='gamecenter_livestart']/div[@class='gamecenter_content']/div[@class='teamlist_box clearfix']/div[@class='teamlist_box_r']/div[@class='all']/div[@class='team']/a/@href");
    sql = "delete from TeamScore"
    cur.execute(sql)
    conn.commit()
    sql = "delete from Player"
    cur.execute(sql)
    conn.commit()
    for each in URL:
        response = s.get(each)
        selector = etree.HTML(response.content)
        # 球员编号
        number = selector.xpath(
            "/html[@class='expanded']/body/div[@class='gamecenter_livestart']/div[@class='gamecenter_content']/div[@class='gamecenter_content_l']/div[@class='team_list_data']/div[@class='jiben_title_table']/div[@class='a']/div[@class='x_list']/span[@class='c1']/text()")
        # 球员姓名
        name = selector.xpath(
            "/html[@class='expanded']/body/div[@class='gamecenter_livestart']/div[@class='gamecenter_content']/div[@class='gamecenter_content_l']/div[@class='team_list_data']/div[@class='jiben_title_table']/div[@class='a']/div[@class='x_list']/span[@class='c2']/a/@title")
        # 基本信息
        infor = selector.xpath(
            "/html[@class='expanded']/body/div[@class='gamecenter_livestart']/div[@class='gamecenter_content']/div[@class='gamecenter_content_l']/div[@class='team_list_data']/div[@class='jiben_title_table']/div[@class='b']/div[@id='table_post']/div[@class='x_list']/span/text()")
        # 命中率
        hitrate = selector.xpath(
            "/html[@class='expanded']/body/div[@class='gamecenter_livestart']/div[@class='gamecenter_content']/div[@class='gamecenter_content_l']/div[@class='team_list_data']/div[@class='jiben_title_table']/div[@class='b']/div[@id='table_post2']/div[@class='x_list']/span[@class='c5'][7]/text()")
        # 三分命中率
        hitrate3 = selector.xpath(
            "/html[@class='expanded']/body/div[@class='gamecenter_livestart']/div[@class='gamecenter_content']/div[@class='gamecenter_content_l']/div[@class='team_list_data']/div[@class='jiben_title_table']/div[@class='b']/div[@id='table_post2']/div[@class='x_list']/span[@class='c5'][10]/text()")
        # 场均得分
        score = selector.xpath(
            "/html[@class='expanded']/body/div[@class='gamecenter_livestart']/div[@class='gamecenter_content']/div[@class='gamecenter_content_l']/div[@class='team_list_data']/div[@class='jiben_title_table']/div[@class='b']/div[@id='table_post2']/div[@class='x_list']/span[@class='c5'][4]/text()")
        # 助攻
        shelp = selector.xpath(
            "/html[@class='expanded']/body/div[@class='gamecenter_livestart']/div[@class='gamecenter_content']/div[@class='gamecenter_content_l']/div[@class='team_list_data']/div[@class='jiben_title_table']/div[@class='b']/div[@id='table_post2']/div[@class='x_list']/span[@class='c5'][5]/text()")
        # 队名
        team = selector.xpath(
            "/html[@class='expanded']/body/div[@class='gamecenter_livestart']/div[@class='gamecenter_content']/div[@class='gamecenter_content_l']/div[@class='team_data']/h2/span[@class='title-text']/text()")
        # 得分信息
        Score = selector.xpath("//div[@class='border']/span[@class='b']/b/text()")
        team = team[0]
        team = team.split('（')[0]
        sql = "insert into TeamScore values('%s','%s','%s','%s','%s','%s')" % (
        team, float(Score[0]), float(Score[1]), float(Score[2]), float(Score[3]), float(Score[4]))
        cur.execute(sql)
        conn.commit()
        i = 0
        lenth = len(number)
        while i < lenth:
            sql = "insert into Player values('%s','%s','%s','%s',%d,%d,'%s','%s','%s',%f,%f,'%s','%s')" % (
            number[i], name[i], team, infor[0 + i * 6], int(infor[1 + i * 6]), int(infor[2 + i * 6]), infor[3 + i * 6],
            infor[4 + i * 6], infor[5 + i * 6], float(score[i]), float(shelp[i]), hitrate[i], hitrate3[i])
            cur.execute(sql)
            conn.commit()
            i = i + 1
#爬取虎扑热点新闻
def crawNews():
    newsTitle=[]
    newsUrl=[]
    newsContent=[]
    mainurl = 'https://voice.hupu.com/nba'
    response = s.get(mainurl)
    home_content = response.content
    newsUrl = etree.HTML(home_content).xpath("//div[@class='hours24-top']/div[@class='bd']/ul[@class='list']/li/a/@href")
    newsUrl=['https://voice.hupu.com'+x for x in newsUrl]
    newsTitle = etree.HTML(home_content).xpath("//div[@class='hours24-top']/div[@class='bd']/ul[@class='list']/li/a/text()")
    for i in range(len(newsUrl)):
        response = s.get(newsUrl[i])
        home_content = response.content
        temp=[]
        temp.append(newsTitle[i])
        temp_list=etree.HTML(home_content).xpath("//div[@class='artical-main-content']/p//text()")
        content=''
        for i in temp_list:
            content=content+'<br/>'+i
        temp.append(content)
        newsContent.append(temp)
    return newsContent
def insertNews():
    print("wwww")
    newsContent=crawNews()
    cur.execute('delete from News')
    cur.commit()
    playerdata = crawPlayerData()
    for i in newsContent:
        cur.execute('insert into News values (?,?)', i)
        cur.commit()

def updateSchedule():
    cur.execute('delete from Schedule')
    conn.commit()
    s = requests.session()
    url = 'https://nba.hupu.com/schedule'
    response = s.get(url)
    home_content = response.content
    selector = etree.HTML(home_content)
    schedule = selector.xpath("//table[@class='players_table']/tbody/tr/td//text()")
    del_list = ['\n', '客队 vs 主队', '北京时间', '\xa0vs\xa0', '\xa0\xa0\xa0\n', '数据统计', '数据直播', '比赛前瞻']
    schedule = [x for x in schedule if x not in del_list]
    i = 0
    List = []
    while i < len(schedule):
        List = []
        if (schedule[i].find('月') >= 0):
            Stime = schedule[i].split('\xa0\xa0')[0]
            i = i + 1
        List.append((Stime))
        List.append(schedule[i])
        List.append(schedule[i + 1])
        List.append(schedule[i + 2])
        i = i + 3
        cur.execute('insert into Schedule values(?,?,?,?)', List)
        cur.commit()


if __name__ == '__main__':
    getTeam()

    # #更新球队的数据排行
    # insert_team_data()
    # print("success1")
    # #更新当前战况
    # insertGameCondition()
    # print("success2")
    #更新球员当前数据
    # insertPlayerData()
    # print("success3")
    # #更新按球队分类的球员的当前数据
    # updatePlayerData_team()
    # print("success4")
    #更新最新新闻
    insertNews()
    # print("success5")
    # #更新未来比赛安排
    # updateSchedule()
    # print("success6")

