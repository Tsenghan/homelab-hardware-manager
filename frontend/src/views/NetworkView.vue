<template>
  <div class="network-view">
    <div class="view-header">
      <h2 class="page-title">
        IP列表
        <span class="inline-filters">
          <el-input v-model="ipFilter" placeholder="搜索IP..." clearable style="width: 160px; margin-left: 12px">
            <template #prefix><el-icon><Search /></el-icon></template>
          </el-input>
          <el-select v-model="ipGroupFilter" placeholder="分组" clearable style="width: 140px; margin-left: 8px">
            <el-option v-for="g in store.state.ipGroups" :key="g.id" :label="g.name + ' (' + g.subnet + ')'" :value="g.id" />
          </el-select>
          <el-checkbox v-model="showIdleIps" style="margin-left: 8px">显示空闲IP</el-checkbox>
          <el-button type="primary" @click="showDialog = true" style="margin-left: 8px">
            <el-icon><Plus /></el-icon>
            添加分组
          </el-button>
        </span>
      </h2>
      <div class="header-actions">
        <el-button @click="toggleExpandAll">
          {{ allExpanded ? '折叠全部' : '展开全部' }}
        </el-button>
      </div>
    </div>

    <div class="ip-groups">
      <div v-for="group in filteredIpGroups" :key="group.id" class="ip-group">
        <div class="ip-group-header" @click="toggleGroup(group.id)">
          <div class="ip-group-title">
            <FolderOpen theme="outline" size="16" stroke="currentColor" />
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
                <th style="width:250px">主机/名称</th>
                <th style="width:100px">类型</th>
                <th>服务 (端口)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="ip in group.ips" :key="ip.ip" :class="{ idle: !ip.occupied }">
                <td>
                    <span class="ip-cell" :class="ip.occupied ? 'occupied' : 'idle'">{{ ip.ip }}</span>
                </td>
                <td>
                  <span v-if="ip.hostName" class="host-link" @click="navigateToIp(ip)">{{ ip.hostName }}</span>
                  <span v-else style="color:#dcdfe6">—</span>
                </td>
                <td><el-tag size="small" :type="ip.tagType">{{ ip.typeName }}</el-tag></td>
                <td>
                  <div class="service-tags">
                    <span
                      v-for="svc in ip.services"
                      :key="svc.id"
                      class="service-tag"
                      :style="{ background: svc.bgColor }"
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
import { Search, Edit, Delete, ArrowRight, ArrowDown } from '@element-plus/icons-vue'
import { FolderOpen } from '@icon-park/vue-next'
import { useAppStore } from '../stores/app'
import { ElMessage, ElMessageBox } from 'element-plus'

const store = useAppStore()
const openDrawer = inject('openDrawer')

// 静态映射表，避免循环内重复创建
const OS_TYPE_TAG_MAP = { 'PVE': 'warning', 'LXC': 'info', 'VM': '', 'Linux': 'success', 'Windows': 'danger' }
const IP_TYPE_TAG_MAP = { computer: '', os_instance: 'success', service: 'warning', service_only: 'warning', idle: 'info' }

const getServiceTypeColor = (typeName) => {
  if (!typeName) return '#94a3b8'
  const config = store.state.typeConfigs.find(t => t.category === 'service_type' && t.name === typeName)
  if (config?.color) {
    return config.color
  }
  return '#94a3b8'
}

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

const isValidIp = (ip) => {
  if (!ip || typeof ip !== 'string') return false
  const parts = ip.split('.')
  if (parts.length !== 4) return false
  return parts.every(p => {
    const num = parseInt(p, 10)
    return !isNaN(num) && num >= 0 && num <= 255
  })
}

const ipToNum = (ip) => {
  if (!isValidIp(ip)) return NaN
  const parts = ip.split('.')
  return parseInt(parts[3], 10)
}

const ipInRange = (ip, start, end) => {
  const ipNum = ipToNum(ip)
  const startNum = ipToNum(start)
  const endNum = ipToNum(end)
  if (isNaN(ipNum) || isNaN(startNum) || isNaN(endNum)) return false
  return ipNum >= startNum && ipNum <= endNum
}

