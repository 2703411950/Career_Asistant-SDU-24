<template>
  <div>
    <head>
      <meta name="referrer" content="no-referrer" />
    </head>
    <div class="company">
      <div class="left">
        <div class="l-head">
          <div class="title">
            <h1>面试经验</h1>
          </div>
        </div>
        <div class="selectJob">
          <el-checkbox-group
            v-model="checkList"
            class="class=selectJobList"
            @change="changeJobList"
          >
            <el-checkbox
              v-for="job in jobList"
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
              :jobItem="currentJobInformation"
            ></JobInformationCard>
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
import { ref } from "vue";
export default {
  components: {
    ExpeienceBlog,
    JobInformationCard,
  },
  data() {
    return {
      companies: ["阿里", "美团", "腾讯", "华为"],
      jobList: ["数据", "算法", "开发", "前端", "后端", "网络"],
      jobInformationList: [],
      currentCompany: "",
      currentJob: "",
      currentJobInformation: Object,
      offset: ref(0),
      checkList: [],
    };
  },
  mounted() {
    this.getCompanyJobInform();
  },
  methods: {
    getCompanyJobInform() {
      let params = {
        offset: this.offset,
        job: this.currentJob,
        company: this.currentCompany,
      };
      let ret = false;
      getCompanyJobInformationList(params).then((res) => {
        if (res != null) {
          this.currentJobInformation = res;
          console.log(this.currentJobInformation.title);
          ret = true;
        } else {
          this.$message("暂时还没有该部分的信息哦");
        }
      });
      return ret;
    },
    slectedCompany(company) {
      console.log(`你选择了${company}`);
      this.currentCompany = company;
      this.getCompanyJobInform();
    },
    changeJobList() {
      console.log(`selected job list:${this.checkList}`);
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
      ret = this.getCompanyJobInform();
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
</style>
