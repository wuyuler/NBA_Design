import pyodbc
import requests
from lxml import etree
class mysql:
    def __init__(self,host,user,pwd,db):
        self.host = "localhost";
        self.user = "sa";
        self.pwd = "jjh123";
        self.db = "NBAinfo";
    def GetConnect(self):
        if not self.db:
            raise (NameError,"noinfo");
        self.conn = pyodbc.connect(host = self.host,user = self.user,password = self.pwd,database = self.db);
        cur = self.conn.cursor;
        if not cur:
            raise(NameError,"失败连接");
        else:
            print("创建成功")
            return cur
    def ExecNonQuery(self,sql):
        cur = self.GetConnect();
        cur.execute(sql);
        self.conn.commit();
        self.conn.close();
def getteamname(): #球队信息
    r = requests.get('http://www.nba.com/teams');
    team = etree.HTML(r.text).xpath("//div[@class='team__list']/a/text()")
    return team
def eachsite(teamlist):
    for team in teamlist:
        teamname = team.split()[-1]
        r = requests.get("http://nba.hupu.com/teams/"+teamname);
        info = etree.HTML(r.text).xpath("//span[@class='b']/b/text()"); #场均数据
        print(info)
def gameinarow():
    r = requests.get("https://nba.hupu.com/standings")
    i = 3
    conn = pyodbc.connect(driver='{SQL Server}',host="localhost", user="sa", password="jjh123", database="NBAinfo");
    cursor = conn.cursor();
    while i<35:
        teamname = etree.HTML(r.text).xpath("//tr["+str(i)+"]/td[@class='left']/a/text()")
        status = etree.HTML(r.text).xpath("//tr["+str(i)+"]/td[14]/text()");
        temp = str(status[0]);
        if temp[-1] ==  '败':
            type = int(temp[0]) * -1;
        else:
            type = int(temp[0]) * 1;
        cursor.execute('insert into wlrow VALUES(?,?)', (str(teamname[0]), str(type)));
        cursor.commit();
        print(teamname,status)
        if i != 17:
            i = i+1;
        else:
            i = i+3;

gameinarow()