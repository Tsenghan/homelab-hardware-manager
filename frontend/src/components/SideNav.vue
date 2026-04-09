<template>
  <nav class="side-nav">
    <el-menu
      :default-active="currentRoute"
      router
      class="nav-menu"
      background-color="#304156"
      text-color="#bfcbd9"
      active-text-color="#409EFF"
    >
      <el-menu-item index="/">
        <el-icon><Connection /></el-icon>
        <span>拓扑视图</span>
      </el-menu-item>
      <el-menu-item index="/computers">
        <el-icon><Monitor /></el-icon>
        <span>物理主机</span>
      </el-menu-item>
      <el-menu-item index="/hardware">
        <el-icon><Cpu /></el-icon>
        <span>硬件库</span>
      </el-menu-item>
      <el-menu-item index="/services">
        <el-icon><Service /></el-icon>
        <span>服务列表</span>
      </el-menu-item>
      <el-menu-item index="/network">
        <el-icon><Grid /></el-icon>
        <span>IP网络</span>
      </el-menu-item>
      <el-menu-item index="/settings">
        <el-icon><Setting /></el-icon>
        <span>配置管理</span>
      </el-menu-item>
    </el-menu>

    <div class="nav-footer">
      <div class="db-status">
        <el-icon><SuccessFilled /></el-icon>
        <span>数据库已连接</span>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Connection, Monitor, Cpu, Grid, Setting, SuccessFilled, Service } from '@element-plus/icons-vue'

const route = useRoute()
const currentRoute = computed(() => route.path)
</script>

<style scoped>
.side-nav {
  width: 200px;
  background: var(--bg-white);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  height: calc(100vh - 56px);
}

.nav-menu {
  flex: 1;
  border-right: none;
  padding: 8px;
}

.nav-menu:not(.el-menu--collapse) {
  width: 200px;
}

.nav-footer {
  padding: 12px 16px;
  border-top: 1px solid var(--border-light);
}

.db-status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.75rem;
  color: var(--success-color);
}
</style>
