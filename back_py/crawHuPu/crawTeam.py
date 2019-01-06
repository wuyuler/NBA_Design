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
def getTeam():
    global teamUrl,teamname
    url='https://nba.hupu.com/teams'
    response = s.get(url)
    home_content=response.content

    #获取队伍主页网址
    teamUrl=etree.HTML(home_content).xpath("//a[@class='a_teamlink']/@href")
    print(teamUrl)
    teamname = etree.HTML(home_content).xpath("//a[@class='a_teamlink']//h2/text()")
    imgUrl=etree.HTML(home_content).xpath("//a[@class='a_teamlink']//img/@src")
    size=len(teamUrl)

    # #h获取队伍标志
    # for i in range(size):
    #     img_url=imgUrl[i]
    #     imageres = s.get(img_url, stream=True)
    #     image = imageres.content
    #     workDir = os.getcwd() + "\\"
    #     with open(workDir + teamname[i]+".tif", 'wb') as jpg:  # 以二进制方式写入code.jpg w模式若文件存在,首先要清空
    #         # with语句不必自己jpg.close()
    #         jpg.write(image)

    # team_chToEng={}
    # for i in range(0,len(teamUrl)):
    #     team_chToEng[teamname[i]]=teamUrl[i][27:]

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

def insert_team_base():
    for base in team_baseinfo:
        cur.execute('insert into team_base(t_name,intro,dateToNBA,home,website,coach) values (?,?,?,?,?,?)',
                    (base['t_name'],base['intro'],base['dateToNBA'],base['home'],base['website'],base['coach']))
        cur.commit()

def getTeam_data():
    url = 'https://nba.hupu.com/stats/teams'
    response = s.get(url)
    home_content = response.content
    # 获取队伍主页网址
    teamtoulan = etree.HTML(home_content).xpath("//table[@id='data_js_sort']/tbody//td/text()")
    teams=etree.HTML(home_content).xpath("//tbody//td[2]/a/text()")
    print(teamtoulan)
    print(teams)
    teams_temp={}
    for i in range(30):
        temp1=[]
        for j in range(19):
            temp1.append(teamtoulan[20+i*19+j])
        teams_temp[teams[i+1]]=temp1[1:]
    return teams_temp
def insert_team_data():
    teams_data=getTeam_data()
    for i in teamname:
        list = []
        list.append(i)
        for j in teams_data.get(i):
            list.append(j)
        #print(len(list))
        print(type(list))
        cur.execute('insert into team_data values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',list)
        cur.commit()
if __name__ == '__main__':
    getTeam()
    #getBaseInfo()
    #insert_team_base()
    #cur.execute('select * from team_base')
    insert_team_data()

