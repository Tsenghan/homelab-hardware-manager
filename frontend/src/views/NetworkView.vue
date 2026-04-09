<template>
  <div class="network-view">
    <div class="view-header">
      <h2 class="page-title">IP 网络视图</h2>
      <div class="header-actions">
        <el-button @click="toggleExpandAll">
          {{ allExpanded ? '折叠全部' : '展开全部' }}
        </el-button>
        <el-button @click="showDialog = true">
          <el-icon><FolderAdd /></el-icon> 添加分组
        </el-button>
      </div>
    </div>

    <div class="filter-bar">
      <el-input v-model="ipFilter" placeholder="搜索IP或主机名..." clearable style="width: 300px">
        <template #prefix><el-icon><Search /></el-icon></template>
      </el-input>
      <el-select v-model="ipGroupFilter" placeholder="分组" clearable style="width: 200px; margin-left: 12px">
        <el-option v-for="g in store.state.ipGroups" :key="g.id" :label="g.name + ' (' + g.subnet + ')'" :value="g.id" />
      </el-select>
      <el-checkbox v-model="showIdleIps" style="margin-left: 12px">显示空闲IP</el-checkbox>
    </div>

    <div class="ip-groups">
      <div v-for="group in filteredIpGroups" :key="group.id" class="ip-group">
        <div class="ip-group-header" @click="toggleGroup(group.id)">
          <div class="ip-group-title">
            <el-icon><Folder /></el-icon>
            <span>{{ group.name }}</span>
            <span style="opacity:0.7;font-size:12px">{{ group.startIp }} - {{ group.endIp }}</span>
            <span class="ip-group-count">{{ group.usedCount }}/{{ group.totalCount }} 已用</span>
          </div>
          <div @click.stop>
            <el-button size="small" text @click="editGroup(group)"><el-icon><Edit /></el-icon></el-button>
            <el-button size="small" text type="danger" @click="confirmDeleteGroup(group)"><el-icon><Delete /></el-icon></el-button>
            <el-icon v-if="!expandedGroups.includes(group.id)"><ArrowRight /></el-icon>
            <el-icon v-else><ArrowDown /></el-icon>
          </div>
        </div>

        <div v-if="expandedGroups.includes(group.id)">
          <table class="ip-table">
            <thead>
              <tr>
                <th style="width:140px">IP地址</th>
                <th>主机/名称</th>
                <th style="width:100px">类型</th>
                <th>服务 (端口)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="ip in group.ips" :key="ip.ip" :class="{ idle: !ip.occupied }">
                <td class="ip-cell" :class="ip.occupied ? 'occupied' : 'idle'">{{ ip.ip }}</td>
                <td>
                  <span v-if="ip.hostName" class="host-link" @click="navigateToIp(ip)">{{ ip.hostName }}</span>
                  <span v-else style="color:#dcdfe6">—</span>
                </td>
                <td><el-tag size="small" :type="getIpTypeTag(ip.type)">{{ ip.typeName }}</el-tag></td>
                <td>
                  <div class="service-tags">
                    <span
                      v-for="svc in ip.services"
                      :key="svc.id"
                      class="service-tag"
                      :style="{ background: store.getProtocolColor(svc.protocol) }"
                      @click="openDrawer('service', svc)"
                    >
                      {{ svc.name }}:{{ svc.port }}
                    </span>
                    <span v-if="ip.occupied" class="add-service-btn" @click="openAddServiceForIp(ip)">+ 添加</span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <el-empty v-if="filteredIpGroups.length === 0" description="暂无IP数据" />
    </div>

    <!-- IP Group Dialog -->
    <el-dialog v-model="showDialog" :title="editingGroup ? '编辑分组' : '添加分组'" width="500px">
      <el-form label-width="80px">
        <el-form-item label="分组名称" required>
          <el-input v-model="form.name" placeholder="如 网络设备" />
        </el-form-item>
        <el-form-item label="子网">
          <el-input v-model="form.subnet" placeholder="如 192.168.1.0/24" />
        </el-form-item>
        <el-form-item label="起始IP" required>
          <el-input v-model="form.startIp" placeholder="如 192.168.1.1" />
        </el-form-item>
        <el-form-item label="结束IP" required>
          <el-input v-model="form.endIp" placeholder="如 192.168.1.30" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="saveGroup">保存</el-button>
      </template>
    </el-dialog>

    <!-- Add Service Dialog -->
    <el-dialog v-model="showServiceDialog" title="添加服务" width="500px">
      <el-form label-width="80px">
        <el-form-item label="服务名称" required>
          <el-input v-model="serviceForm.name" placeholder="如 Nginx" />
        </el-form-item>
        <el-form-item label="所属系统" required>
          <el-select v-model="serviceForm.osInstanceId" placeholder="选择系统" style="width: 100%">
            <el-option
              v-for="os in store.state.allOsInstances"
              :key="os?.id"
              :label="os?.name + ' (' + os?.computerName + ')'"
              :value="os?.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="协议" required>
          <el-select v-model="serviceForm.protocol" placeholder="选择协议" style="width: 100%">
            <el-option v-for="p in protocolOptions" :key="p?.name" :label="p?.name" :value="p?.name" />
          </el-select>
        </el-form-item>
        <el-form-item label="IP地址" required>
          <el-input v-model="serviceForm.ip_address" placeholder="如 192.168.1.1" />
        </el-form-item>
        <el-form-item label="端口" required>
          <el-input-number v-model="serviceForm.port" :min="1" :max="65535" style="width: 100%" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="serviceForm.description" type="textarea" rows="2" placeholder="服务描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showServiceDialog = false">取消</el-button>
        <el-button type="primary" @click="saveService">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, inject } from 'vue'
