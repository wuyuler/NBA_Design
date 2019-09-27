import re
import pyodbc
def change():
    conn = pyodbc.connect(driver='{SQL Server}', host="localhost", user="sa", password="jjh123", database="NBAinfo");
    cursor = conn.cursor();
    sql = "select * from gamehistory";
    cursor.execute(sql);
    number = cursor.fetchall();
    for num in number:
        #需要修改第四个
        guest = str(num[4]).split('-')[0]
        numpattern = re.compile(r'\d+');
        guestscore = numpattern.findall(guest);
        if guestscore[0] == '76':
            try:
                gscore = guestscore[1];
                gname = guest.replace(guestscore[1],"",-1)
            except:
                gscore = guestscore[0];
                gname = guest.replace(guestscore[0], "", -1)
        else:
            gscore = guestscore[0];
            gname = guest.replace(guestscore[0], "", -1)
        home = str(num[4]).split('-')[1];
        homescore = numpattern.findall(home);
        if homescore[0] == '76':
            try:
                hscore = homescore[1];
                hname = home.replace(homescore[1],"",-1)
            except:
                hscore = homescore[0];
                hname = home.replace(homescore[0], "", -1)
        else:
            hscore = homescore[0];
            hname = home.replace(homescore[0], "", -1)
        print(type(num[0]))
        list = num[0]+num[1]+num[2]+num[3]+gscore+gname+hscore+hname+num[5]+num[6]+num[7]+num[8]+num[9]+ num[10]+num[11]+num[12]+num[13]+num[14]+num[15]+num[16]+num[17]+num[18]+num[19]+num[20]+num[21]
        cursor.execute('insert into gamestat VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(num[0],num[1],num[2],num[3],gscore,gname,hscore,hname,num[5],num[6],num[7],num[8],num[9], num[10],num[11],num[12],num[13],num[14],num[15],num[16],num[17],num[18],num[19],num[20],num[21]
) );
        cursor.commit()
change()