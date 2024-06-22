<template>
  <div>
    <head>
      <meta name="referrer" content="no-referrer" />
    </head>
    <div class="head">
      <!-- <el-menu
        :default-active="activeIndex2"
        class="company-list"
        mode="horizontal"
        background-color="rgb(50, 54, 68)"
        text-color="#fff"
        active-text-color="#ffd04b"
      >
        <el-menu-item v-for="company in companies" index="1">
          <div class="company-icon" @click="slectedCompany(company)">
            <img
              :src="require(`@/assets/img/company-icon/${company}.png`)"
              alt=""
            />
          </div> </el-menu-item
      ></el-menu> -->
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
    </div>
    <div class="main">
      <div class="left">
        <div class="selectJob">
          <el-checkbox-group v-model="checkList" class="class=selectJobList">
            <el-checkbox
              v-for="job in jobList"
              :label="job"
              :value="job"
              style="display: block"
            />
          </el-checkbox-group>
        </div>
      </div>
      <div class="right"></div>
    </div>
  </div>
</template>

<script>
import { getCompanyJobList } from "@/api/getData";
import { ref } from "vue";
export default {
  data() {
    return {
      companies: ["阿里", "美团", "腾讯", "华为"],
      jobList: [],
      currentCompany: "",
      currentJob: "",
      offset: ref(0),
      checkList: [],
    };
  },
  methods: {
    getCompanyJobInform() {
      let params = {
        offset: this.offset,
        job: this.currentJob,
        company: this.currentCompany,
      };
      getCompanyJobList(params).then((res) => {
        this.jobList = res;
        console.log(this.jobList[0].job_name);
      });
    },
    slectedCompany(company) {
      console.log(`你选择了${company}`);
      this.currentCompany = company;
      this.getCompanyJobInform();
    },
  },
};
</script>

<style lang="scss" scoped>
.head {
  display: flex;
  align-items: center;
  justify-content: center;
}

.company-list {
  width: 700px;

  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.company-icon img {
  height: 40px;
}
.selectJobList {
  display: flex;
  flex-direction: column;
}
</style>