import { Folder, FolderAdd, Search, Edit, Delete, ArrowRight, ArrowDown } from '@element-plus/icons-vue'
import { useAppStore } from '../stores/app'
import { ElMessage, ElMessageBox } from 'element-plus'

const store = useAppStore()
const openDrawer = inject('openDrawer')

const ipFilter = ref('')
const ipGroupFilter = ref('')
const showIdleIps = ref(false)
const expandedGroups = ref([])
const showDialog = ref(false)
const editingGroup = ref(null)
const showServiceDialog = ref(false)
const serviceForm = ref({
  name: '',
  osInstanceId: null,
  protocol: 'http',
  ip_address: '',
  port: null,
  description: ''
})

const protocolOptions = computed(() => {
  const configs = store.protocolConfigs
  if (!configs) return []
  return Array.isArray(configs) ? configs : (configs.value || [])
})

const form = ref({
  name: '',
  subnet: '192.168.1.0/24',
  startIp: '',
  endIp: ''
})

const ipToNum = (ip) => {
  const parts = ip.split('.')
  return parseInt(parts[3])
}

const ipInRange = (ip, start, end) => {
  const ipNum = ipToNum(ip)
  return ipNum >= ipToNum(start) && ipNum <= ipToNum(end)
}

const ipGroups = computed(() => {
  return store.state.ipGroups.map(group => {
    const ips = []
    const startNum = ipToNum(group.startIp)
    const endNum = ipToNum(group.endIp)

    // Collect all occupied IPs from osInstances
    const occupiedIps = []
    store.state.allOsInstances.forEach(os => {
      if (os.ipAddress && ipInRange(os.ipAddress, group.startIp, group.endIp)) {
        occupiedIps.push({
          ip: os.ipAddress,
          hostName: os.name,
          type: 'os_instance',
          refId: os.id,
          entity: os
        })
      }
    })

    // Generate all IPs in range
    for (let i = startNum; i <= endNum; i++) {
      const ipStr = group.startIp.replace(/\d+$/, i)
      const record = occupiedIps.find(r => r.ip === ipStr)
      const ipServices = store.state.services.filter(s => s.ip_address === ipStr)

      let hostName = record?.hostName || ''
      if (!hostName && ipServices.length > 0) {
        const firstSvc = ipServices[0]
        const hostOs = store.state.allOsInstances.find(os => os.id === firstSvc.osInstanceId)
        hostName = hostOs?.computerName || hostOs?.name || firstSvc.name || ''
      }

      ips.push({
        ip: ipStr,
        hostName: hostName,
        type: record?.type || (ipServices.length ? 'service_only' : 'idle'),
        refId: record?.refId || (ipServices.length ? ipServices[0].osInstanceId : null),
        occupied: !!record || ipServices.length > 0,
        entity: record?.entity || null,
        services: ipServices,
        typeName: record ? '虚拟机' : (ipServices.length ? '服务' : '空闲')
      })
    }

    return {
      ...group,
      ips: ips,
      usedCount: ips.filter(ip => ip.occupied).length,
      totalCount: ips.length
    }
  })
})

const filteredIpGroups = computed(() => {
  let groups = ipGroups.value
  if (ipGroupFilter.value) {
    groups = groups.filter(g => g.id === ipGroupFilter.value)
  }
  if (!showIdleIps.value) {
    groups = groups.map(g => ({
      ...g,
      ips: g.ips.filter(ip => ip.occupied)
    })).filter(g => g.ips.length > 0)
  }
  if (ipFilter.value) {
    const q = ipFilter.value.toLowerCase()
    groups = groups.map(g => ({
      ...g,
      ips: g.ips.filter(ip => ip.ip.includes(q) || (ip.hostName && ip.hostName.toLowerCase().includes(q)))
    })).filter(g => g.ips.length > 0)
  }
  return groups
})

