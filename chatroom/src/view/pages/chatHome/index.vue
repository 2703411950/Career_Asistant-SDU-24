<template>
  <div v-loading="isLoading" element-loading-text="加载中" element-loading-background="rgba(180, 180, 180, 0.8)"
       class="chatHome">
    <div class="chatLeft">
      <div class="title">
        <h1>职跃助手</h1>
      </div>

      <el-form class="user-settings" ref="form" :model="form" label-width="80px" label-position="top">
        <el-form-item class="settings-unit">
          <span class="settings-text">选择岗位</span>
          <el-select class="my-selector" v-model="form.job" placeholder="请选择岗位">
            <el-option
                v-for="item in jobOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item class="settings-unit">
          <span class="settings-text">选择公司</span>
          <el-select class="my-selector" v-model="form.company" placeholder="请选择公司">
            <el-option
                v-for="item in companyOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item class="settings-unit">
          <span class="settings-text">选择面试类型</span>
          <el-select class="my-selector" v-model="form.interview" placeholder="请选择面试类型">
            <el-option
                v-for="item in interviewOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item class="settings-unit">
          <div class="flex-container">
            <span class="settings-text">上传你的简历</span>
            <div class="my-selector">
              <input type="file" style="color: white" @change="onFileChange"/>
            </div>
          </div>
        </el-form-item>
      </el-form>
      <el-button type="primary" style="margin-left: 90px; margin-top: 40px" @click="onSubmit">开始面试</el-button>


    </div>

    <div class="chatRight">
      <div>
        <ChatWindow
            :frinedInfo="chatWindowInfo"
            :question="question"
            :startInterview="startInterview"
            @personCardSort="personCardSort"
        ></ChatWindow>
      </div>
    </div>
  </div>
</template>

<script>
import PersonCard from "@/components/PersonCard.vue";
import ChatWindow from "./chatwindow.vue";

import {getFriend} from "@/api/getData";
import request from "@/utils/request";

export default {
  name: "App",
  components: {
    PersonCard,
    ChatWindow,
  },
  data() {
    return {
      question: [],
      pcCurrent: "",
      personList: [],
      startInterview: false,
      isLoading: false,
      chatWindowInfo: {},
      companyOptions: [
        {
          value: '华为',
          label: '华为'
        }, {
          value: '阿里',
          label: '阿里'
        }, {
          value: '腾讯',
          label: '腾讯'
        }],
      jobOptions: [
        {
          value: '前端',
          label: '前端'
        }, {
          value: '后端',
          label: '后端'
        }, {
          value: '移动',
          label: '移动'
        }],
      interviewOptions: [
        {
          value: '技术面',
          label: '技术面',
        },
        {
          value: 'HR面',
          label: 'HR面',
        }
      ],
      form: {
        job: '',
        company: '',
        interview: '',
      },
      file: null
    };
  },
  mounted() {
    getFriend().then((res) => {
      console.log(res);
      this.personList = res;
    });
    this.clickPerson({
      img: "",
      name: "机器人1号",
      detail: "我是机器人1号",
      lastMsg: "to do",
      id: "1002",
      headImg: require("@/assets/img/img_2.png"),
    },)
  },
  methods: {

    clickPerson(info) {
      this.chatWindowInfo = info;
      this.personInfo = info;
      this.pcCurrent = info.id;
    },

    personCardSort(id) {
      if (id !== this.personList[0].id) {
        console.log(id);
        let nowPersonInfo;
        for (let i = 0; i < this.personList.length; i++) {
          if (this.personList[i].id === id) {
            nowPersonInfo = this.personList[i];
            this.personList.splice(i, 1);
            break;
          }
        }
        this.personList.unshift(nowPersonInfo);
      }
    },
    onFileChange(e) {
      this.file = e.target.files[0];
      console.log(this.file)
    },
    onSubmit() {
      let formData = new FormData();
      // 添加文本字段
      for (let key in this.form) {
        if (this.form[key] === '') {
          alert("请填写完整信息");
          return;
        }
        formData.append(key, this.form[key]);
      }
      // 添加文件
      console.log(this.file)
      if (this.file) {
        formData.append('file', this.file);
      } else {
        alert("请上传简历文件！");
        return;
      }
      this.isLoading = true;
      // 使用axios或fetch发送POST请求
      // 假设你的Flask后端API地址是 '/upload'
      // delete formData.headers['Content-Type'];
      request.post('/upload_file', formData, {
        headers: {
          // 注意：当使用 FormData 时，不需要手动设置 Content-Type
          // axios 会自动处理
        },
      }).then(response => {
        if (response.code === 200) {
          this.$message("上传成功~🥳");
          console.log(response.result)
          this.question = response.result
          this.startInterview = true
        }
        this.isLoading = false;
      }).catch(error => {
        console.error(error);
        this.isLoading = false;
        // 处理错误
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.chatHome {
  // margin-top: 20px;
  display: flex;

  .chatLeft {
    width: 280px;

    .title {
      color: #fff;
      padding-left: 10px;
    }

    .user-settings {
      margin-top: 20px;

      .settings-unit {
        padding-left: 10px;
        margin-top: 0px;
      }

      .settings-text {
        padding-left: 10px;
        margin-top: 0px;
        color: rgb(176, 178, 189);
      }

      .my-selector {
        padding-left: 10px;
        margin-top: 0px;
      }
    }
  }

  .chatRight {
    flex: 1;
    padding-right: 30px;

    .showIcon {
      position: absolute;
      top: calc(50% - 150px); /*垂直居中 */
      left: calc(50% - 50px); /*水平居中 */
      .icon-snapchat {
        width: 300px;
        height: 300px;
        font-size: 300px;
        // color: rgb(28, 30, 44);
      }
    }
  }
}
</style>