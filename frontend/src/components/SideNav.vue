<template>
  <nav class="side-nav">
    <el-menu
      :default-active="currentRoute"
      router
      class="nav-menu"
      background-color="#1e293b"
      text-color="#94a3b8"
      active-text-color="#60a5fa"
    >
      <el-menu-item index="/">
        <span class="nav-icon"><TreeList theme="outline" size="20" stroke="currentColor" /></span>
        <span>拓扑视图</span>
      </el-menu-item>
      <el-menu-item index="/computers">
        <span class="nav-icon"><Computer theme="outline" size="20" stroke="currentColor" /></span>
        <span>物理主机</span>
      </el-menu-item>
      <el-menu-item index="/hardware">
        <span class="nav-icon"><Cpu theme="outline" size="20" stroke="currentColor" /></span>
        <span>硬件库</span>
      </el-menu-item>
      <el-menu-item index="/services">
        <span class="nav-icon"><System theme="outline" size="20" stroke="currentColor" /></span>
        <span>服务列表</span>
      </el-menu-item>
      <el-menu-item index="/network">
        <span class="nav-icon"><NetworkTree theme="outline" size="20" stroke="currentColor" /></span>
        <span>IP地址列表</span>
      </el-menu-item>
      <el-menu-item index="/settings">
        <span class="nav-icon"><SettingConfig theme="outline" size="20" stroke="currentColor" /></span>
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
import { SuccessFilled } from '@element-plus/icons-vue'
import { TreeList, Computer, Cpu, NetworkTree, System, SettingConfig } from '@icon-park/vue-next'

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

.nav-icon {
  display: inline-flex;
  align-items: center;
  margin-right: 6px;
}

.nav-icon :deep(.i-icon) {
  display: flex;
  align-items: center;
}
</style>
