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
        <!-- Host 节点 -->
        <div
          class="tree-node host-node"
          :class="{ active: selectedId === computer.id && selectedType === 'computer' }"
          @click="selectNode('computer', computer)"
        >
          <div class="node-icon"><el-icon><Monitor /></el-icon></div>
          <div class="node-info">
            <div class="node-name">
              {{ computer.name }}
              <span v-if="computer.remarks" class="node-notes">{{ computer.remarks }}</span>
            </div>
            <div class="node-meta">{{ computer.location || '' }}</div>
          </div>
          <div class="node-expand" @click.stop="toggleExpand(`host-${computer.id}`)">
            <el-icon v-if="!expandedIds.includes(`host-${computer.id}`)"><ArrowRight /></el-icon>
            <el-icon v-else><ArrowDown /></el-icon>
          </div>
        </div>

        <!-- Host 下的 OS 实例 -->
        <div v-if="expandedIds.includes(`host-${computer.id}`)" class="tree-children">
          <div v-for="os in getDirectChildrenOs(computer.id)" :key="os.id" style="margin-bottom:4px;">
            <!-- OS 节点 -->
            <div
              class="tree-node os-node"
              :class="{ 'is-parent': hasChildren(os.id), active: selectedId === os.id && selectedType === 'os_instance' }"
              @click="selectNode('os_instance', os)"
            >
              <div class="node-icon"><el-icon><component :is="getOsIcon(os.type)" /></el-icon></div>
              <div class="node-info">
                <div class="node-name">
                  <el-tag size="small" :type="getOsTypeTagType(os.type)">
                    {{ os.parentOsId ? os.type : '底层' }}
                  </el-tag>
                  {{ os.name }}
                  <span v-if="os.notes" class="node-notes">{{ os.notes }}</span>
                </div>
                <div class="node-meta">{{ os.ipAddress || '无IP' }}</div>
              </div>
              <div v-if="hasChildren(os.id) || getOsServices(os.id).length" class="node-expand" @click.stop="toggleExpand(`os-${os.id}`)">
                <el-icon v-if="!expandedIds.includes(`os-${os.id}`)"><ArrowRight /></el-icon>
                <el-icon v-else><ArrowDown /></el-icon>
              </div>
            </div>

            <!-- OS 下的子 VM/LXC 和服务 -->
            <div v-if="expandedIds.includes(`os-${os.id}`)" class="vm-children">
              <!-- 子 VM/LXC 及其服务 -->
              <div v-for="childOs in getChildOsInstances(os.id)" :key="childOs.id" class="child-os-wrapper">
                <div
                  class="tree-node vm-node"
                  :class="{ active: selectedId === childOs.id && selectedType === 'os_instance' }"
                  @click="selectNode('os_instance', childOs)"
                >
                  <div class="node-icon"><el-icon><component :is="getOsIcon(childOs.type)" /></el-icon></div>
                  <div class="node-info">
                    <div class="node-name">
                      <el-tag size="small" :type="getOsTypeTagType(childOs.type)">{{ childOs.type }}</el-tag>
                      {{ childOs.name }}
                      <span v-if="childOs.notes" class="node-notes">{{ childOs.notes }}</span>
                    </div>
                    <div class="node-meta">{{ childOs.ipAddress || '无IP' }}</div>
                  </div>
                  <div v-if="getOsServices(childOs.id).length" class="node-expand" @click.stop="toggleExpand(`child-os-${childOs.id}`)">
                    <el-icon v-if="!expandedIds.includes(`child-os-${childOs.id}`)"><ArrowRight /></el-icon>
                    <el-icon v-else><ArrowDown /></el-icon>
                  </div>
                </div>

                <!-- 子 VM/LXC 的服务 -->
                <div v-if="expandedIds.includes(`child-os-${childOs.id}`)" class="child-services">
                  <div v-for="svc in getOsServices(childOs.id)" :key="svc.id" class="tree-node service-node" :class="{ active: selectedId === svc.id && selectedType === 'service' }" @click="selectNode('service', svc)">
                    <div class="node-icon"><el-icon><Connection /></el-icon></div>
                    <div class="node-info">
                      <div class="node-name">
                        <el-tag v-if="svc.type" size="small" :type="getServiceTypeTagType(svc.type)">
                          {{ svc.type }}
                        </el-tag>
                        {{ svc.name }}
                        <span v-if="svc.description" class="node-notes">{{ svc.description }}</span>
                      </div>
                      <div class="node-meta">
                        <el-tag size="small" :type="svc.protocol === 'https' ? 'success' : 'info'">
                          {{ svc.protocol?.toUpperCase() }}
                        </el-tag>
                        {{ svc.ip_address }}:{{ svc.port }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 顶级 OS 自己的服务 -->
              <div v-for="svc in getOsServices(os.id)" :key="svc.id" style="margin-bottom:2px;">
                <div
                  class="tree-node service-node"
                  :class="{ active: selectedId === svc.id && selectedType === 'service' }"
                  @click="selectNode('service', svc)"
                >
                  <div class="node-icon"><el-icon><Connection /></el-icon></div>
                  <div class="node-info">
                    <div class="node-name">
                      <el-tag v-if="svc.type" size="small" :type="getServiceTypeTagType(svc.type)">
                        {{ svc.type }}
                      </el-tag>
                      {{ svc.name }}
                      <span v-if="svc.description" class="node-notes">{{ svc.description }}</span>
                    </div>
                    <div class="node-meta">
                      <el-tag size="small" :type="svc.protocol === 'https' ? 'success' : 'info'">
                        {{ svc.protocol?.toUpperCase() }}
                      </el-tag>
                      {{ svc.ip_address }}:{{ svc.port }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <el-empty v-if="store.state.computers.length === 0" description="暂无主机数据" />
    </div>
  </div>
</template>

<script setup>
import { ref, inject, watch, onMounted } from 'vue'
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

// 获取 OS 类型颜色
const getOsTypeColor = (typeName) => {
  const config = store.state.typeConfigs.find(t => t.category === 'os_type' && t.name === typeName)
  return config?.color || '#f59e0b' // 默认黄色
}

// 获取 OS 类型标签显示
const getOsTypeTagType = (typeName) => {
  const config = store.state.typeConfigs.find(t => t.category === 'os_type' && t.name === typeName)
  if (config?.color) {
    const colorMap = { '#67C23A': 'success', '#409EFF': '', '#E6A23C': 'warning', '#F56C6C': 'danger', '#909399': 'info' }
    return colorMap[config.color] || 'warning'
  }
  return 'warning'
}

// 获取服务类型标签显示
const getServiceTypeTagType = (typeName) => {
  const config = store.state.typeConfigs.find(t => t.category === 'service_type' && t.name === typeName)
  if (config?.color) {
    const colorMap = { '#67C23A': 'success', '#409EFF': '', '#E6A23C': 'warning', '#F56C6C': 'danger', '#909399': 'info' }
    return colorMap[config.color] || 'info'
  }
  return 'info'
}

// 获取直接子 OS 实例（顶级，没有父）
const getDirectChildrenOs = (computerId) => {
  return store.state.allOsInstances.filter(os => os.computerId === computerId && !os.parentOsId)
}

// 获取子 VM/LXC
const getChildOsInstances = (parentOsId) => {
  return store.state.allOsInstances.filter(os => os.parentOsId === parentOsId)
}

// 检查是否有子节点
const hasChildren = (osId) => {
  return store.state.allOsInstances.some(os => os.parentOsId === osId)
}

const getOsServices = (osId) => {
  return store.getOsServices(osId)
}

const selectNode = (type, data) => {
  selectedType.value = type
  selectedId.value = data.id
  openDrawer(type, data)
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
  // 展开所有 host
  store.state.computers.forEach(c => {
    ids.push(`host-${c.id}`)
  })
  // 展开所有 OS 实例
  store.state.allOsInstances.forEach(os => {
    ids.push(`os-${os.id}`)
  })
  // 展开所有子 VM/LXC 的服务
  store.state.allOsInstances.forEach(os => {
    if (os.parentOsId) {
      ids.push(`child-os-${os.id}`)
    }
  })
  expandedIds.value = ids
}

const collapseAll = () => {
  expandedIds.value = []
}

// Watch for data to be loaded, then expand all
watch(
  () => store.state.computers.length,
  (newLen) => {
    if (newLen > 0) {
      setTimeout(() => expandAll(), 100)
    }
  },
  { immediate: true }
)

watch(
  () => store.state.services.length,
  () => {
    // Re-expand when services are loaded
    if (store.state.computers.length > 0) {
      expandAll()
    }
  }
)

onMounted(() => {
  // Initial expand if data already loaded
  if (store.state.computers.length > 0) {
    expandAll()
  }
})
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

.node-notes {
  font-weight: 400;
  color: #94a3b8;
  font-size: 0.75rem;
  margin-left: 4px;
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

/* --- 树状缩进 --- */
/* Level 1: OS 实例（Host 下） */
.tree-children,
.vm-children {
  margin-left: 32px;
  padding-left: 16px;
  border-left: 2px solid #e2e8f0;
  margin-top: 2px;
}

/* Level 2: 子 VM/LXC */
.child-os-wrapper {
  border-left: 1px solid #cbd5e1;
  padding-left: 20px;
  margin-left: 16px;
  margin-bottom: 4px;
}

/* Level 3: 子 VM 下的服务 */
.child-services {
  padding-left: 24px;
  border-left: 1px dashed #cbd5e1;
  margin-left: 16px;
}

.child-services .tree-node {
  margin-bottom: 2px;
}

:deep(.el-tag) {
  line-height: 1;
  display: inline-flex;
  align-items: center;
  padding: 1px 5px; /* 压缩原生 Tag 的高度 */
  height: auto;
}
</style>