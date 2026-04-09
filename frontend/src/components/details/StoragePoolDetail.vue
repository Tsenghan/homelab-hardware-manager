<template>
  <div class="detail-container">
    <div class="info-section">
      <div class="info-row">
        <span class="label">名称</span>
        <span class="value">{{ data.name }}</span>
      </div>
      <div class="info-row">
        <span class="label">类型</span>
        <span class="value">
          <el-tag size="small">{{ data.type }}</el-tag>
        </span>
      </div>
      <div class="info-row">
        <span class="label">关联硬盘</span>
        <span class="value">{{ data.disks?.length || 0 }} 块</span>
      </div>
    </div>

    <div class="disk-list">
      <div class="section-title">
        <el-icon><Folder /></el-icon> 底层物理硬盘
      </div>
      <div v-for="disk in data.disks" :key="disk.id" class="disk-item">
        <div class="disk-icon">
          <el-icon><Folder /></el-icon>
        </div>
        <div class="disk-info">
          <div class="disk-name">{{ disk.brand }} {{ disk.model }}</div>
          <div class="disk-meta">{{ disk.capacity_gb }}GB · {{ disk.interface }} · {{ disk.slot_info }}</div>
        </div>
      </div>
    </div>

    <div class="vdisk-list">
      <div class="section-title">
        <el-icon><Box /></el-icon> 虚拟磁盘
      </div>
      <div v-for="vdisk in data.virtual_disks" :key="vdisk.id" class="vdisk-item">
        <div class="vdisk-name">{{ vdisk.name }}</div>
        <div class="vdisk-meta">{{ vdisk.format }} · {{ vdisk.size_gb }}GB</div>
      </div>
      <el-empty v-if="!data.virtual_disks?.length" description="暂无虚拟磁盘" :image-size="60" />
    </div>
  </div>
</template>

<script setup>
import { Folder, Box } from '@element-plus/icons-vue'

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
  width: 100px;
  color: #909399;
  font-size: 14px;
}

.info-row .value {
  flex: 1;
  color: #303133;
  font-size: 14px;
}

.disk-list,
.vdisk-list {
  margin-bottom: 24px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e4e7ed;
}

.disk-item,
.vdisk-item {
  display: flex;
  align-items: center;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 8px;
}

.disk-icon {
  width: 40px;
  height: 40px;
  background: #409EFF;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-right: 12px;
}

.disk-info {
  flex: 1;
}

.disk-name,
.vdisk-name {
  font-weight: 500;
  color: #303133;
}

.disk-meta,
.vdisk-meta {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}
</style>
