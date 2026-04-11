<template>
  <el-drawer
    :model-value="modelValue"
    :title="drawerTitle"
    :size="drawerSize"
    direction="rtl"
    class="detail-drawer"
    @close="handleClose"
  >
    <div v-if="type && data" class="drawer-content">
      <!-- 物理主机详情 -->
      <template v-if="type === 'computer'">
        <div class="detail-container">
          <!-- 基本信息 -->
          <div class="section-title"><el-icon><InfoFilled /></el-icon> 基本信息</div>
          <div class="info-section">
            <div class="info-row"><span class="label">名称</span><span class="value">{{ data.name }}</span></div>
            <div class="info-row"><span class="label">位置</span><span class="value">{{ data.location || '-' }}</span></div>
            <div v-if="data.remarks" class="info-row"><span class="label">备注</span><span class="value">{{ data.remarks }}</span></div>
          </div>

          <!-- 硬件 -->
          <div class="section-title" style="margin-top:20px;"><el-icon><Cpu /></el-icon> CPU</div>
          <div v-for="cpu in getComputerCpus(data.id)" :key="cpu.id" class="hardware-item col-item">
            <div class="item-name">{{ cpu.model }}</div>
            <div class="item-meta">{{ cpu.cores }}核 @ {{ cpu.clockSpeed }}GHz</div>
          </div>
          <div v-if="getComputerCpus(data.id).length === 0" class="empty-text">暂无CPU</div>

          <div class="section-title" style="margin-top:16px;"><el-icon><Histogram /></el-icon> 内存</div>
          <div v-for="ram in getComputerRams(data.id)" :key="ram.id" class="hardware-item col-item">
            <div class="item-name">{{ ram.brand }} {{ ram.model }}</div>
            <div class="item-meta">{{ ram.capacity }}GB {{ ram.type }}</div>
          </div>
          <div v-if="getComputerRams(data.id).length === 0" class="empty-text">暂无内存</div>

          <div class="section-title" style="margin-top:16px;"><el-icon><Folder /></el-icon> 硬盘</div>
          <div v-for="disk in getComputerDisks(data.id)" :key="disk.id" class="hardware-item col-item">
            <div class="item-name">{{ disk.brand }} {{ disk.model }}</div>
            <div class="item-meta">{{ disk.capacity }}GB {{ disk.interface }}</div>
          </div>
          <div v-if="getComputerDisks(data.id).length === 0" class="empty-text">暂无硬盘</div>

          <!-- 系统 -->
          <div class="section-title" style="margin-top:16px;">
            <el-icon><Box /></el-icon> 系统
            <el-button size="small" type="primary" @click="emit('open-add-os', data.id)" style="margin-left:8px">+ 添加</el-button>
          </div>
          <div v-for="os in getComputerOsInstances(data.id)" :key="os.id" class="hardware-item">
            <div class="item-content" @click="selectNode('os_instance', os)">
              <div class="item-name">
                <el-tag size="small" :type="getOsTypeTagType(os.type)">
                  {{ os.parentOsId ? os.type : '底层' }}
                </el-tag>
                {{ os.name }}
              </div>
              <div class="item-meta">{{ os.ipAddress || '无IP' }}</div>
            </div>
            <el-button size="small" type="danger" text @click.stop="confirmDeleteOs(os)">
              <el-icon><Delete /></el-icon>
            </el-button>
          </div>
          <div v-if="getComputerOsInstances(data.id).length === 0" class="empty-text">暂无系统</div>
        </div>
      </template>

      <!-- 系统/虚拟机详情 -->
      <template v-else-if="type === 'os_instance'">
        <div class="detail-container">
          <div class="info-section">
            <div class="info-row"><span class="label">名称</span><span class="value">{{ data.name }}</span></div>
            <div class="info-row"><span class="label">类型</span><span class="value"><el-tag size="small">{{ data.type }}</el-tag></span></div>
            <div class="info-row"><span class="label">IP</span><span class="value ip">{{ data.ipAddress || '未分配' }}</span></div>
            <div class="info-row"><span class="label">宿主</span><span class="value">{{ data.computerName }}</span></div>
            <div v-if="data.notes" class="info-row"><span class="label">备注</span><span class="value">{{ data.notes }}</span></div>
          </div>

          <div style="display:flex;gap:12px;margin-top:16px;">
            <el-button type="primary" @click="openEditOsDialog"><el-icon><Edit /></el-icon> 编辑配置</el-button>
          </div>

          <div class="section-title" style="margin-top:20px;"><el-icon><Connection /></el-icon> 运行服务</div>
          <div v-for="svc in getOsServices(data.id)" :key="svc.id" class="hardware-item service-item" @click="selectNode('service', svc)">
            <div class="item-name">{{ svc.name }}</div>
            <div class="item-meta">{{ svc.protocol }}://{{ svc.ip_address }}:{{ svc.port }}</div>
          </div>
          <el-empty v-if="getOsServices(data.id).length === 0" description="暂无服务" />
        </div>
      </template>

      <!-- 服务详情 -->
      <template v-else-if="type === 'service'">
        <div class="detail-container">
          <div class="info-section">
            <div class="info-row full-row">
              <div class="info-content">
                <div class="info-row"><span class="label">服务名</span><span class="value">{{ data.name }}</span></div>
                <div v-if="data.type" class="info-row"><span class="label">类型</span><span class="value"><el-tag size="small">{{ data.type }}</el-tag></span></div>
                <div class="info-row"><span class="label">协议</span><span class="value"><el-tag size="small">{{ data.protocol?.toUpperCase() }}</el-tag></span></div>
                <div v-if="data.description" class="info-row"><span class="label">描述</span><span class="value">{{ data.description }}</span></div>
              </div>
              <div class="info-content">
                <div class="info-row"><span class="label">地址</span><span class="value mono">{{ data.ip_address }}:{{ data.port }}</span></div>
                <div class="info-row"><span class="label">宿主</span><span class="value">{{ getOsInstanceName(data.osInstanceId) }}</span></div>
              </div>
            </div>
          </div>
          <div class="service-actions">
            <el-button type="primary" @click="openServiceUrl"><el-icon><Link /></el-icon> 访问</el-button>
            <el-button @click="copyServiceUrl"><el-icon><CopyDocument /></el-icon> 复制</el-button>
            <el-button @click="openEditServiceDialog"><el-icon><Edit /></el-icon> 编辑</el-button>
            <el-button type="danger" @click="confirmDeleteService"><el-icon><Delete /></el-icon> 删除</el-button>
          </div>
        </div>
      </template>
    </div>
  </el-drawer>
