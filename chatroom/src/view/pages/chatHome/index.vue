<template>
  <div class="chatHome">
    <div class="chatLeft">
      <div class="title">
        <h1>职跃助手</h1>
      </div>

      <!--      <div class="user-settings">-->
      <!--        <div class="settings-unit">-->
      <!--          <span class="settings-text">选择公司</span>-->
      <!--          <div class="my-selector">-->
      <!--            <el-select v-model="companyValue" placeholder="请选择">-->
      <!--              <el-option-->
      <!--                  v-for="item in companyOptions"-->
      <!--                  :key="item.value"-->
      <!--                  :label="item.label"-->
      <!--                  :value="item.value">-->
      <!--              </el-option>-->
      <!--            </el-select>-->
      <!--          </div>-->
      <!--        </div>-->
      <!--        <div class="settings-unit">-->
      <!--          <span class="settings-text">选择岗位</span>-->
      <!--          <div class="my-selector">-->
      <!--            <el-select v-model="jobValue" placeholder="请选择">-->
      <!--              <el-option-->
      <!--                  v-for="item in jobOptions"-->
      <!--                  :key="item.value"-->
      <!--                  :label="item.label"-->
      <!--                  :value="item.value">-->
      <!--              </el-option>-->
      <!--            </el-select>-->
      <!--          </div>-->
      <!--        </div>-->
      <!--        <div class="settings-unit">-->
      <!--          <span class="settings-text">选择面试类型</span>-->
      <!--          <div class="my-selector">-->
      <!--            <el-select v-model="interviewValue" placeholder="请选择">-->
      <!--              <el-option-->
      <!--                  v-for="item in interviewOptions"-->
      <!--                  :key="item.value"-->
      <!--                  :label="item.label"-->
      <!--                  :value="item.value">-->
      <!--              </el-option>-->
      <!--            </el-select>-->
      <!--          </div>-->
      <!--        </div>-->
      <!--        <div class="settings-unit">-->
      <!--          <span class="settings-text">上传你的简历</span>-->
      <!--          <div class="my-selector">-->
      <!--            <el-upload-->
      <!--                class="upload-demo"-->
      <!--                action="https://jsonplaceholder.typicode.com/posts/"-->
      <!--                :on-preview="handlePreview"-->
      <!--                :on-remove="handleRemove"-->
      <!--                :before-remove="beforeRemove"-->
      <!--                multiple-->
      <!--                :limit="1"-->
      <!--                :on-exceed="handleExceed"-->
      <!--                :file-list="fileList">-->
      <!--              <el-button size="small" type="primary">点击上传</el-button>-->
      <!--              <div slot="tip" class="el-upload__tip">只能上传pdf文件</div>-->
      <!--            </el-upload>-->
      <!--          </div>-->
      <!--        </div>-->
      <!--      </div>-->

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
<!--              <el-upload-->
<!--                  class="upload-demo"-->
<!--                  :before-upload="beforeUpload"-->
<!--                  :before-remove="beforeRemove"-->
<!--                  multiple-->
<!--                  :auto-upload="false"-->
<!--                  :limit="1"-->
<!--                  :on-exceed="handleExceed"-->
<!--                  :file-list="form.fileList"-->
<!--                  @change="handleFileUploadChange"> &lt;!&ndash; 添加 change 事件处理器 &ndash;&gt;-->
<!--                <el-button size="small" type="primary">点击上传</el-button>-->
<!--              </el-upload>-->

            </div>
          </div>
        </el-form-item>
      </el-form>

          <el-button type="primary"style="margin-left: 90px;margin-top: 40px" @click="onSubmit">开始面试</el-button>



    </div>

    <div class="chatRight">
      <div>
        <ChatWindow
            :frinedInfo="chatWindowInfo"
            @personCardSort="personCardSort"
        ></ChatWindow>
      </div>
      <!--      <div class="showIcon">-->
      <!--        <span class="iconfont icon-snapchat"></span>-->
      <!--      </div>-->
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
      pcCurrent: "",
      personList: [],
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
        fileList: [],
      }
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
          if (this.personList[i].id == id) {
            nowPersonInfo = this.personList[i];
            this.personList.splice(i, 1);
            break;
          }
        }
        this.personList.unshift(nowPersonInfo);
      }
    },
    handleFileUploadChange(file, fileList) {
      // 在这里，你可以根据需要处理文件对象或更新 fileList
      // 例如，你可以将新文件添加到 form.fileList 中
      this.form.fileList = fileList; // 直接使用组件提供的 fileList
      // 或者你可以添加额外的逻辑来检查文件类型等
    },
    beforeUpload(file) {
      this.form.fileList.push(file);
      return false;
    },

    handleExceed(files, fileList) {
      this.$message.warning('当前限制选择 1 个文件');
    },
    beforeRemove(file, fileList) {
      return this.$confirm(`确定移除 ${file.name}？`);
    },
    onSubmit() {
      console.log(this.form.fileList[0])
      try {
        const formData = new FormData();
        formData.append('job', this.form.job);
        formData.append('company', this.form.company);
        formData.append('interview', this.form.interview);

        if (this.form.fileList.length > 0) {
          formData.append('resume', this.form.fileList[0].raw);
        }

        request.post('/submit', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        console.log('Response:', response.data);
      } catch (error) {
        console.error('Error submitting form:', error);
      }

    }
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