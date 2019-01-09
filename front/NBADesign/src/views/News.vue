<template>
    <el-collapse accordion>
        <el-collapse-item v-for="(news,index) in newslist" :key="index"  >
            <template slot="title">
                <i class="iconfont icon-xinwen"></i> <p class="title">{{index+1}}--{{news.title}}</p>
            </template>
           
            <p class="text" v-html="news.content"></p>
        </el-collapse-item>
    </el-collapse>
</template>

<script>
import { requestgetNews } from '../request/api';
export default {
    created(){
        requestgetNews().then(res=>{
            this.newslist=res.data
        })
    },
    data(){
        return{
            newslist:[]

        }
    }
}
</script>

<style>
    .title {
    font-size: 25px;
  }
  .text{
      font-size: 20px;
  }
</style>
