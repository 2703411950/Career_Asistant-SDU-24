<template>
  <el-card>
    <template #header>
      <div class="experience-title">
        <span>{{ exp.title }}</span>
      </div>
    </template>
    <div v-if="exp.title === '词云'" class="img-content">
      <img :src="require(`@/assets/img/词云.png`)" alt="" />
    </div>
    <p class="experience-content">
      {{ exp.content }}
    </p>
    <template #footer>Footer content</template>
  </el-card>
</template>

<script>
export default {
  name: "ExperienceBlog",
  props: {
    exp: {
      type: Object,
      required: true,
      default: () => ({
        title: "",
        content: "",
      }),
    },
  },
};
</script>

<style lang="scss" scoped>
.el-card {
  background-color: rgb(50, 54, 68);
  color: #fff;
  border-color: transparent;
  border-radius: 20px;
  width: 800px;
  padding: 20px;
  margin-bottom: 20px;
  height: 500px;
  overflow-y: auto;
  &::-webkit-scrollbar {
    width: 0; /* Safari,Chrome 隐藏滚动条 */
    height: 0; /* Safari,Chrome 隐藏滚动条 */
    display: none; /* 移动端、pad 上Safari，Chrome，隐藏滚动条 */
  }
}
.img-content {
  display: flex;
  align-items: center;
  justify-content: center;
}
.experience-content {
  white-space: pre-line;
  line-height: 2em;
}
img {
  height: 350px;
}
</style>

