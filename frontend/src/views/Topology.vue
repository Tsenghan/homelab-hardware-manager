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
      <div v-for="computer in store.state.computers" :key="computer.id" style="margin-bottom:4px;">
        <!-- Host 节点 -->
        <div
          class="tree-node host-node"
          :class="{ active: selectedId === computer.id && selectedType === 'computer' }"
          @click="selectNode('computer', computer)"
        >
          <div class="node-icon"><Computer theme="outline" size="16" stroke="currentColor" /></div>
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
          <div v-for="os in getDirectChildrenOs(computer.id)" :key="os.id" >
            <!-- OS 节点 -->
            <div
              class="tree-node os-node"
              :class="{ 'is-parent': hasChildren(os.id), active: selectedId === os.id && selectedType === 'os_instance' }"
              @click="selectNode('os_instance', os)"
            >
              <div class="node-icon">
                <DatabasePoint v-if="!os.parentOsId" theme="outline" size="16" stroke="currentColor" />
                <DataServer v-else theme="outline" size="16" stroke="currentColor" />
              </div>
              <div class="node-info">
                <div class="node-name">
                  {{ os.name }}
                  <el-tag size="small" :style="getOsTypeStyle(os.type)">
                    {{ os.parentOsId ? os.type : '底层' }}
                  </el-tag>
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
                  <div class="node-icon">
                    <DataServer theme="outline" size="16" stroke="currentColor" />
                  </div>
                  <div class="node-info">
                    <div class="node-name">
                      {{ childOs.name }}
                      <el-tag size="small" :style="getOsTypeStyle(childOs.type)">{{ childOs.type }}</el-tag>
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
                    <div class="node-icon"><System theme="outline" size="14" stroke="currentColor" /></div>
                    <div class="node-info">
                      <div class="node-name">
                        {{ svc.name }}
                        <el-tag v-if="svc.type" size="small" :style="getServiceTypeStyle(svc.type)">
                          {{ svc.type }}
                        </el-tag>
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
              <div v-for="svc in getOsServices(os.id)" :key="svc.id" style="margin-bottom:0;">
                <div
                  class="tree-node service-node"
                  :class="{ active: selectedId === svc.id && selectedType === 'service' }"
                  @click="selectNode('service', svc)"
                >
                  <div class="node-icon"><System theme="outline" size="14" stroke="currentColor" /></div>
                  <div class="node-info">
                    <div class="node-name">
                      {{ svc.name }}
                      <el-tag v-if="svc.type" size="small" :style="getServiceTypeStyle(svc.type)">
                        {{ svc.type }}
                      </el-tag>
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
import { ArrowRight, ArrowDown } from '@element-plus/icons-vue'
import { Computer, Server, ComputerOne, System, DatabasePoint, DataServer } from '@icon-park/vue-next'
import { useAppStore } from '../stores/app'

const store = useAppStore()
const openDrawer = inject('openDrawer')

const expandedIds = ref([])
const selectedId = ref(null)
const selectedType = ref(null)

// 获取 OS 类型样式
const getOsTypeStyle = (typeName) => {
  const color = store.state.typeConfigs.find(t => t.category === 'os_type' && t.name === typeName)?.color || '#f59e0b'
  return {
    backgroundColor: `${color}15`,
    borderColor: color,
    color: color
  }
}

// 获取服务类型样式
const getServiceTypeStyle = (typeName) => {
  const color = store.state.typeConfigs.find(t => t.category === 'service_type' && t.name === typeName)?.color || '#909399'
  return {
    backgroundColor: `${color}15`,
    borderColor: color,
    color: color
  }
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
.topology-container > div { margin-bottom: 2px !important; }
.tree-children > div { margin-bottom: 0px !important; }

/* --- 核心：收紧树节点行高 --- */
.tree-node {
  display: flex;
  align-items: center;
  padding: 3px 8px; /* ✨ 从 2px 8px 改为 3px，让文本高度更均衡 */
  margin-bottom: 1px; /* ✨ 统一节点间距，拒绝松散 */
  border-radius: 4px;
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
  padding-right: 4px;
}

/* ✨ 缩小字体，提升专业感 */
.node-name {
  display: flex;
  align-items: center;
  gap: 4px;
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
  font-size: 0.7rem;
  color: #64748b;
  background: #f1f5f9;
  padding: 0 4px;
  border-radius: 3px;
}

/* --- ✨ 统一图标尺寸和中性灰骨架色 --- */
.node-icon {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 6px;
  flex-shrink: 0;
  background: #64748b;
  color: #fff;
}

.node-icon :deep(.i-icon) {
  display: flex;
  align-items: center;
}

/* 各层级的灰色微调：层级越高颜色越深 */
.host-node .node-icon { background: #475569; } /* slate-600 */
.os-node .node-icon { background: #64748b; } /* slate-500 */
.os-node.is-parent .node-icon { background: #64748b; } /* slate-500 */
.vm-node .node-icon { background: #94a3b8; } /* slate-400 */

.service-node {
  padding: 2px 8px; /* ✨ 最后一层极度压缩，体现从属感 */
  margin-bottom: 0;
}

/* --- 统一所有图标的占位盒模型 --- */
.service-node .node-icon {
  width: 24px;  /* ✨ 核心修复：强制与上面的实心图标 24px 同宽 */
  height: 24px;
  margin-right: 6px; /* ✨ 强制与上面的图标保持相同的右边距 */
  background: transparent;
  color: #94a3b8;
  border-radius: 0;
  box-shadow: none;
  justify-content: center;
}
.node-expand {
  width: 20px;
  height: 20px;
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

/* 统一控制所有层级的左侧缩进容器 */
.tree-children,
.vm-children,
.child-services {
  /* ✨ 核心算式：8px(父级padding) + 12px(图标中点) = 20px */
  margin-left: 20px; 
  padding-left: 14px; /* 竖线到子节点文字的呼吸距离 */
  border-left: 1px solid #cbd5e1; /* ✨ 改用 1px 细线，显得更清晰锐利 */
}

/* 服务层用虚线区分 */
.child-services {
  border-left-style: dashed; 
}

/* ✨ 修复导致结构崩溃的“罪魁祸首” */
.child-os-wrapper {
  padding-left: 0; /* 删掉这里多余的边距，交给上面统一控制 */
  margin-left: 0;
  margin-bottom: 0;
}

/* 隐藏最后一个子节点的连接线尾巴（可选美化） */
.child-services:last-child {
  margin-bottom: 4px;
}
:deep(.el-tag) {
  line-height: 1;
  display: inline-flex;
  align-items: center;
  padding: 1px 5px; /* 压缩原生 Tag 的高度 */
  height: auto;
}
</style>