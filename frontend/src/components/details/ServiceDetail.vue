<template>
  <div class="detail-container">
    <div class="info-section">
      <div class="info-row">
        <span class="label">服务名</span>
        <span class="value">{{ data.name }}</span>
      </div>
      <div class="info-row">
        <span class="label">协议</span>
        <span class="value">
          <el-tag size="small" :type="data.protocol === 'https' ? 'success' : ''">
            {{ data.protocol?.toUpperCase() }}
          </el-tag>
        </span>
      </div>
      <div class="info-row">
        <span class="label">地址</span>
        <span class="value url">{{ data.url }}</span>
      </div>
      <div class="info-row">
        <span class="label">端口</span>
        <span class="value port">{{ data.port }}</span>
      </div>
      <div class="info-row">
        <span class="label">运行于</span>
        <span class="value">
          <el-tag size="small" type="warning">{{ data.os_instance?.name || '未知' }}</el-tag>
        </span>
      </div>
      <div class="info-row">
        <span class="label">备注</span>
        <span class="value">{{ data.notes || '无' }}</span>
      </div>
    </div>

    <div class="action-section">
      <el-button @click="openService">
        <el-icon><Link /></el-icon>
        访问服务
      </el-button>
      <el-button @click="copyUrl">
        <el-icon><CopyDocument /></el-icon>
        复制地址
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { Link, CopyDocument } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  data: Object
})

const openService = () => {
  const url = `${props.data.protocol}://${props.data.url}:${props.data.port}`
  window.open(url, '_blank')
}

const copyUrl = () => {
  const url = `${props.data.protocol}://${props.data.url}:${props.data.port}`
  navigator.clipboard.writeText(url)
  ElMessage.success('已复制到剪贴板')
}
</script>

<style scoped>
.detail-container {
  padding: 20px;
}

.info-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 24px;
}

.info-row {
  flex-direction: column;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 8px;
  gap: 6px;
}

.info-row .label {
  color: #909399;
  font-size: 14px;
}

.info-row .value {
  color: #303133;
  font-size: 14px;
}

.info-row .value.url {
  font-family: 'Monaco', 'Menlo', monospace;
  color: #409EFF;
}

.info-row .value.port {
  font-family: 'Monaco', 'Menlo', monospace;
  font-weight: 600;
}

.action-section {
  display: flex;
  gap: 12px;
}
</style>
