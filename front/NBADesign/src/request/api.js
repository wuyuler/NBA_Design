import axios from 'axios';
import Vue from 'vue'
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
import qs from 'qs'
Vue.prototype.$axios = axios;
let base = 'http://localhost:8082';

//TODO:校验用户登录信息
export const requestLogin=params=>{ return axios.post(`${base}/loginin`,qs.stringify(params));};
//TODO:校验用户注册信息
export const requestSign=params=>{ return axios.post(`${base}/signin`,qs.stringify(params));};
//get the type of the team
export const get_team_type=params=>{return axios.get(`${base}/get_categories`,{ params: params });}
//查询胜率
export const requestCompare=params=>{ return axios.get(`${base}/compare`,{ params: params });};
//查询球队数据排名
export const requestgetIeam_data=()=>{ return axios.get(`${base}/getTeam_data`);};
//查询当前战绩
export const requestgetGame_conditon=()=>{ return axios.get(`${base}/getGame_conditon`);};
//查询当前球员数据
export const requestgetPlayerData=params=>{ return axios.get(`${base}/getPlayerData`,{ params: params });};
//查询虎扑24小时最热新闻
export const requestgetNews=()=>{ return axios.get(`${base}/getNews`);};
//获取
export const handleUserList=params=>{ return axios.get(`${base}/player`,{ params: params });};

export const baseHandle=params=>{ return axios.get(`${base}/baseinfor`,{ params: params });};

export const scoreHandle=params=>{ return axios.get(`${base}/score`,{ params: params });};
//获取新闻详情
export const getIDnews=params=>{ return axios.get(`${base}/getIDnews/`+params.ID);};
//获取某新闻的所有评论
export const getComment=params=>{ return axios.get(`${base}/getComment/`,{ params: params });};
//上传评论
export const save_comment=params=>{ return axios.get(`${base}/save_comment`,{ params: params });};
//修改信息
export const update_info=params=>{return axios.get(`${base}/                `,{params: params });};



//获取反馈
export const get_feed=()=>{return axios.get(`${base}/get_feed`)}
//将反馈置为已处理
export const handle_log=params=>{return axios.get(`${base}/handle_log`,{ params: params });}

//获取所有队伍中文 英文缩写
export const getTeamValues=()=>{
    return {'火箭': 'rockets', '马刺': 'spurs', '鹈鹕': 'pelicans', '灰熊': 'grizzlies', '独行侠': 'mavericks', 
    '勇士': 'warriors', '快船': 'clippers', '湖人': 'lakers', '国王': 'kings', '太阳': 'suns', 
    '掘金': 'nuggets', '雷霆': 'thunder', '开拓者': 'blazers', '爵士': 'jazz', '森林狼': 'timberwolves', 
    '猛龙': 'raptors', '76人': '76ers', '凯尔特人': 'celtics', '篮网': 'nets', '尼克斯': 'knicks',
     '热火': 'heat', '黄蜂': 'hornets', '魔术': 'magic', '奇才': 'wizards', '老鹰': 'hawks', '雄鹿': 'bucks',
      '步行者': 'pacers', '活塞': 'pistons', '公牛': 'bulls', '骑士': 'cavaliers'}
};

//获取所有队伍信息
export const getTeamValues_all=()=>{
    return {'火箭': 'Houston Rockets', '马刺': 'San Antonio Spurs', '鹈鹕': 'New Orleans Pelicans', '灰熊': 'Memphis Grizzlies', '独行侠': 'Dallas Mavericks', 
    '勇士': 'Golden State Warriors', '快船': 'Los Angeles Clippers', '湖人': 'Los Angeles Lakers', '国王': 'Sacramento Kings', '太阳': 'Phoenix Suns', 
    '掘金': 'Denver Nuggets', '雷霆': 'Oklahoma City Thunder', '开拓者': 'Portland Trail Blazers', '爵士': 'Utah Jazz', '森林狼': 'Minnesota Timberwolves', 
    '猛龙': 'Toronto Raptors', '76人': 'Philadelphia 76ers', '凯尔特人': 'Boston Celtics', '篮网': 'Brooklyn Nets', '尼克斯': 'New York Knicks',
     '热火': 'Miami Heat', '黄蜂': 'Charlotte Hornets', '魔术': 'Orlando Magic', '奇才': 'Washington Wizards', '老鹰': 'Atlanta Hawks', '雄鹿': 'Milwaukee Bucks',
      '步行者': 'Indiana Pacers', '活塞': 'Detroit Pistons', '公牛': 'Chicago Bulls', '骑士': 'Cleveland Cavaliers'}
};