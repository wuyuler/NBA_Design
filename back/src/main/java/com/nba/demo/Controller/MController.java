package com.nba.demo.Controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletRequest;
import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.sql.Time;
import java.text.SimpleDateFormat;
import java.util.*;

@RestController
//实现跨域注解
//origin="*"代表所有域名都可访问
//maxAge飞行前响应的缓存持续时间的最大年龄，简单来说就是Cookie的有效期 单位为秒
//若maxAge是负数,则代表为临时Cookie,不会被持久化,Cookie信息保存在浏览器内存中,浏览器关闭Cookie就消失
@CrossOrigin(origins = "*",maxAge = 3600)
public class MController {
    @Resource
    private JdbcTemplate jdbcTemplate;
    @GetMapping(value = "/test")
    public void test(@RequestParam String Vteam,String Hteam){
        File f=new File("..");

        try{
            String[] args1=new String[]{"D:\\Development_tools\\Anaconda\\python", "F:\\Course_project\\NBA_Design\\back_py\\crawHuPu\\prediction.py",Vteam,Hteam};
            Process proc=Runtime.getRuntime().exec(args1);
            BufferedReader in=new BufferedReader(new InputStreamReader(proc.getInputStream()));
            String line=null;
            while ((line = in.readLine()) != null) {
                System.out.println(line);
            }
            in.close();
            proc.waitFor();
        }catch (Exception e){
            e.printStackTrace();
        }

    }
    @GetMapping(value ="/compare")
    public String compare(@RequestParam String Hteam,@RequestParam String Vteam){
        System.out.println("Vteam:"+Vteam+"-"+"Hteam"+Hteam);
        return jdbcTemplate.queryForObject("select rate from winning_rate where home_team = '"+Hteam+"'and guest_team = '"+Vteam+"'",String.class);
    }
    @GetMapping(value = "/getTeam_data")
    public List getIeam_data(){
        return jdbcTemplate.queryForList("select * from team_data order by score desc ");
    }

    @GetMapping(value = "/getGame_conditon")
    public Map<String, List> getGame_conditon(){
        Map condition = new HashMap();
        System.out.println("Success!!!");
        condition.put("east",jdbcTemplate.queryForList("select * from game_conditon where eorw = 'east' order by rank asc"));
        condition.put("west",jdbcTemplate.queryForList("select * from game_conditon where eorw = 'west' order by rank asc")) ;
        return condition;
    }
    @GetMapping(value = "/getPlayerData")
    public List getPlayerData(@RequestParam String playername){
        if (playername.isEmpty())
        return jdbcTemplate.queryForList("select * from PlayerData order by a  ");
        else
            return jdbcTemplate.queryForList("select * from PlayerData where s like ? order by a",new Object[]{"%"+playername+"%"});
    }
    @GetMapping(value = "/getNews")
    public List getNews(){
        return jdbcTemplate.queryForList("select * from News");
    }
    @GetMapping(value = "/getReq")
    public void getReq(HttpServletRequest request){
        System.out.println(request.getSession().getId());
    }
    @GetMapping(value = "/updateTeam_data")
    public String updateTeam_data(){
        try {
            String[] args1=new String[]{"D:\\Development_tools\\Anaconda\\python", "F:\\Course_project\\NBA_Design\\back_py\\crawHuPu\\crawTeam.py"};
            Process proc=Runtime.getRuntime().exec(args1);
            proc.waitFor();
            return "更新成功";
        }catch (Exception e){
            e.printStackTrace();
        }
        return null;
    }
    @GetMapping(value="/player")
    public List<Map<String,Object>> getPlayer(@RequestParam("Names") String name) {
        String sql="select * from Player where team like ?";
        return jdbcTemplate.queryForList(sql,new String[]{"%"+name+"%"});
    }
    @GetMapping(value = "/baseinfor")
    public List<Map<String,Object>> getBase(@RequestParam("Names") String name){
        String sql="select * from team_base where t_name like ?";
        return jdbcTemplate.queryForList(sql,new String[]{"%"+name+"%"});
    }
    @GetMapping(value ="/score")
    public List<Map<String,Object>> getScore(@RequestParam("Names") String name)
    {
        String sql="select * from TeamScore where name like ?";
        return jdbcTemplate.queryForList(sql,new String[]{"%"+name+"%"});
    }

    @GetMapping(value = "/schedule")
    public List<Map<String, Object>> getSchedule()
    {
        String sql="select * from Schedule";
        return jdbcTemplate.queryForList(sql);
    }
    @GetMapping(value = "/get_categories")
    public String get_categories(@RequestParam String teamname){
        teamname = "%"+teamname;
        String type = jdbcTemplate.queryForObject("select categories from categories where team_name like '"+teamname+"'",String.class);
        return type;
    }
    @GetMapping(value = "/get_feed")
    public List get_feed(){
        List feed_data = jdbcTemplate.queryForList("select * from user_log where hasHandled=0 order by log_date");
        return feed_data;
    }
    @GetMapping(value = "/handle_log")
    public void handle_log(@RequestParam Integer log_id){
        jdbcTemplate.update("update user_log set hashandled=1 where log_id=?",log_id);
    }

