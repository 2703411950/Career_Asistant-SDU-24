<template>
  <el-card>
    <template #header>
      <div class="experience-title">
        <span>{{ exp.title }}</span>
      </div>
    </template>
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
}
.experience-content {
  white-space: pre-line;
  line-height: 2em;
}
</style>
