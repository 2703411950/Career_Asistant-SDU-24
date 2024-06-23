<template>
  <el-card>
    <template #header>
      <div class="experience-title">
        <span>{{ jobItem.job }}</span>
      </div>
    </template>
    <p class="experience-content">
      {{ jobItem.requriement }}
    </p>
    <template #footer>Footer content</template>
  </el-card>
</template>

<script>
export default {
  name: "JobInformationCard",
  props: {
    jobItem: {
      type: Object,
      required: true,
      default: () => ({
        job: "",
        requriement: "",
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
}
.experience-content {
  white-space: pre-line;
  line-height: 2em;
}
</style>
