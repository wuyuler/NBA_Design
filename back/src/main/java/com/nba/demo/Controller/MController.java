package com.nba.demo.Controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.List;
import java.util.Map;

@RestController
public class MController {
    @Resource
    private JdbcTemplate jdbcTemplate;
    @GetMapping(value = "/test")
    public void test(@RequestParam String Vteam,String Hteam){
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
}
