<template>
  <div class="experience">
    <div class="head">
      <div class="title">
        <h1>面试经验</h1>
      </div>
    </div>
    <div class="main">
      <div class="experienceShow">
        <div class="experienceSlect">
          <el-select
            v-model="company"
            clearable
            placeholder="请选择公司"
            @change="getSelectedExperience"
          >
            <el-option
              v-for="company in companies"
              :key="company"
              :label="company"
              :value="company"
            ></el-option>
          </el-select>
          <el-select
            v-model="job"
            clearable
            placeholder="请选择岗位"
            @change="getSelectedExperience"
          >
            <el-option
              v-for="job in jobs"
              :key="job"
              :label="job"
              :value="job"
            ></el-option>
          </el-select>
        </div>
        <div class="experienceInformation">
          <ul
            v-infinite-scroll="loadMoreExperience"
            class="experience-list"
            style="overflow: auto"
            :infinite-scroll-disabled="disabled"
          >
            <ExpeienceBlog
              v-for="exp in experienceList"
              :exp="exp"
            ></ExpeienceBlog>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ExpeienceBlog from "../../components/ExperienceBlog.vue";
import { getExperienceWithOfset } from "@/api/getData";
import { ref } from "vue";
export default {
  components: {
    ExpeienceBlog,
  },
  data() {
    return {
      companies: ["阿里", "美团", "腾讯", "华为"],
      jobs: ["前端", "后端"],
      company: "",
      job: "",
      experienceList: [],
      count: ref(0),
      disabled: false,
    };
  },
  mounted() {
    this.getExperience();
  },
  methods: {
    // 获取面试经验的帖子
    getExperience() {
      let params = {
        ofset: this.count,
        job: this.job,
        company: this.company,
      };
      getExperienceWithOfset(params).then((res) => {
        console.log(res);
        if (res != null) {
          if (this.count == 0) {
            this.experienceList = [res];
          } else {
            this.experienceList.push(res);
          }
        } else {
          this.$message("暂时还没有该部分的信息哦");
          this.count = this.count - 1;
          this.disabled = true;
        }
      });
    },
    // 下拉栏触底触发
    loadMoreExperience() {
      console.log(`load experience to ${this.count}`);
      this.count += 1;
      this.getExperience();
    },
    // 选择公司或职位栏发生变化时触发
    getSelectedExperience() {
      this.disabled = false;
      this.count = 0;
      this.getExperience();
    },
  },
};
</script>

<style lang="scss" scoped>
.experience {
  display: flex;
  flex-direction: column;
  color: #fff;
  .head {
    .title {
      padding-left: 10px;
    }
  }
  .main {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    .experienceShow {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      .experienceSlect {
        display: flex;
        justify-content: space-between;
        padding: 20px;
        width: 100%;
      }
      .experienceInformation {
        border-radius: 20px;
        width: 100%;
        margin-top: 20px;
        .experience-list {
          height: 70vh;
          &::-webkit-scrollbar {
            width: 0; /* Safari,Chrome 隐藏滚动条 */
            height: 0; /* Safari,Chrome 隐藏滚动条 */
            display: none; /* 移动端、pad 上Safari，Chrome，隐藏滚动条 */
          }
        }
      }
    }
  }
}

.el-select {
  margin-left: 20px;
  margin-right: 20px;
}

.el-select .el-input {
  background-color: rgb(50, 54, 68);
}
</style>
