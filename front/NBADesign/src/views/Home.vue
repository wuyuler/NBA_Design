<template>
 
<el-row calss="container">
<el-col :span="24" class="header">
  <!-- 设置收起导航栏,logo消失 -->
  <el-col :span="10" class="logo" :class="collapsed?'logo-collapse-width':'logo-width'">{{collapsed?'':sysname}}</el-col >
  <el-col :span="10"><div class="tools" @click.prevent="collapse"><i class="el-icon-arrow-left" ></i></div></el-col>
  <el-col :span="4" class="userinfo">

        <el-dropdown trigger="hover">
					<span class="el-dropdown-link userinfo-inner"> {{sysUserName}}</span>
					<el-dropdown-menu slot="dropdown">
						<!-- <el-dropdown-item v-show="usercondition==1" @click.native="gotoUserInfo">个人信息</el-dropdown-item> -->
						<el-dropdown-item divided @click.native="logout" v-if="usercondition!=0">退出登录</el-dropdown-item>
            <el-dropdown-item v-if="usercondition==0" @click.native="login">进入登录页面</el-dropdown-item>
            <el-dropdown-item  @click.native="dialogFormVisible = true">打开嵌套表单的 Dialog</el-dropdown-item>
            <el-dropdown-item  @click.native="super_dialogFormVisible = true">超级会员注册</el-dropdown-item>
					</el-dropdown-menu>
				</el-dropdown>
       
  </el-col>
</el-col>
<el-col :span="24" class="main">
  <aside :class="collapsed?'menu-collapsed':'menu-expanded'">
				<!--导航菜单-->
				<el-menu :default-active="$route.path" class="el-menu-vertical-demo" @open="handleopen" @close="handleclose" @select="handleselect"
					  router v-show="!collapsed">
					<template v-for="(item,index) in $router.options.routes" v-if="!item.hidden" >
						<el-submenu :index="index+''" v-if="!item.leaf" :key="index">
							<template slot="title"><i :class="item.iconCls"></i>{{item.name}}</template>
							<el-menu-item v-for="child in item.children" :index="child.path" :key="child.path" v-if="!child.hidden">{{child.name}}</el-menu-item>
						</el-submenu>
						<el-menu-item v-if="item.leaf&&item.children.length>0" :index="item.children[0].path" :key="item.children[0].path"><i :class="item.iconCls" ></i>{{item.children[0].name}}</el-menu-item>
					</template>
				</el-menu>
        <!--导航菜单-折叠后-->
				<ul class="el-menu el-menu-vertical-demo collapsed" v-show="collapsed" ref="menuCollapsed">
					<li v-for="(item,index) in $router.options.routes" v-if="!item.hidden" class="el-submenu item" :key="index">
						<template v-if="!item.leaf">
							<div class="el-submenu__title" style="padding-left: 20px;" @mouseover="showMenu(index,true)" @mouseout="showMenu(index,false)"><i :class="item.iconCls"></i></div>
							<ul class="el-menu submenu" :class="'submenu-hook-'+index" @mouseover="showMenu(index,true)" @mouseout="showMenu(index,false)"> 
								<li v-for="child in item.children" v-if="!child.hidden" :key="child.path" class="el-menu-item" style="padding-left: 40px;" :class="$route.path==child.path?'is-active':''" @click="$router.push(child.path)">{{child.name}}</li>
							</ul>
						</template>
						<template v-else>
							<li class="el-submenu">
								<div class="el-submenu__title el-menu-item" style="padding-left: 20px;height: 56px;line-height: 56px;padding: 0 20px;" :class="$route.path==item.children[0].path?'is-active':''" @click="$router.push(item.children[0].path)"><i :class="item.iconCls"></i></div>
							</li>
						</template>
					</li>
				</ul>
			</aside>
  <section class="content-container">
				<div class="grid-content bg-purple-light">
					<!-- <el-col :span="24" class="breadcrumb-container"> -->
						<!-- <strong class="title">{{$route.name}}</strong> -->
						<!-- <el-breadcrumb separator="/" class="breadcrumb-inner">
							<el-breadcrumb-item v-for="item in $route.matched" :key="item.path">
								{{ item.name }}
							</el-breadcrumb-item>
						</el-breadcrumb>
					</el-col> -->
          
					<el-col :span="24" class="content-wrapper">
						<transition name="fade" mode="out-in">
							<router-view></router-view>
						</transition>
					</el-col>
				</div>
			</section>
      <!-- 修改个人信息的表单 -->
<el-dialog title="收货地址" :visible.sync="dialogFormVisible">
  <el-form :model="form">
    <el-form-item label="姓名" :label-width="formLabelWidth">
      <el-input v-model="form.name" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="年龄" :label-width="formLabelWidth">
      <el-input v-model="form.age" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="性别" :label-width="formLabelWidth">
      <el-select v-model="form.gender" placeholder="请选择活动区域">
        <el-option label="男" value="男"></el-option>
        <el-option label="女" value="女"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="支持球队" :label-width="formLabelWidth">
      <el-select v-model="form.support_team" filterable  placeholder="请选择支持球队" >
        <el-option v-for="(value,key) in teamsC_E" :key="key" :label="key" :value="key"></el-option>
      </el-select>
    </el-form-item>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="dialogFormVisible = false">取 消</el-button>
    <el-button type="primary" @click="update_selfData">确 定</el-button>
  </div>
</el-dialog>

