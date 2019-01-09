package com.nba.demo.Service;

import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.HashMap;
import java.util.Map;

@Service
public class UserService {
    @Resource
    private JdbcTemplate jdbcTemplate;
    //登录
    public Map superUserloginin(String username, String password){
        try {
            Map  temp=jdbcTemplate.queryForMap("select * from _User where Uno = '"+username+"'and Upw='"+password+"'");
            String idcard=(String) temp.get("UUid");
            String tele=(String) temp.get("Utel");
            String truename = (String)temp.get("Uname");
            Map map=new HashMap();
            Map res=new HashMap();
            map.put("idcard",idcard);
            map.put("tele",tele);
            map.put("name",username);
            map.put("truename",truename);
            res.put("data",map);
            res.put("condition",1);
            return res;
        }catch (EmptyResultDataAccessException e){
            Map res=new HashMap();
            res.put("condition",-1);
            return res;
        }


    }

    //判断注册信息的可用性
    public  int  canSign(String username){
        String sql="select count(*) from _User where Uno="+"'"+username+"'";
        int count=jdbcTemplate.queryForObject(sql,Integer.class);
        if(count!=0)return -2;
        return 1;
    }
    //注册
    public void signin(String username,String password,String tele){
        String sql = "insert into _User  values(?,?,?)";
        jdbcTemplate.update(sql,new Object[]{username,password,tele});
    }

}
