<template>
  <div class="detail-container">
    <el-tabs v-model="activeTab" class="detail-tabs">
      <el-tab-pane label="基本信息" name="info">
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
            <span class="label">IP地址</span>
            <span class="value ip">{{ data.ip_address || '未分配' }}</span>
          </div>
          <div class="info-row">
            <span class="label">MAC地址</span>
            <span class="value mac">{{ data.mac_address || '未知' }}</span>
          </div>
          <div class="info-row">
            <span class="label">PCIe直通</span>
            <span class="value">{{ data.pcie_passthrough || '无' }}</span>
          </div>
          <div class="info-row">
            <span class="label">备注</span>
            <span class="value">{{ data.notes || '无' }}</span>
          </div>
        </div>
      </el-tab-pane>

      <el-tab-pane label="存储溯源" name="storage">
        <div class="section-title">
          <el-icon><Guide /></el-icon> 虚拟磁盘 → 存储池 → 物理硬盘
        </div>
        <div v-for="vdisk in virtualDisks" :key="vdisk.id" class="storage-trace">
          <div class="trace-step vm">
            <el-icon><Box /></el-icon>
            <span>{{ vdisk.name }}</span>
            <span class="size">{{ vdisk.size_gb }}GB</span>
          </div>
          <div class="trace-line"></div>
          <div class="trace-step pool">
            <el-icon><Folder /></el-icon>
            <span>{{ vdisk.storage_pool?.name }}</span>
            <span class="type">{{ vdisk.storage_pool?.type }}</span>
          </div>
          <div class="trace-line"></div>
          <div class="trace-step disk">
            <el-icon><Cpu /></el-icon>
            <span>{{ vdisk.storage_pool?.disks?.[0]?.brand }} {{ vdisk.storage_pool?.disks?.[0]?.model }}</span>
            <span class="size">{{ vdisk.storage_pool?.disks?.[0]?.capacity_gb }}GB</span>
          </div>
        </div>
        <el-empty v-if="virtualDisks.length === 0" description="暂无虚拟磁盘" :image-size="60" />
      </el-tab-pane>

      <el-tab-pane label="运行服务" name="services">
        <div class="service-list">
          <div v-for="service in services" :key="service.id" class="service-item">
            <div class="service-icon">
              <el-icon><Connection /></el-icon>
            </div>
            <div class="service-info">
              <div class="service-name">{{ service.name }}</div>
              <div class="service-url">{{ service.protocol }}://{{ service.url }}:{{ service.port }}</div>
            </div>
            <el-tag size="small" :type="service.protocol === 'https' ? 'success' : ''">
              {{ service.protocol.toUpperCase() }}
            </el-tag>
          </div>
          <el-empty v-if="services.length === 0" description="暂无运行服务" :image-size="60" />
        </div>
      </el-tab-pane>

      <el-tab-pane label="子虚拟机" name="children">
        <div class="vm-list">
          <div v-for="child in childVms" :key="child.id" class="vm-item">
            <el-tag size="small" :type="child.type === 'LXC' ? 'warning' : ''">
              {{ child.type }}
            </el-tag>
            <span class="vm-name">{{ child.name }}</span>
            <span class="vm-ip">{{ child.ip_address || '无IP' }}</span>
          </div>
          <el-empty v-if="childVms.length === 0" description="无子虚拟机" :image-size="60" />
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Guide, Box, Folder, Cpu, Connection } from '@element-plus/icons-vue'

const props = defineProps({
  data: Object
})

const activeTab = ref('info')

// 模拟数据
const virtualDisks = ref([
  {
    id: 1,
    name: 'vm-101-disk-0.qcow2',
    size_gb: 100,
    storage_pool: {
      name: 'local-lvm',
      type: 'LVM',
      disks: [{ brand: 'Samsung', model: 'PM983', capacity_gb: 960 }]
    }
  }
])

const services = ref([
  { id: 1, name: 'HomeAssistant', protocol: 'https', url: 'homeassistant.local', port: 8123 },
  { id: 2, name: 'Nextcloud', protocol: 'https', url: 'nextcloud.local', port: 443 }
])

const childVms = ref([
  { id: 2, name: 'OpenWrt-主路由', type: 'LXC', ip_address: '192.168.1.1' }
])
</script>

<style scoped>
.detail-container {
  height: 100%;
}

.detail-tabs :deep(.el-tabs__header) {
  margin: 0;
  background: #f5f7fa;
  padding: 0 16px;
}

.detail-tabs :deep(.el-tabs__nav-wrap::after) {
  display: none;
}

.detail-tabs :deep(.el-tabs__content) {
  padding: 16px;
}

.info-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
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

.info-row .value.ip,
.info-row .value.mac {
  font-family: 'Monaco', 'Menlo', monospace;
  color: #409EFF;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 16px;
}

.storage-trace {
  background: #f5f7fa;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
}

.trace-step {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  background: white;
  border-radius: 8px;
  border-left: 3px solid;
}

.trace-step.vm {
  border-color: #409EFF;
}

.trace-step.pool {
  border-color: #67C23A;
}

.trace-step.disk {
  border-color: #E6A23C;
}

.trace-step .el-icon {
  font-size: 20px;
}

.trace-step span {
  flex: 1;
}

.trace-step .size,
.trace-step .type {
  font-size: 12px;
  color: #909399;
  background: #f5f7fa;
  padding: 2px 8px;
  border-radius: 4px;
}

.trace-line {
  width: 2px;
  height: 16px;
  background: #dcdfe6;
  margin-left: 24px;
}

.service-list,
.vm-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.service-item,
.vm-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: #f5f7fa;
  border-radius: 8px;
}

.service-icon {
  width: 36px;
  height: 36px;
  background: #409EFF;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.service-info {
  flex: 1;
}

.service-name {
  font-weight: 500;
  color: #303133;
}

.service-url {
  font-size: 12px;
  color: #909399;
  font-family: 'Monaco', 'Menlo', monospace;
}

.vm-name {
  flex: 1;
  font-weight: 500;
  color: #303133;
}

.vm-ip {
  color: #909399;
  font-size: 12px;
}
</style>
