<template>
  <div class="detail-container">
    <div class="info-section">
      <div class="info-row">
        <span class="label">名称</span>
        <span class="value">{{ data.name }}</span>
      </div>
      <div class="info-row">
        <span class="label">格式</span>
        <span class="value">
          <el-tag size="small" type="info">{{ data.format }}</el-tag>
        </span>
      </div>
      <div class="info-row">
        <span class="label">容量</span>
        <span class="value">{{ data.size_gb }} GB</span>
      </div>
      <div class="info-row">
        <span class="label">挂载到</span>
        <span class="value">{{ data.os_instance?.name || '未挂载' }}</span>
      </div>
    </div>

    <div class="trace-section">
      <div class="section-title">
        <el-icon><Guide /></el-icon> 存储溯源路径
      </div>
      <div class="trace-path">
        <div class="trace-node host">
          <el-icon><Odometer /></el-icon>
          <span>{{ data.computer?.name || '物理机' }}</span>
        </div>
        <div class="trace-arrow">→</div>
        <div class="trace-node pool">
          <el-icon><Folder /></el-icon>
          <span>{{ data.storage_pool?.name || '存储池' }}</span>
        </div>
        <div class="trace-arrow">→</div>
        <div class="trace-node disk">
          <el-icon><Box /></el-icon>
          <span>{{ data.name }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Guide, Odometer, Folder, Box } from '@element-plus/icons-vue'

defineProps({
  data: Object
})
</script>

<style scoped>
.detail-container {
  padding: 20px;
}

.info-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.info-row {
  display: flex;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 8px;
}

.info-row .label {
  width: 80px;
  color: #909399;
  font-size: 14px;
}

.info-row .value {
  flex: 1;
  color: #303133;
  font-size: 14px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e4e7ed;
}

.trace-path {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 12px;
}

.trace-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px 20px;
  background: white;
  border-radius: 8px;
  border: 2px solid #e4e7ed;
  min-width: 100px;
}

.trace-node.host {
  border-color: #67C23A;
}

.trace-node.pool {
  border-color: #409EFF;
}

.trace-node.disk {
  border-color: #E6A23C;
}

.trace-node .el-icon {
  font-size: 24px;
}

.trace-node.host .el-icon {
  color: #67C23A;
}

.trace-node.pool .el-icon {
  color: #409EFF;
}

.trace-node.disk .el-icon {
  color: #E6A23C;
}

.trace-arrow {
  color: #909399;
  font-size: 20px;
}
</style>
