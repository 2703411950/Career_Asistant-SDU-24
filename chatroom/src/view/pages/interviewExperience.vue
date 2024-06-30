<template>
  <div>
    <head>
      <meta name="referrer" content="no-referrer"/>
    </head>
    <div class="company">
      <div class="left">
        <div class="l-head"></div>
        <el-dropdown @command="changeMenu">
          <h1 class="el-dropdown-link">{{ currentMenu }}</h1>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="公司一览"
              >
                <div class="menu-label">公司一览</div>
              </el-dropdown-item
              >
              <el-dropdown-item command="面试经验"
              >
                <div class="menu-label">面试经验</div>
              </el-dropdown-item
              >

            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <div class="selectJob">
          <el-checkbox-group
              v-model="checkList"
              class="class=selectJobList"
              @change="changeJobList"
          >
            <el-checkbox
                v-if="currentMenu === '公司一览'"
                v-for="job in jobList1"
                :label="job"
                :value="job"
                style="display: block"
                class="selectJobItem"
            />
            <el-checkbox
                v-if="currentMenu === '面试经验' || currentMenu === '数据统计'"
                v-for="job in jobList2"
                :label="job"
                :value="job"
                style="display: block"
                class="selectJobItem"
            />
          </el-checkbox-group>
        </div>
      </div>
      <div class="right">
        <div class="r-head">
          <div class="company-list">
            <div
                v-for="company in companies"
                class="company-icon"
                @click="slectedCompany(company)"
            >
              <img
                  :src="require(`@/assets/img/company-icon/${company}.png`)"
                  alt=""
              />
            </div>
          </div>
          <div class="jobInformations">
            <div class="arrow-icon" @click="loadBefor">
              <img :src="require(`@/assets/img/icon/向左.png`)" alt=""/>
            </div>
            <JobInformationCard
                v-if="currentMenu === '公司一览'"
                :jobItem="currentJobInformation"
            ></JobInformationCard>
            <ExpeienceBlog
                v-if="currentMenu === '面试经验'"
                :exp="currentExperienceBlog"
            ></ExpeienceBlog>
            <ExpeienceBlog
                v-if="currentMenu === '数据统计'"
                :exp="currentDataVisualization"
            ></ExpeienceBlog>
            <div class="arrow-icon" @click="loadNext">
              <img :src="require(`@/assets/img/icon/向右.png`)" alt=""/>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ExpeienceBlog from "../../components/ExperienceBlog.vue";
import JobInformationCard from "../../components/JobInformationCard.vue";
import {getCompanyJobInformationWithOfset, getTechnicalQuestion} from "@/api/getDataOut";
import {getExperienceWithOfset} from "@/api/getDataOut";
import {showTechnicalQuestion} from "@/api/getDataOut";
import {ref} from "vue";