const allExpanded = computed(() => {
  return store.state.ipGroups.every(g => expandedGroups.value.includes(g.id))
})

const toggleGroup = (id) => {
  const idx = expandedGroups.value.indexOf(id)
  if (idx > -1) {
    expandedGroups.value.splice(idx, 1)
  } else {
    expandedGroups.value.push(id)
  }
}

const toggleExpandAll = () => {
  if (allExpanded.value) {
    expandedGroups.value = []
  } else {
    expandedGroups.value = store.state.ipGroups.map(g => g.id)
  }
}

const getIpTypeTag = (type) => {
  const map = { computer: '', os_instance: 'success', service: 'warning', service_only: 'warning', idle: 'info' }
  return map[type] || 'info'
}

const navigateToIp = (ip) => {
  if (ip.type === 'os_instance') {
    const os = store.getOsInstanceById(ip.refId)
    if (os) openDrawer('os_instance', os)
  }
}

const openAddServiceForIp = (ip) => {
  serviceForm.value = {
    name: '',
    osInstanceId: ip.refId || null,
    protocol: 'http',
    ip_address: ip.ip,
    port: null,
    description: ''
  }
  showServiceDialog.value = true
}

const saveService = async () => {
  if (!serviceForm.value.name || !serviceForm.value.osInstanceId) {
    ElMessage.warning('请填写服务名称和选择系统')
    return
  }
  try {
    await store.saveService(serviceForm.value.osInstanceId, {
      name: serviceForm.value.name,
      protocol: serviceForm.value.protocol,
      ip_address: serviceForm.value.ip_address,
      port: serviceForm.value.port,
      description: serviceForm.value.description
    })
    showServiceDialog.value = false
    store.loadData()
    ElMessage.success('添加成功')
  } catch (e) {
    ElMessage.error('添加失败')
  }
}

const editGroup = (group) => {
  editingGroup.value = group
  form.value = {
    name: group.name,
    subnet: group.subnet,
    startIp: group.startIp,
    endIp: group.endIp
  }
  showDialog.value = true
}

const confirmDeleteGroup = (group) => {
  ElMessageBox.confirm(`确定要删除分组 "${group.name}" 吗?`, '确认删除', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await store.deleteIpGroup(group.id)
      ElMessage.success('删除成功')
    } catch (e) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

const saveGroup = async () => {
  try {
    await store.saveIpGroup(form.value, editingGroup.value?.id)
    showDialog.value = false
    editingGroup.value = null
    resetForm()
    ElMessage.success('保存成功')
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

const resetForm = () => {
  form.value = {
    name: '',
    subnet: '192.168.1.0/24',
    startIp: '',
    endIp: ''
  }
}

// Expand all by default
expandedGroups.value = store.state.ipGroups.map(g => g.id)
</script>

<style scoped>
.network-view {
  padding: 0;
}

.filter-bar {
  display: flex;
  margin-bottom: 16px;
}

.ip-groups {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.ip-group {
  background: var(--bg-white);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.ip-group-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: var(--primary-color);
  color: white;
  cursor: pointer;
  transition: opacity 0.15s;
}

.ip-group-header:hover {
  opacity: 0.9;
}

.ip-group-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 500;
  font-size: 0.875rem;
}

.ip-group-count {
  background: rgba(255, 255, 255, 0.2);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
}

.ip-table {
  width: 100%;
  border-collapse: collapse;
}

.ip-table th,
.ip-table td {
  padding: 8px 14px;
  text-align: left;
  border-bottom: 1px solid var(--border-light);
  font-size: 0.8125rem;
}

.ip-table th {
  background: var(--bg-gray-50);
  font-weight: 500;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-secondary);
}

.ip-table tr:hover td {
  background: var(--bg-gray-50);
}

.ip-table tr:last-child td {
  border-bottom: none;
}

.ip-table tr.idle td {
  color: var(--text-muted);
}

.ip-cell {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
}

.ip-cell.occupied {
  color: var(--text-primary);
}

.ip-cell.idle {
  color: var(--text-muted);
}

.host-link {
  color: var(--primary-color);
  cursor: pointer;
}

.host-link:hover {
  text-decoration: underline;
}

.service-tag {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  color: white;
  cursor: pointer;
  font-weight: 500;
}

.service-tag:hover {
  opacity: 0.85;
}

.add-service-btn {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  background: #f5f7fa;
  color: #909399;
  border: 1px dashed #dcdfe6;
  cursor: pointer;
}

.add-service-btn:hover {
  background: #ecf5ff;
  color: #409EFF;
  border-color: #409EFF;
}
</style>