    @GetMapping(value = "/stat/{teamname1}/vs/{teamname2}/table")
    public List gettable(@PathVariable("teamname1") String teamname1, @PathVariable("teamname2") String teamname2){
        return jdbcTemplate.queryForList("select gamedate,score,rebound,swish,ftshoot,steal\n" +
                "from gamehistory\n" +
                "where (score like '%"+teamname2+"' and score like '"+teamname1+"%') ");

    }
    @GetMapping(value = "/{teamname1}/vs/{teamname2}/eighttimes")
    public Map<String, List<String>> getscore(@PathVariable("teamname1") String teamname1,@PathVariable("teamname2") String teamname2) {
        List temp= jdbcTemplate.queryForList( "select gamedate,homescore,guestscore from gamestat where (guestname = '"+teamname2+"' and homename = '"+teamname1+"') order by cast(gamedate as date) desc limit 8" );
        Map<String,List<String>> datescore = new HashMap<>();
        ArrayList<String> playdate = new ArrayList<>();
        ArrayList<String> homeplayscore = new ArrayList<>();
        ArrayList<String> guestplaysocre = new ArrayList<>();
        for(int i = temp.size() - 1;i>=0;i--) {
            Map maptemp = (Map) temp.get(i);
            String date = String.valueOf(maptemp.get("gamedate"));
            String homescore = String.valueOf(maptemp.get("homescore"));
            String guestscore = String.valueOf(maptemp.get("guestscore"));
            playdate.add(date);
            homeplayscore.add(homescore);
            guestplaysocre.add(guestscore);
        }
        datescore.put("date",playdate);
        datescore.put("home",homeplayscore);
        datescore.put("guest",guestplaysocre);
        System.out.println(datescore);
        return datescore;
    }
    @GetMapping(value = "getComment")
    public List get_comment(@RequestParam String NewsId){
        return jdbcTemplate.queryForList("select * from _comment where news_id = '"+NewsId+"'");
    }
    @GetMapping(value = "/getIDnews/{ID}")
    public Map get_id_news(@PathVariable("ID") String ID){
        return jdbcTemplate.queryForMap("select title, content from news where id = '"+ID+"'");
    }
    @GetMapping(value = "/save_comment")
    public String save_comment(@RequestParam String content, @RequestParam String user_id, @RequestParam String news_id){
        SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");//设置日期格式
        System.out.println(df.format(new Date()));// new Date()为获取当前系统时间
        int n_id = Integer.valueOf(news_id);
        jdbcTemplate.update("insert into _comment(news_id, user_id, content,time) " +
                "values(?,?,?,?)",n_id,user_id,content, df.format(new Date()));
        return "成功";
    }
    @GetMapping(value = "/stat/{team1}/vs/{team2}") //team1对应甲队，team2对应乙队
    public Map<String,ArrayList<String>> getstat(@PathVariable("team1") String team1,@PathVariable("team2") String team2){
        List info = jdbcTemplate.queryForList("select teamname,avg(cast(homescore as INTEGER)) avgpoint, avg (cast (rebound as INTEGER)) avgrebound, avg(cast(swish as INTEGER)) avgswish,avg(cast(triswish as INTEGER)) avgtriswish\n" +
                ", avg(cast(steal as INTEGER)) avgsteal , avg(cast(ftshoot as INTEGER)) avgftshoot from gamestat where (guestname = '"+team2+"' and homename = '"+team1+"') or (homename = '"+team2+"' and guestname = '"+team1+"')\n" +
                " group by teamname");
        Map<String,ArrayList<String>> avginfo = new HashMap<>();
        for(int i = 0;i<info.size();i++){
            Map temp = (Map)info.get(i);
            ArrayList<String> statinfo = new ArrayList<>();
            String teamname = String.valueOf(i);
            String avgpoint =  temp.get("avgpoint").toString();
            statinfo.add(avgpoint);
            String avgrebound = temp.get("avgrebound").toString();
            statinfo.add(avgrebound);
            String avgtri = temp.get("avgtriswish").toString();
            statinfo.add(avgtri);
            String avgswish = temp.get("avgswish").toString();
            statinfo.add(avgswish);
            String avgftshoot = temp.get("avgftshoot").toString();
            statinfo.add(avgftshoot);
            String  avgsteal =  temp.get("avgsteal").toString();
            statinfo.add(avgsteal);
            avginfo.put(teamname,statinfo);
        }
        ArrayList<String> teamlist = new ArrayList<>();
        teamlist.add(team1);
        teamlist.add(team2);
        avginfo.put("2",teamlist);
        System.out.println(avginfo);
        return avginfo;
    }



}
