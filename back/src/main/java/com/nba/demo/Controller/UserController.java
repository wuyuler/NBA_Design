package com.nba.demo.Controller;

import com.nba.demo.Service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
public class UserController {
    @Resource
    private JdbcTemplate jdbcTemplate;
    @Autowired
    private UserService userService;

    @PostMapping(value = "/loginin")
    public Map loginin(@RequestParam String username, @RequestParam String password){
        Map map=null;
        map=userService.superUserloginin(username,password);

        return map;//包含联系电话
    }
    @PostMapping(value = "/signin")
    public Map signin( @RequestParam String username, @RequestParam String password, @RequestParam String tele){
        Map map=new HashMap();

        int res=userService.canSign(username);
        switch (res){
            case -2:map.put("info",-2);break;
            case 1:userService.signin(username,password,tele);map.put("info",1);break;
            default:map.put("info","未知错误");
        }
        return map;//包含身份证,联系电话
    }
//    @GetMapping(value = "/test")
//    public List mytest(){
//        List list=jdbcTemplate.queryForList("select * from netuser");
//        return list;
//    }
    @PostMapping(value = "/updateTele")
    public Boolean updateTele(@RequestParam String username,@RequestParam String newTele){
        try {
            jdbcTemplate.update("update _USER set Utel =? where  Uno =?",new Object[]{newTele,username});
            return true;
        }catch (Exception e){
            return false;
        }


    }
}
