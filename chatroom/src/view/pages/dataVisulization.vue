<template>
  <div class="dataPage">
    <div class="search-area">
      <el-button type="info" round @click="clickWordCloud">词云</el-button>
      <el-dialog
        :visible.sync="dialogVisible"
        :title="dialogOptions.title"
        :width="dialogOptions.width"
        :height="dialogOptions.height"
        append-to-body
      >
        <img :src="imageUrl" alt="" style="height: 500px" />
      </el-dialog>
      <el-input
        v-model="serchKeyWord"
        style="max-width: 600px"
        placeholder="请输入查询关键词"
        class="key-word-input"
      >
        <template #prepend>
          <el-select
            multiple
            v-model="selectedCompanyList"
            placeholder="选择公司"
            style="width: 150px"
            collapse-tags
          >
            <el-option
              v-for="company in companies"
              :label="company"
              :value="company"
            ></el-option>
          </el-select>
        </template>
        <template #append>
          <div class="search-button" @click="searchNow">
            <svg
              t="1719170153061"
              class="icon"
              viewBox="0 0 1024 1024"
              version="1.1"
              xmlns="http://www.w3.org/2000/svg"
              p-id="5234"
              width="20"
              height="20"
            >
              <path
                d="M417.383062 781.594111c-62.535265 0-124.161834-16.698311-179.426509-49.300846-81.562621-48.080042-139.525754-125.07053-163.182546-216.743416s-10.1952-187.094142 37.913495-268.656763c48.080042-81.533968 125.07053-139.497101 216.743416-163.153894 91.701538-23.77038 187.094142-10.223852 268.656763 37.884842S737.613434 246.722194 761.270227 338.394057l0 0c23.656793 91.672886 10.1952 187.094142-37.913495 268.629133-48.108694 81.562621-125.099183 139.525754-216.772069 163.182546C477.05 777.816065 447.11727 781.594111 417.383062 781.594111zM418.518932 130.511449c-24.848944 0-49.868781 3.152806-74.547857 9.54233-76.649727 19.766183-141.002384 68.214614-181.187619 136.4016-40.213887 68.186985-51.458999 147.932214-31.69384 224.553289 19.793812 76.649727 68.214614 141.002384 136.4016 181.187619 68.186985 40.212864 147.903561 51.402717 224.553289 31.69384 76.649727-19.793812 141.002384-68.214614 181.216271-136.4016 40.212864-68.158333 51.458999-147.932214 31.665187-224.553289l0 0c-19.766183-76.649727-68.186985-141.002384-136.372947-181.216271C522.317996 144.456043 470.801692 130.511449 418.518932 130.511449z"
                p-id="5235"
                fill="#707070"
              ></path>
              <path
                d="M915.563312 953.295682c-11.161201 0-22.321378-4.260024-30.841426-12.780071l-260.307607-260.421194c-17.039072-17.039072-17.039072-44.672432 0-61.682851 17.039072-17.039072 44.64378-17.039072 61.682851 0l260.307607 260.421194c17.039072 17.039072 17.039072 44.672432 0 61.682851C937.88469 949.035658 926.723489 953.295682 915.563312 953.295682z"
                p-id="5236"
                fill="#707070"
              ></path>
            </svg>
          </div>
        </template>
      </el-input>
    </div>
    <div class="information-area">
      <div v-if="currentData.length === 0" class="no-data">
        <svg
          t="1719173417348"
          class="icon"
          viewBox="0 0 1024 1024"
          version="1.1"
          xmlns="http://www.w3.org/2000/svg"
          p-id="7531"
          width="50"
          height="50"
        >
          <path
            d="M544 0C281.6 0 64 217.6 64 480S281.6 960 544 960 1024 742.4 1024 480 806.4 0 544 0z m0 896C313.6 896 128 710.4 128 480S313.6 64 544 64 960 249.6 960 480 774.4 896 544 896z m-128-512h-128c-19.2 0-32-12.8-32-32s12.8-32 32-32h128c19.2 0 32 12.8 32 32s-12.8 32-32 32z m416-32c0 19.2-12.8 32-32 32h-128c-19.2 0-32-12.8-32-32s12.8-32 32-32h128c19.2 0 32 12.8 32 32z m-128 384c0 19.2-12.8 32-32 32s-32-12.8-32-32c0-51.2-44.8-96-96-96S448 684.8 448 736c0 19.2-12.8 32-32 32s-32-12.8-32-32C384 646.4 454.4 576 544 576s160 70.4 160 160z"
            fill="#dbdbdb"
            p-id="7532"
          ></path>
        </svg>
      </div>
      <p v-for="data in currentData" class="real-data">{{ data[0] }}</p>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { getLLMQuestion } from "@/api/getDataOut";
export default {
  components: {},
  data() {
    return {
      companies: ["阿里", "美团", "腾讯", "华为"],
      currentCompany: "阿里",
      selectedCompanyList: [],
      serchKeyWord: "",
      currentData: [],
      dialogVisible: false,
      dialogOptions: {
        title: "图片预览",
        width: "700px",
        height: "600px",
      },
      imageUrl: "",
    };
  },
  methods: {
    async searchNow() {
      //   this.$message(`搜索${this.selectedCompanyList}公司,${this.serchKeyWord}`);
      let params = {
        company: this.selectedCompanyList,
        keyword: this.serchKeyWord,
      };
      let ret = false;
      try {
        let res = await getLLMQuestion(params);
        console.log(res);
        if (res.questions !== "无") {
          this.currentData = res.questions;
          ret = true;
        } else {
          this.$message("暂时还没有该部分的信息哦");
          this.currentData = [];
        }
      } catch (error) {
        console.error(error);
      }
      return ret;
    },
    renderQues() {},
    clickWordCloud() {
      if (
        this.selectedCompanyList.length == 0 ||
        this.selectedCompanyList.length > 1
      ) {
        this.$message("请选择一个公司");
      } else {
        console.log(this.selectedCompanyList[0]);
        switch (this.selectedCompanyList[0]) {
          case "阿里":
            this.imageUrl = require(`@/assets/img/阿里.png`);
            this.dialogVisible = true;
            break;
          case "美团":
            this.imageUrl = require(`@/assets/img/美团.png`);
            this.dialogVisible = true;
            break;
          case "腾讯":
            this.imageUrl = require(`@/assets/img/腾讯.png`);
            this.dialogVisible = true;
            break;
          case "华为":
            this.imageUrl = require(`@/assets/img/华为.png`);
            this.dialogVisible = true;
            break;
        }
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.dataPage {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 50px;
  .search-area {
    margin-bottom: 25px;
    display: flex;
    flex-direction: row;
    .el-button {
      margin-right: 20px;
    }
  }
  .information-area {
    margin-top: 25px;
    background-color: rgb(50, 54, 68);
    color: #fff;
    border-color: transparent;
    border-radius: 20px;
    width: 1000px;
    padding: 40px;
    margin-bottom: 20px;
    height: 350px;
    overflow-y: auto;
    .no-data {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 300px;
    }
    .real-data {
      line-height: 2em;
    }
  }
}
.show-img {
  height: 70%;
  width: 60%;
}
</style>
