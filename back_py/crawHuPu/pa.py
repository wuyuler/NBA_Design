from lxml import etree
import requests
import re
import pypyodbc

#获取M,O,T表
conn = pypyodbc.connect(driver='{SQL Server}',server='localhost',database='SDM', uid='sa', pwd='1')
cursor=conn.cursor()
s=requests.session()
url='https://www.basketball-reference.com/leagues/NBA_2018.html'
response=s.get(url)
home_content=response.content
home_content=re.sub('<!--', '', str(home_content))
home_content=re.sub('-->', '', str(home_content))
selector=etree.HTML(home_content)
num=selector.xpath("//table[@id='opponent-stats-per_game']/tbody/tr/th//text()")
team_per=selector.xpath("//table[@id='opponent-stats-per_game']/tbody/tr/td//text()")
for each in team_per:
    if each=='*':
        team_per.remove(each)
print(len(team_per))
i=0
while i<30:
    j=0
    List=[]
    List.append(num[i])
    while j<24:
        List.append(team_per[i*24+j])        
        j=j+1
    cursor.execute('insert into Opponent values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',List)
    conn.commit()
    #print(List)
    i=i+1
    print('end')
