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

.topology-container {
  background: var(--bg-white);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 16px;
  max-height: calc(100vh - 140px);
  overflow-y: auto;
}

.node-icon {
  width: 28px;
  height: 28px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  font-size: 14px;
  color: white;
  flex-shrink: 0;
}

.host-node .node-icon {
  background: var(--success-color);
}

.os-node .node-icon {
  background: var(--primary-color);
}

.os-node.is-parent .node-icon {
  background: var(--success-color);
}

.vm-node .node-icon {
  background: var(--warning-color);
}

.service-node .node-icon {
  background: var(--text-muted);
  width: 24px;
  height: 24px;
  font-size: 12px;
}

.node-expand {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  flex-shrink: 0;
}

.tree-children {
  margin-left: 28px;
  padding-left: 16px;
  border-left: 1px solid var(--border-light);
}

.vm-children,
.service-children {
  margin-left: 16px;
  padding-left: 12px;
  border-left: 1px dashed var(--border-light);
}
</style>