export default {
  components: {
    ExpeienceBlog,
    JobInformationCard,
  },
  data() {
    return {
      companies: ["阿里", "美团", "腾讯", "华为"],
      jobList1: ["数据", "算法", "开发", "网络"],
      jobList2: ["前端", "后端"],
      currentCompany: "腾讯",
      currentJob: "算法",
      currentJobInformation: Object,
      currentExperienceBlog: Object,
      offset: ref(0),
      checkList: [],
      currentMenu: "公司一览",
      nextAble: true,
    };
  },
  mounted() {
    this.getCompanyJobInform();
    this.showTechnical();
    // this.getExperience();
  },
  methods: {
    showTechnical() {
      let params = {
        company: this.currentCompany,
      };
      getTechnicalQuestion(params).then((res) => {
        console.log("问题")
        console.log(res)
      });
    },
    async getExperience() {
      let t;
      if (this.checkList.length === 0) {
        t = ["后端", "前端"]
      } else {
        t = this.checkList
      }
      let params = {
        offset: this.offset,
        checkList: t,
        company: this.currentCompany,
      };
      let ret = false;
      console.log(params);
      try {
        let res = await getExperienceWithOfset(params);
        console.log(res);
        if (res.title !== "无") {
          this.currentExperienceBlog = {
            title: res.title.toString(),
            content: res.content.toString()
          };
          ret = true;
          // this.$message("获得面经");
        } else {
          this.$message("暂时还没有该部分的信息哦");
        }
      } catch (error) {
        console.error(error);
      }
      return ret;
    },
    // 获取职位信息的封装函数
    async getCompanyJobInform() {
      let t;
      if (this.checkList.length === 0) {
        t = ["算法", "数据", "开发", "网络"]
      } else {
        t = this.checkList
      }
      let params = {
        offset: this.offset,
        checkList: t,
        company: this.currentCompany,
      };
      let ret = false;
      console.log(params);
      try {
        let res = await getCompanyJobInformationWithOfset(params);
        if (res.job !== "无") {
          this.currentJobInformation = {
            job: res.job.toString(),
            requriement: res.requirement.toString(),
          };
          ret = true;
          // this.$message("获得岗位信息");
        } else {
          this.$message("暂时还没有该部分的信息哦");
        }
      } catch (error) {
        console.error(error);
      }
      return ret;
    },

    // 获取可视化数据的封装函数
    getDataVisualization() {
      this.currentDataVisualization = {
        title: "词云",
        content: "",
      };
    },
    // 公司一览或面试经验或数据可视化
    changeMenu(command) {
      this.currentMenu = command;
      this.offset = 0;
      // this.$message(`你选择了${this.currentMenu}`);
      switch (command) {
        case "公司一览":
          this.currentJob = "算法"
          this.getCompanyJobInform();
          break;
        case "面试经验":
          this.currentJob = "后端"
          this.getExperience();
          break;
        case "数据统计":
          this.getDataVisualization();
          break;
      }
    },
    // 阿里、腾讯、美团、华为
    slectedCompany(company) {
      this.currentCompany = company;
      this.offset = 0;
      // this.$message(`你选择了${this.currentCompany}`);
      switch (this.currentMenu) {
        case "公司一览":
          this.currentJob = "算法"
          this.getCompanyJobInform();
          break;
        case "面试经验":
          this.currentJob = "后端"
          this.getExperience();
          break;
        case "数据统计":
          this.getDataVisualization();
          break;
      }
    },
    // 公司一览或面试经验对应了不同的职位列表
    changeJobList() {
      this.offset = 0;
      // this.$message(`你选择了${this.currentCompany}`);
      switch (this.currentMenu) {
        case "公司一览":
          this.currentJob = "算法"
          this.getCompanyJobInform();
          break;
        case "面试经验":
          this.currentJob = "后端"
          this.getExperience();
          break;
        case "数据统计":
          this.getDataVisualization();
          break;
      }
      // this.$message(`你选择了${this.checkList}`);
    },
    loadBefor() {
      if (this.offset > 0) {
        this.offset = this.offset - 1;
        let ret;
        if (this.currentMenu === "公司一览") {
          ret = this.getCompanyJobInform();
        }
        if (this.currentMenu === "面试经验") {
          ret = this.getExperience();
        }
        if (!ret) {
          this.offset = this.offset + 1;
        }
      } else {
        this.$message(`已经是最前面了噢`);
      }
    },
    loadNext() {
      this.offset = this.offset + 1;
      let ret = true
      if (this.currentMenu === "公司一览") {
        ret = this.getCompanyJobInform();
      }
      if (this.currentMenu === "面试经验") {
        ret = this.getExperience();
      }
      if (!ret) {
        this.offset = this.offset - 1;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.company {
  display: flex;

  .left {
    width: 200px;

    .l-head {
      display: flex;

      .title {
        padding-left: 10px;
        color: #fff;
      }
    }

    .selectJob {
      margin-top: 65px;
      height: 500px;

      .selectJobList {
        display: flex;
        flex-direction: column;
      }
    }
  }

  .right {
    flex: 1;
    padding-right: 30px;

    .company-list {
      margin-left: 100px;
      margin-right: 100px;
      margin-top: 20px;
      width: 800px;
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      align-items: center;
    }

    .company-icon img {
      height: 40px;
    }

    .jobInformations {
      margin-top: 20px;
      display: flex;
      flex-direction: row;

      .arrow-icon {
        display: flex;
        align-items: center;
        padding: 20px;
      }

      .arrow-icon img {
        height: 40px;
      }
    }
  }
}

.el-checkbox {
  color: #fff;
  margin: 20px;
}

.el-dropdown-link {
  cursor: pointer;
  color: #fff;
  display: flex;
  align-items: center;
}

.el-dropdown-menu {
  background-color: rgb(50, 54, 68);
  border-color: transparent;
}

.menu-label {
  color: #8e9083;
}
</style>