const ipGroups = computed(() => {
  // 预构建查找表，彻底干掉 find
  const osInstanceByIp = new Map()
  const osInstanceById = new Map()
  store.state.allOsInstances.forEach(os => {
    osInstanceById.set(os.id, os)
    if (os.ipAddress) {
      osInstanceByIp.set(os.ipAddress, os)
    }
  })

  const servicesByIp = new Map()
  store.state.services.forEach(s => {
    if (s.ip_address) {
      if (!servicesByIp.has(s.ip_address)) {
        servicesByIp.set(s.ip_address, [])
      }
      servicesByIp.get(s.ip_address).push(s)
    }
  })

  return store.state.ipGroups.map(group => {
    const ips = []
    const startNum = ipToNum(group.startIp)
    const endNum = ipToNum(group.endIp)

    // Skip invalid IP ranges (including infinite loop prevention when start > end)
    if (isNaN(startNum) || isNaN(endNum) || startNum > endNum) {
      return {
        ...group,
        ips: [],
        usedCount: 0,
        totalCount: 0
      }
    }

    // 提前计算 IP 前缀，避免循环内正则
    const baseIpStr = group.startIp.substring(0, group.startIp.lastIndexOf('.') + 1)

    // Generate all IPs in range
    for (let i = startNum; i <= endNum; i++) {
      const ipStr = baseIpStr + i
      const osInstance = osInstanceByIp.get(ipStr)
      const ipServices = servicesByIp.get(ipStr) || []

      let hostName = osInstance?.name || ''
      if (!hostName && ipServices.length > 0) {
        const firstSvc = ipServices[0]
        const hostOs = osInstanceByIp.get(firstSvc.ip_address) || osInstanceById.get(firstSvc.osInstanceId)
        hostName = hostOs?.computerName || hostOs?.name || firstSvc.name || ''
      }

      const isOs = !!osInstance
      const hasService = ipServices.length > 0
      const ipType = isOs ? 'os_instance' : (hasService ? 'service_only' : 'idle')

      // 提前计算 tagType，避免模板中重复调用函数
      let tagType = 'info'
      if (isOs && osInstance.type) {
        tagType = OS_TYPE_TAG_MAP[osInstance.type] || ''
      } else {
        tagType = IP_TYPE_TAG_MAP[ipType] || 'info'
      }

      // 提前计算服务颜色（基于服务类型）
      const processedServices = ipServices.map(svc => ({
        ...svc,
        bgColor: getServiceTypeColor(svc.type)
      }))

      ips.push({
        ip: ipStr,
        hostName: hostName,
        type: ipType,
        osType: osInstance?.type || '',
        refId: osInstance?.id || (hasService ? ipServices[0].osInstanceId : null),
        occupied: isOs || hasService,
        entity: osInstance || null,
        services: processedServices,
        typeName: isOs ? (osInstance.type || 'OS') : (hasService ? '服务' : '空闲'),
        tagType: tagType
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

// 默认只展开第一个分组，避免大量 IP 同时渲染导致卡顿
expandedGroups.value = store.state.ipGroups.length > 0 ? [store.state.ipGroups[0].id] : []
</script>

<style scoped>
.network-view {
  padding: 0;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.inline-filters {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.filter-bar {
  display: flex;
  margin-bottom: 16px;
  align-items: center;
}

/* --- 卡片与间距排版 --- */
.ip-groups {
  display: flex;
  flex-direction: column;
  gap: 16px; /* 稍微拉开一点分组之间的距离，增加呼吸感 */
}

.ip-group {
  background: var(--bg-white, #ffffff);
  border: 1px solid var(--border-light, #e4e7ed);
  border-radius: var(--radius-lg, 8px);
  overflow: hidden; /* ✨ 核心：确保内容不会超出圆角 */
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.03); /* ✨ 统一的柔和阴影 */
  transition: box-shadow 0.3s ease;
}

.ip-group:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06); /* 鼠标移入时阴影稍微加深 */
}

/* --- 分组标题栏 (颜值核心重构) --- */
.ip-group-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: #f8fafc; /* ✨ 改用极浅的蓝灰色，不再刺眼 */
  color: #334155;      /* ✨ 深色文字，高对比度 */
  border-left: 4px solid var(--primary-color, #409eff); /* ✨ 用左侧的一抹主色来强调层级 */
  border-bottom: 1px solid var(--border-light, #ebeef5);
  cursor: pointer;
  transition: background-color 0.2s;
}

.ip-group-header:hover {
  background: #f1f5f9;
}

.ip-group-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600; /* 标题字重加粗一点 */
  font-size: 0.9rem;
  color: #1e293b;
}

.ip-group-title :deep(.i-icon) {
  display: flex;
  align-items: center;
}

.ip-group-count {
  background: #e2e8f0; /* 标签底色配合浅色主题 */
  color: #64748b;
  padding: 2px 8px;
  border-radius: 12px; /* 药丸形状更具现代感 */
  font-size: 0.75rem;
  font-weight: 500;
}

/* --- 表格样式 --- */
.ip-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed; /* 解决列宽不对齐的神器 */
}

.ip-table th,
.ip-table td {
  padding: 10px 16px; /* 稍微增加一点内边距 */
  text-align: left;
  border-bottom: 1px solid var(--border-light, #ebeef5);
  font-size: 0.8125rem;
}

.ip-table th {
  background: #ffffff; /* 表头纯白，和上面灰色的 header 形成反差 */
  font-weight: 500;
  font-size: 0.75rem;
  color: #94a3b8;
}

.ip-table tr:hover td {
  background: #fcfcfd;
}

.ip-table tr:last-child td {
  border-bottom: none;
}

.header-actions :deep(.i-icon) {
  display: flex;
  align-items: center;
}

/* --- IP 数据展示 --- */
.ip-cell {
  font-family: var(--font-mono, ui-monospace, SFMono-Regular, Consolas, monospace);
  font-size: 0.8125rem;
}

.ip-cell.occupied {
  /* ✨ 和服务列表统一：代码块风格的 IP 显示 */
  color: #334155; 
  background-color: #f1f5f9; 
  padding: 3px 6px;
  border-radius: 4px;
  border: 1px solid #e2e8f0;
  display: inline-block;
  line-height: 1;
}

.ip-cell.idle {
  color: #cbd5e1; /* 空闲 IP 颜色再淡一点，降低干扰 */
}

.host-link {
  color: #1e293b;
  cursor: pointer;
  font-weight: 500;
}

.host-link:hover {
  text-decoration: underline;
}

/* --- 标签优化 --- */
.service-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: center;
}

.service-tag {
  display: inline-flex; /* ✨ 修复裁切问题 */
  align-items: center;
  justify-content: center;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  color: white;
  cursor: pointer;
  font-weight: 500;
  line-height: 1; /* ✨ 修复裁切问题 */
  box-sizing: border-box;
}

.service-tag:hover {
  opacity: 0.85;
  transform: translateY(-1px); /* 悬停时微微上浮的微交互 */
}

.add-service-btn {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  background: #f8fafc;
  color: #94a3b8;
  border: 1px dashed #cbd5e1;
  cursor: pointer;
  line-height: 1;
  transition: all 0.2s;
}

.add-service-btn:hover {
  background: #eff6ff;
  color: var(--primary-color, #409eff);
  border-color: var(--primary-color, #409eff);
}
</style>