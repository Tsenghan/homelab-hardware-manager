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
            <span class="label">IP地址</span>
            <span class="value ip">{{ data.ip }}</span>
          </div>
          <div class="info-row">
            <span class="label">位置</span>
            <span class="value">{{ data.location }}</span>
          </div>
          <div class="info-row">
            <span class="label">备注</span>
            <span class="value">{{ data.notes || '无' }}</span>
          </div>
        </div>
      </el-tab-pane>

      <el-tab-pane label="硬件" name="hardware">
        <div class="hardware-section">
          <div class="section-title">
            <Cpu theme="outline" size="14" stroke="currentColor" /> CPU ({{ cpus.length }})
          </div>
          <div v-for="cpu in cpus" :key="cpu.id" class="hardware-item" @click="$emit('select', 'cpu', cpu)">
            <div class="item-name">{{ cpu.model }}</div>
            <div class="item-meta">{{ cpu.cores }}核 @ {{ cpu.clock_speed_ghz }}GHz</div>
          </div>

          <div class="section-title">
            <MemoryOne theme="outline" size="14" stroke="currentColor" /> 内存 ({{ rams.length }})
          </div>
          <div v-for="ram in rams" :key="ram.id" class="hardware-item" @click="$emit('select', 'ram', ram)">
            <div class="item-name">{{ ram.brand }} {{ ram.model }}</div>
            <div class="item-meta">{{ ram.capacity_gb }}GB {{ ram.type }} · {{ ram.slots_occupied }}</div>
          </div>

          <div class="section-title">
            <HardDisk theme="outline" size="14" stroke="currentColor" /> 硬盘 ({{ disks.length }})
          </div>
          <div v-for="disk in disks" :key="disk.id" class="hardware-item" @click="$emit('select', 'disk', disk)">
            <div class="item-name">{{ disk.brand }} {{ disk.model }}</div>
            <div class="item-meta">{{ disk.capacity_gb }}GB {{ disk.interface }} · {{ disk.is_boot_disk ? '系统盘' : '数据盘' }}</div>
          </div>
        </div>
      </el-tab-pane>

      <el-tab-pane label="虚拟机/系统" name="vms">
        <div class="hardware-section">
          <div v-for="vm in osInstances" :key="vm.id" class="hardware-item" @click="$emit('select', 'os_instance', vm)">
            <div class="item-name">
              <el-tag size="small" :type="vm.parent_os_id ? 'warning' : 'success'">
                {{ vm.parent_os_id ? 'VM' : 'Host' }}
              </el-tag>
              {{ vm.name }}
            </div>
            <div class="item-meta">{{ vm.type }} · {{ vm.ip_address || '无IP' }}</div>
          </div>
          <el-empty v-if="osInstances.length === 0" description="暂无系统实例" :image-size="60" />
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, computed, inject } from 'vue'
import { Cpu as EpCpu, Histogram as EpHistogram, Folder as EpFolder } from '@element-plus/icons-vue'
import { Cpu, MemoryOne, HardDisk } from '@icon-park/vue-next'

const props = defineProps({
  data: Object
})

defineEmits(['select'])

const activeTab = ref('info')
const cpus = ref([])
const rams = ref([])
const disks = ref([])
const osInstances = ref([])

// 模拟数据
if (props.data?.id) {
  cpus.value = [
    { id: 1, model: 'Intel Xeon E-2286G', cores: 12, clock_speed_ghz: 4.0 }
  ]
  rams.value = [
    { id: 1, brand: 'Samsung', model: 'M393A2G40AB2', capacity_gb: 32, type: 'DDR4', slots_occupied: 'DIMM_A1' }
  ]
  disks.value = [
    { id: 1, brand: 'Samsung', model: 'PM983', capacity_gb: 960, interface: 'NVMe', is_boot_disk: true }
  ]
  osInstances.value = [
    { id: 1, name: 'Proxmox VE 8', type: 'PVE', ip_address: '192.168.1.100', parent_os_id: null },
    { id: 2, name: 'OpenWrt-主路由', type: 'LXC', ip_address: '192.168.1.1', parent_os_id: 1 }
  ]
}
</script>

<style scoped>
.detail-container {
  height: 100%;
}

.detail-tabs {
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

.info-row .value.ip {
  font-family: 'Monaco', 'Menlo', monospace;
  color: #409EFF;
}

.hardware-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-top: 8px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e4e7ed;
}

.section-title :deep(.i-icon) {
  display: flex;
  align-items: center;
}

.hardware-item {
  padding: 12px 16px;
  background: #f5f7fa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.hardware-item:hover {
  background: #ecf5ff;
  transform: translateX(4px);
}

.item-name {
  font-weight: 500;
  color: #303133;
  display: flex;
  align-items: center;
  gap: 8px;
}

.item-meta {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}
</style>