</template>

<script setup>
import { computed, inject } from 'vue'
import { Cpu, Histogram, Folder, Connection, Link, CopyDocument, Delete, InfoFilled, Box, Edit } from '@element-plus/icons-vue'
import { useAppStore } from '../stores/app'
import { ElMessage, ElMessageBox } from 'element-plus'

const props = defineProps({
  modelValue: Boolean,
  type: String,
  data: Object
})

const emit = defineEmits(['update:modelValue', 'refresh', 'open-add-os', 'open-edit-os', 'open-edit-service'])
const store = useAppStore()
const openDrawer = inject('openDrawer')

const drawerTitle = computed(() => {
  const titles = {
    computer: '物理主机详情',
    os_instance: '系统详情',
    service: '服务详情'
  }
  return titles[props.type] || '详情'
})

const drawerSize = computed(() => {
  return props.type === 'os_instance' ? '600px' : '500px'
})

const handleClose = () => {
  emit('update:modelValue', false)
}

const getComputerCpus = (cid) => store.getComputerCpus(cid)
const getComputerRams = (cid) => store.getComputerRams(cid)
const getComputerDisks = (cid) => store.getComputerDisks(cid)
const getComputerOsInstances = (cid) => store.getComputerOsInstances(cid)
const getOsServices = (osId) => store.getOsServices(osId)
const getOsInstanceName = (id) => store.getOsInstanceName(id)

