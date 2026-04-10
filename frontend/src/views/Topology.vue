<template>
  <div class="topology-view">
    <div class="view-header">
      <h2 class="page-title">拓扑视图</h2>
      <div class="header-actions">
        <el-button @click="expandAll">展开全部</el-button>
        <el-button @click="collapseAll">折叠全部</el-button>
      </div>
    </div>

    <div class="topology-container">
      <div v-for="computer in store.state.computers" :key="computer.id" style="margin-bottom:12px;">
        <div
          class="tree-node host-node"
          :class="{ active: selectedId === computer.id && selectedType === 'computer' }"
          @click="selectNode('computer', computer)"
        >
          <div class="node-icon"><el-icon><Monitor /></el-icon></div>
          <div class="node-info">
            <div class="node-name">{{ computer.name }}</div>
            <div class="node-meta">{{ computer.location || '' }}</div>
          </div>
          <div class="node-expand" @click.stop="toggleExpand(`host-${computer.id}`)">
            <el-icon v-if="!expandedIds.includes(`host-${computer.id}`)"><ArrowRight /></el-icon>
            <el-icon v-else><ArrowDown /></el-icon>
          </div>
        </div>

        <div v-if="expandedIds.includes(`host-${computer.id}`)" class="tree-children">
          <div v-for="os in getAllOsInstances(computer.id)" :key="os.id" style="margin-bottom:4px;">
            <!-- Skip VMs here — they render inside their parent's expanded section -->
            <template v-if="!os.parentOsId">
            <div
              class="tree-node os-node"
              :class="{ 'is-parent': !os.parentOsId, active: selectedId === os.id && selectedType === 'os_instance' }"
              @click="selectNode('os_instance', os)"
            >
              <div class="node-icon"><el-icon><component :is="getOsIcon(os.type)" /></el-icon></div>
              <div class="node-info">
                <div class="node-name">
                  <el-tag size="small" :type="os.parentOsId ? 'warning' : 'success'">
                    {{ os.parentOsId ? 'VM' : 'Host' }}
                  </el-tag>
                  {{ os.name }}
                </div>
                <div class="node-meta">{{ os.type }} · {{ os.ipAddress || '无IP' }}</div>
              </div>
              <div v-if="os.childVmIds && os.childVmIds.length" class="node-expand" @click.stop="toggleExpand(`os-${os.id}`)">
                <el-icon v-if="!expandedIds.includes(`os-${os.id}`)"><ArrowRight /></el-icon>
                <el-icon v-else><ArrowDown /></el-icon>
              </div>
            </div>

            <div v-if="expandedIds.includes(`os-${os.id}`)">
              <div v-if="os.childVmIds && os.childVmIds.length" class="vm-children">
                <div v-for="childId in os.childVmIds" :key="childId" style="margin-bottom:2px;">
                  <div
                    class="tree-node vm-node"
                    :class="{ active: selectedId === childId && selectedType === 'os_instance' }"
                    @click="selectChildVm(childId)"
                  >
                    <div class="node-icon"><el-icon><component :is="getChildVmIcon(childId)" /></el-icon></div>
                    <div class="node-info">
                      <div class="node-name">
                        <el-tag size="small" type="warning">{{ getChildVmType(childId) }}</el-tag>
                        {{ getChildVmName(childId) }}
                      </div>
                      <div class="node-meta">{{ getChildVmIp(childId) }}</div>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="getOsServices(os.id).length" class="service-children">
                <div v-for="svc in getOsServices(os.id)" :key="svc.id" style="margin-bottom:2px;">
                  <div
                    class="tree-node service-node"
                    :class="{ active: selectedId === svc.id && selectedType === 'service' }"
                    @click="selectNode('service', svc)"
                  >
                    <div class="node-icon"><el-icon><Connection /></el-icon></div>
                    <div class="node-info">
                      <div class="node-name">
                        <el-tag size="small" :type="svc.protocol === 'https' ? 'success' : 'info'">
                          {{ svc.protocol?.toUpperCase() }}
                        </el-tag>
                        {{ svc.name }}
                      </div>
                      <div class="node-meta">{{ svc.ip_address }}:{{ svc.port }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            </template>
          </div>
        </div>
      </div>

      <el-empty v-if="store.state.computers.length === 0" description="暂无主机数据" />
    </div>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue'
import { Monitor, Box, Connection, ArrowRight, ArrowDown, Odometer, Tickets } from '@element-plus/icons-vue'
import { useAppStore } from '../stores/app'

const store = useAppStore()
const openDrawer = inject('openDrawer')

const expandedIds = ref([])
const selectedId = ref(null)
const selectedType = ref(null)

// Icon mapping for different OS types
const osIconMap = {
  'PVE': Odometer,
  'LXC': Tickets,
  'VM': Box,
  'Linux': Odometer,
  'Windows': Tickets,
  'default': Box
}

const getOsIcon = (type) => {
  return osIconMap[type] || osIconMap['default']
}

const getAllOsInstances = (computerId) => {
  return store.getComputerOsInstances(computerId)
}

const getOsServices = (osId) => {
  return store.getOsServices(osId)
}

const getChildVmName = (childId) => {
  const vm = store.getOsInstanceById(childId)
  return vm?.name || ''
}

const getChildVmType = (childId) => {
  const vm = store.getOsInstanceById(childId)
  return vm?.type || 'VM'
}

const getChildVmIp = (childId) => {
  const vm = store.getOsInstanceById(childId)
  return vm?.ipAddress || ''
}

const getChildVmIcon = (childId) => {
  const vm = store.getOsInstanceById(childId)
  return getOsIcon(vm?.type)
}

const selectNode = (type, data) => {
  selectedType.value = type
  selectedId.value = data.id
  openDrawer(type, data)
}

const selectChildVm = (childId) => {
  const vm = store.getOsInstanceById(childId)
  if (vm) {
    selectNode('os_instance', vm)
  }
}

const toggleExpand = (id) => {
  const idx = expandedIds.value.indexOf(id)
  if (idx > -1) {
    expandedIds.value.splice(idx, 1)
  } else {
    expandedIds.value.push(id)
  }
}

const expandAll = () => {
  const ids = []
  store.state.computers.forEach(c => {
    ids.push(`host-${c.id}`)
    store.getComputerOsInstances(c.id).forEach(os => {
      // Expand OS instances that have services OR child VMs
      const hasServices = store.getOsServices(os.id).length > 0
      const hasChildVms = os.childVmIds && os.childVmIds.length
      if (hasServices || hasChildVms) {
        ids.push(`os-${os.id}`)
      }
    })
  })
  expandedIds.value = ids
}

const collapseAll = () => {
  expandedIds.value = []
}

// Expand all by default on mount
expandAll()
</script>

<style scoped>
.topology-view {
  padding: 0;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px; /* 缩小头部间距 */
}

.header-actions {
  display: flex;
  gap: 12px;
}

.topology-container {
  background: var(--bg-white, #ffffff);
  border: 1px solid var(--border-light, #e4e7ed);
  border-radius: var(--radius-lg, 8px);
  padding: 12px 16px; /* 缩小外围留白 */
  max-height: calc(100vh - 140px);
  overflow-y: auto;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.03);
}

/* ✨ 强制压缩 HTML 中写死的 margin-bottom */
.topology-container > div { margin-bottom: 6px !important; }
.tree-children > div { margin-bottom: 0px !important; }

/* --- 核心：收紧树节点行高 --- */
.tree-node {
  display: flex;
  align-items: center;
  padding: 4px 8px; /* ✨ 大幅缩小上下内边距 */
  border-radius: 4px; /* 圆角稍微收敛 */
  cursor: pointer;
  transition: all 0.15s ease;
  border: 1px solid transparent;
}

.tree-node:hover {
  background: #f8fafc;
  border-color: #f1f5f9;
}

.tree-node.active {
  background: #eff6ff;
  border-color: #bfdbfe;
  box-shadow: inset 3px 0 0 var(--primary-color, #409eff);
}

.node-info {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-right: 8px; /* 缩小右侧留白 */
}

/* ✨ 缩小字体，提升专业感 */
.node-name {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 500;
  color: #1e293b;
  font-size: 0.8125rem; /* 约 13px，紧凑型后台标准字体 */
}

.node-meta {
  font-family: var(--font-mono, ui-monospace, SFMono-Regular, monospace);
  font-size: 0.75rem; /* 约 12px */
  color: #64748b;
  background: #f1f5f9;
  padding: 1px 6px; /* 压缩标签内边距 */
  border-radius: 4px;
}

/* --- ✨ 同步缩小图标，避免撑大行高 --- */
.node-icon {
  width: 24px; /* 从 32px 缩减到 24px */
  height: 24px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
  font-size: 13px; /* 缩小图标内字体 */
  color: white;
  flex-shrink: 0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.host-node .node-icon { background: linear-gradient(135deg, #10b981, #059669); }
.os-node .node-icon { background: linear-gradient(135deg, #3b82f6, #2563eb); }
.os-node.is-parent .node-icon { background: linear-gradient(135deg, #10b981, #059669); }
.vm-node .node-icon { background: linear-gradient(135deg, #f59e0b, #d97706); }

/* 服务节点变得更迷你 */
.service-node .node-icon {
  background: #cbd5e1;
  color: #475569;
  width: 20px; 
  height: 20px;
  font-size: 11px;
  border-radius: 4px;
  box-shadow: none;
}

.node-expand {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  flex-shrink: 0;
  border-radius: 4px;
  transition: background 0.15s;
}

.node-expand:hover {
  background: #e2e8f0;
  color: #475569;
}

/* --- 压缩缩进线的间距 --- */
.tree-children {
  margin-left: 20px; /* 原 28px，向左靠拢 */
  padding-left: 12px;
  border-left: 2px solid #e2e8f0;
  margin-top: 2px;
}

.vm-children,
.service-children {
  margin-left: 12px; /* 向左靠拢 */
  padding-left: 12px;
  border-left: 1px dashed #cbd5e1; /* 虚线改细一点，降低视觉干扰 */
  margin-top: 0;
}

:deep(.el-tag) {
  line-height: 1;
  display: inline-flex;
  align-items: center;
  padding: 1px 5px; /* 压缩原生 Tag 的高度 */
  height: auto;
}
</style>