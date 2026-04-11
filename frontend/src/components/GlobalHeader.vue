<template>
  <header class="global-header">
    <div class="header-left">
      <h1 class="logo">
        <Computer theme="outline" size="24" stroke="currentColor" />
        HomeLab 硬件资产
      </h1>
    </div>
    <div class="header-center">
      <GlobalSearch @select="handleSearchSelect" />
    </div>
    <div class="header-right">
    </div>
  </header>
</template>

<script setup>
import GlobalSearch from './GlobalSearch.vue'
import { Computer } from '@icon-park/vue-next'

const emit = defineEmits(['search'])

const handleSearchSelect = (result) => {
  emit('search', result)
}
</script>

<style scoped>
.global-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
  padding: 0 20px;
  background: var(--bg-white);
  border-bottom: 1px solid var(--border-color);
}

.header-left {
  display: flex;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
  color: var(--text-primary);
}

.logo :deep(.i-icon) {
  display: flex;
  align-items: center;
  color: var(--primary-color);
}

.header-center {
  flex: 1;
  max-width: 500px;
  margin: 0 32px;
}

.header-right {
  display: flex;
  gap: 8px;
}

.header-right .el-button {
  background: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
}

.header-right .el-button:hover {
  background: var(--bg-gray-50);
  border-color: var(--bg-gray-300);
}
</style>