<!-- 超级会员 -->
<el-dialog title="添加管理员" :visible.sync="super_dialogFormVisible">
  <el-form :model="super_form">
    <el-form-item label="姓名" :label-width="formLabelWidth">
      <el-input v-model="super_form.name" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="年龄" :label-width="formLabelWidth">
      <el-input v-model="super_form.age" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="性别" :label-width="formLabelWidth">
      <el-select v-model="super_form.gender" placeholder="请选择活动区域">
        <el-option label="男" value="男"></el-option>
        <el-option label="女" value="女"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="支持球队" :label-width="formLabelWidth">
      <el-select v-model="super_form.support_team" filterable  placeholder="请选择支持球队" >
        <el-option v-for="(value,key) in teamsC_E" :key="key" :label="key" :value="key"></el-option>
      </el-select>
    </el-form-item>
    </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="super_dialogFormVisible = false">取 消</el-button>
    <el-button type="primary" @click="update_selfData">确 定</el-button>
  </div>
</el-dialog>
</el-col>



</el-row>
</template>

<script>
import { getTeamValues } from '../request/api';
import { update_info } from '../request/api';
export default {
  name: 'App',
  data() {
    return {
      sysUserName: '未登录',
      sysname:"NBA对战系统",
      collapsed:false,
      usercondition:0,
      // 表单数据
      dialogFormVisible: false,
      //管理员注册
      super_dialogFormVisible:false,
      form: {
          age: '',
          gender:'',
          support_team:'',
          user_id: '',
        },
      super_form: {
          user_id: '',
          upw:'',
        },
        formLabelWidth: '120px',
        teamsC_E:{},
    };
  },
  methods:{
    //提交表单修改
    update_selfData(){
      this.dialogFormVisible = false,
      console.log(this.form),
      update_info(this.form)
    },
    //退出登录
			logout: function () {
				var _this = this;
				this.$confirm('确认退出吗?', '提示', {
					//type: 'warning'
				}).then(() => {
          sessionStorage.removeItem('user');
          sessionStorage.removeItem('userstatus')
					_this.$router.push('/login');
				}).catch(() => {

				});


      },
      gotoUserInfo(){
        this.$router.push('/userinfo')
      },
    handleopen() {
				//console.log('handleopen');
			},
			handleclose() {
				//console.log('handleclose');
      },
      handleselect: function (a, b) {
			},
      collapse:function(){
				this.collapsed=!this.collapsed;
			},
			showMenu(i,status){
				this.$refs.menuCollapsed.getElementsByClassName('submenu-hook-'+i)[0].style.display=status?'block':'none';
      },
      login(){
        this.$router.push({path:'/login'})
      }
      
  },
  created(){
    //获取所有球队名称
    this.teamsC_E=getTeamValues()
    //后去登录用户的权限
      var status=sessionStorage.getItem('userstatus')
      if(status){
        this.usercondition=status
      }
			var user = sessionStorage.getItem('user');
			if (user) {
				user = JSON.parse(user);
				this.sysUserName = user.name || '';
				
      }
      if(this.usercondition==2){
        //this.$router.push({name:'买票',params:{'traininfo':JSON.stringify(Object.assign({}, row))}});
        this.$router.push({name:'个人订单信息'});
      }
  },
  mounted() {
      

		}
 
}
</script>

<style lang="scss" scoped>

.container{
  position: absolute;
  top: 0px;
  bottom: 0px;
  width: 100%;

  }
.header{
    height: 60px;
    line-height: 60px;
    color: #fff;
    background: #20a0ff;
  }
  .userinfo {
				text-align: right;
				padding-right: 35px;
				float: right;	
			}
    .userinfo-inner {
					cursor: pointer;
					color:#fff;
				}
.logo{
    height:60px;
    width:230px;
    font-size: 22px;
    padding-left:20px;
		padding-right:20px;
    border-color: rgba(238,241,146,0.3);
    border-right-width: 1px;
    border-right-style: solid;//定义实线。
  }
.logo-width{
      width:230px;
    }
.logo-collapse-width{
  width:60px
}
.tools{
				padding: 0px 23px;
				width:14px;
				height: 60px;
				line-height: 60px;
				/* 设置鼠标放置时的样式 */
        cursor: pointer;
			}
.userinfo{
  /* 靠右对齐 */
  text-align: right;
  /* 与右边的间隔,但似乎始终有间隔 */
  padding-right: 35px;
  /* 成功与右边不再有间隔 */
  float: right;
}
// .menu-expanded{
//         /* 如果不加,会导致导航栏的宽度不断变化 */
// 				flex:0 0 230px;
// 				/* width: 230px; */
// }

  .menu-expanded {
        flex: 0 0 230px;
        width: 230px;
  }
  //解决收缩复原后无法完全显示
	.el-menu {
			width: 100% !important;
			}
  .el-submenu .el-menu-item {
			min-width: 0px !important;
			}
  .main{
    display: flex;
    position: absolute;
    top: 60px;
    bottom: 0px;
  }
  .content-container {
    flex:1;
    padding: 20px;
  }

  .item{
      position: relative;
    }
  .submenu{
    position:absolute;
    top:0px;
    left:60px;
    z-index:99999;
    height:auto;
    display:none;
  }
  .menu-collapsed{//收起导航栏
          flex:0 0 60px;
          width: 60px;
        }

  .title {
    width: 200px;
    float: left;
    color: #475669;
  }
  .breadcrumb-inner {
    float: right;
  }
    .content-wrapper {
    background-color: #fff;
    box-sizing: border-box;
  }


</style>