// 获取 OS 类型标签显示
const getOsTypeTagType = (typeName) => {
  const config = store.state.typeConfigs.find(t => t.category === 'os_type' && t.name === typeName)
  if (config?.color) {
    const colorMap = { '#67C23A': 'success', '#409EFF': '', '#E6A23C': 'warning', '#F56C6C': 'danger', '#909399': 'info' }
    return colorMap[config.color] || 'warning'
  }
  return 'warning'
}

const selectNode = (type, data) => {
  openDrawer(type, data)
}

const confirmDeleteOs = (os) => {
  ElMessageBox.confirm(`确定要删除系统 "${os.name}" 吗?`, '确认删除', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await store.deleteOsInstance(os.id)
      emit('refresh')
      ElMessage.success('删除成功')
    } catch (e) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

const openServiceUrl = () => {
  if (props.data) {
    window.open(`${props.data.protocol}://${props.data.ip_address}:${props.data.port}`, '_blank')
  }
}

const copyServiceUrl = () => {
  if (props.data) {
    navigator.clipboard.writeText(`${props.data.protocol}://${props.data.ip_address}:${props.data.port}`)
    ElMessage.success('已复制')
  }
}

const openEditOsDialog = () => {
  emit('open-edit-os', props.data)
}

const openEditServiceDialog = () => {
  emit('open-edit-service', props.data)
}

const confirmDeleteService = () => {
  ElMessageBox.confirm(`确定要删除服务 "${props.data.name}" 吗?`, '确认删除', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await store.deleteService(props.data.id)
      emit('refresh')
      emit('update:modelValue', false)
      ElMessage.success('删除成功')
    } catch (e) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}
</script>

<style scoped>
.detail-container {
  padding: 16px;
}

.info-section {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.info-row {
  display: flex;
  padding: 8px 12px;
  background: var(--bg-gray-50);
  border-radius: var(--radius-md);
}

.info-row .label {
  width: 70px;
  color: var(--text-secondary);
  font-size: 0.8125rem;
  flex-shrink: 0;
}

.info-row .value {
  flex: 1;
  color: var(--text-primary);
  font-size: 0.8125rem;
}

.info-row .value.ip {
  font-family: var(--font-mono);
  color: var(--primary-color);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-light);
}

.section-title .el-button {
  margin-left: auto;
}

.hardware-item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  background: var(--bg-gray-50);
  border-radius: var(--radius-md);
  transition: background 0.15s;
  margin-bottom: 4px;
}

.hardware-item:hover {
  background: #ecf5ff;
}

.item-content {
  flex: 1;
  cursor: pointer;
}

.item-name {
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.8125rem;
  color: var(--text-primary);
}

.item-meta {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-top: 2px;
}

.service-item {
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
}

.service-item .item-name {
  width: 100%;
}

.service-item .item-meta {
  margin-top: 0;
  padding-left: 0;
}

.col-item {
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
}

.col-item .item-meta {
  margin-top: 0;
  padding-left: 0;
}

.empty-text {
  padding: 16px;
  text-align: center;
  color: var(--text-muted);
  font-size: 0.8125rem;
}

.info-row.full-row {
  display: flex;
  gap: 16px;
  padding: 0;
  background: transparent;
}

.info-row.full-row .info-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.info-row.full-row .info-content .info-row {
  padding: 6px 10px;
}

.service-actions {
  display: flex;
  gap: 8px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--border-light);
}

.value.mono {
  font-family: var(--font-mono, ui-monospace, SFMono-Regular, Consolas, monospace);
  font-weight: 500;
  color: #334155;
  background: #f1f5f9;
  padding: 2px 6px;
  border-radius: 4px;
}
</style>
