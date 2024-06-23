<template>
  <div>
    <head>
      <meta name="referrer" content="no-referrer" />
    </head>
    <div class="company">
      <div class="left">
        <div class="l-head"></div>
        <el-dropdown @command="changeMenu">
          <h1 class="el-dropdown-link">{{ currentMenu }}</h1>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="面试经验"
                ><div class="menu-label">面试经验</div></el-dropdown-item
              >
              <el-dropdown-item command="公司一览"
                ><div class="menu-label">公司一览</div></el-dropdown-item
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
              v-if="currentMenu === '面试经验'"
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
              <img :src="require(`@/assets/img/icon/向左.png`)" alt="" />
            </div>
            <JobInformationCard
              v-if="currentMenu === '公司一览'"
              :jobItem="currentJobInformation"
            ></JobInformationCard>
            <ExpeienceBlog
              v-if="currentMenu === '面试经验'"
              :exp="currenrExperienceBlog"
            ></ExpeienceBlog>
            <div class="arrow-icon" @click="loadNext">
              <img :src="require(`@/assets/img/icon/向右.png`)" alt="" />
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
import { getCompanyJobInformationList } from "@/api/getData";
import { getExperienceWithOfset } from "@/api/getData";
import { ref } from "vue";
export default {
  components: {
    ExpeienceBlog,
    JobInformationCard,
  },
  data() {
    return {
      companies: ["阿里", "美团", "腾讯", "华为"],
      jobList1: ["数据", "算法", "开发", "前端", "后端", "网络"],
      jobList2: ["前端", "后端"],
      currentCompany: "",
      currentJob: "",
      currentJobInformation: Object,
      currenrExperienceBlog: Object,
      offset: ref(0),
      checkList: [],
      currentMenu: "面试经验",
    };
  },
  mounted() {
    this.getCompanyJobInform();
    this.getExperience();
  },
  methods: {
    getExperience() {
      let params = {
        offset: this.offset,
        job: this.job,
        company: this.company,
      };
      getExperienceWithOfset(params).then((res) => {
        console.log(res);
        if (res != null) {
          this.currenrExperienceBlog = res;
          this.$message("获得面经");
        } else {
          this.$message("暂时还没有该部分的信息哦");
          this.count = this.count - 1;
          this.disabled = true;
        }
      });
    },
    getCompanyJobInform() {
      let params = {
        offset: this.offset,
        job: this.currentJob,
        company: this.currentCompany,
      };
      let ret = false;
      getCompanyJobInformationWithOfset(params).then((res) => {
        if (res != null) {
          this.currentJobInformation = res;
          this.$message("获得岗位信息");
          ret = true;
        } else {
          this.$message("暂时还没有该部分的信息哦");
        }
      });
      return ret;
    },
    // 公司一览或面试经验
    changeMenu(command) {
      this.currentMenu = command;
      this.$message(`你选择了${this.currentMenu}`);
    },
    // 阿里、腾讯、美团、华为
    slectedCompany(company) {
      this.currentCompany = company;
      this.$message(`你选择了${this.currentCompany}`);
      this.getCompanyJobInform();
    },
    // 公司一览或面试经验对应了不同的职位列表
    changeJobList() {
      this.$message(`你选择了${this.checkList}`);
    },
    loadBefor() {
      this.offset = this.offset - 1;
      ret = this.getCompanyJobInform();
      if (ret == null) {
        this.offset = this.offset + 1;
      }
    },
    loadNext() {
      this.offset = this.offset + 1;
      if (this.currentMenu == "公司一览") {
        ret = this.getCompanyJobInform();
      }
      if (this.currentMenu == "面试经验") {
        ret = this.getExperience();
      }

      if (ret == null) {
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
