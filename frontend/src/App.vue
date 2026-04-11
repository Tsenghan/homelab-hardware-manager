<template>
  <div class="app-layout">
    <GlobalHeader @search="handleSearch" />
    <div class="app-body">
      <SideNav />
      <main class="main-content">
        <router-view v-slot="{ Component }">
          <component :is="Component" />
        </router-view>
      </main>
    </div>
    <DetailDrawer
      v-model="drawerVisible"
      :type="drawerType"
      :data="drawerData"
      @refresh="handleRefresh"
      @open-add-os="openAddOsDialog"
      @open-edit-os="openEditOsDialog"
      @open-edit-service="openEditServiceDialog"
    />

    <!-- 添加系统对话框 -->
    <el-dialog v-model="showAddOsDialog" title="添加系统" width="500px">
      <el-form label-width="80px">
        <el-form-item label="系统名称" required>
          <el-input v-model="osForm.name" placeholder="如 OpenWrt-主路由" />
        </el-form-item>
        <el-form-item label="系统类型" required>
          <el-select v-model="osForm.os_type" placeholder="选择类型" style="width: 100%">
            <el-option v-for="t in osTypeOptions" :key="t?.name || t?.id" :label="t?.name || '未知'" :value="t?.name || ''" />
          </el-select>
        </el-form-item>
        <el-form-item label="父系统">
          <el-select v-model="osForm.parent_os_id" placeholder="无（顶级系统）" clearable style="width: 100%">
            <el-option v-for="h in hostOptions" :key="h.id" :label="h.name + ' (Host)'" :value="h.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="IP地址">
          <el-input v-model="osForm.ip_address" placeholder="如 192.168.1.1" />
        </el-form-item>
        <el-form-item label="MAC地址">
          <el-input v-model="osForm.mac_address" placeholder="如 00:00:00:00:00:00" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="osForm.notes" type="textarea" rows="2" placeholder="备注信息" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddOsDialog = false">取消</el-button>
        <el-button type="primary" @click="saveOsInstance">保存</el-button>
      </template>
    </el-dialog>

    <!-- 编辑系统对话框 -->
    <el-dialog v-model="showEditOsDialog" title="编辑系统" width="500px">
      <el-form label-width="80px">
        <el-form-item label="系统名称" required>
          <el-input v-model="editOsForm.name" placeholder="如 OpenWrt-主路由" />
        </el-form-item>
        <el-form-item label="系统类型" required>
          <el-select v-model="editOsForm.os_type" placeholder="选择类型" style="width: 100%">
            <el-option v-for="t in osTypeOptions" :key="t?.name || t?.id" :label="t?.name || '未知'" :value="t?.name || ''" />
          </el-select>
        </el-form-item>
        <el-form-item label="父系统">
          <el-select v-model="editOsForm.parent_os_id" placeholder="无（顶级系统）" clearable style="width: 100%">
            <el-option v-for="h in editHostOptions" :key="h.id" :label="h.name + ' (Host)'" :value="h.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="IP地址">
          <el-input v-model="editOsForm.ip_address" placeholder="如 192.168.1.1" />
        </el-form-item>
        <el-form-item label="MAC地址">
          <el-input v-model="editOsForm.mac_address" placeholder="如 00:00:00:00:00:00" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="editOsForm.notes" type="textarea" rows="2" placeholder="备注信息" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditOsDialog = false">取消</el-button>
        <el-button type="primary" @click="saveEditOsInstance">保存</el-button>
      </template>
    </el-dialog>

    <!-- 编辑服务对话框 -->
    <el-dialog v-model="showEditServiceDialog" title="编辑服务" width="500px">
      <el-form label-width="80px">
        <el-form-item label="服务名" required>
          <el-input v-model="editServiceForm.name" placeholder="如 HomeAssistant" />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="editServiceForm.type" placeholder="选择类型" style="width:100%" clearable>
            <el-option v-for="t in serviceTypeOptions" :key="t?.name" :label="t?.name" :value="t?.name" />
          </el-select>
        </el-form-item>
        <el-form-item label="协议">
          <el-select v-model="editServiceForm.protocol" placeholder="选择协议" style="width:100%">
            <el-option v-for="p in protocolOptions" :key="p?.name" :label="p?.name?.toUpperCase()" :value="p?.name" />
          </el-select>
        </el-form-item>
        <el-form-item label="IP地址">
          <el-input v-model="editServiceForm.ip_address" placeholder="如 192.168.1.50" />
        </el-form-item>
        <el-form-item label="端口">
          <el-input-number v-model="editServiceForm.port" :min="1" :max="65535" />
        </el-form-item>
        <el-form-item label="宿主" required>
          <el-select v-model="editServiceForm.osInstanceId" placeholder="选择宿主系统" style="width:100%">
            <el-option v-for="os in store.state.allOsInstances" :key="os?.id" :label="os?.name + ' (' + os?.computerName + ')'" :value="os?.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="editServiceForm.description" type="textarea" rows="2" placeholder="服务描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditServiceDialog = false">取消</el-button>
        <el-button type="primary" @click="saveEditService">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, provide, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import GlobalHeader from './components/GlobalHeader.vue'
import SideNav from './components/SideNav.vue'
import DetailDrawer from './components/DetailDrawer.vue'
import { createAppStore } from './stores/app'

const store = createAppStore()

// Initialize data on mount
onMounted(async () => {
  console.log('App mounted, loading data...')
  await store.loadData()
  console.log('Data loaded. typeConfigs:', store.state.typeConfigs)
  console.log('osTypeConfigs:', store.osTypeConfigs)
})

// Drawer state
const drawerVisible = ref(false)
const drawerType = ref('')
const drawerData = ref(null)

// 添加系统对话框状态
const showAddOsDialog = ref(false)
const osForm = ref({
  name: '',
  os_type: '',
  ip_address: '',
  mac_address: '',
  notes: ''
})
const addOsTargetComputerId = ref(null)

// 编辑系统对话框状态
const showEditOsDialog = ref(false)
const editOsForm = ref({
  id: null,
  name: '',
  os_type: '',
  parent_os_id: null,
  ip_address: '',
  mac_address: '',
  notes: ''
})
const editOsTargetComputerId = ref(null)

// 编辑服务对话框状态
const showEditServiceDialog = ref(false)
const editServiceForm = ref({
  id: null,
  name: '',
  type: '',
  protocol: 'http',
  ip_address: '',
  port: 80,
  osInstanceId: null,
  description: ''
})

const osTypeOptions = computed(() => {
  const configs = store.osTypeConfigs
  console.log('osTypeOptions computed, store.osTypeConfigs:', configs)
  if (Array.isArray(configs)) return configs
  if (configs?.value && Array.isArray(configs.value)) return configs.value
  return []
})

const hostOptions = computed(() => {
  if (!addOsTargetComputerId.value) return []
  return store.getHostOsInstances(addOsTargetComputerId.value)
})

const editHostOptions = computed(() => {
  if (!editOsTargetComputerId.value) return []
  return store.getHostOsInstances(editOsTargetComputerId.value)
})

const protocolOptions = computed(() => {
  const configs = store.protocolConfigs
  if (!configs) return []
  return Array.isArray(configs) ? configs : (configs.value || [])
})

const serviceTypeOptions = computed(() => {
  const configs = store.serviceTypeConfigs
  if (!configs) return []
  return Array.isArray(configs) ? configs : (configs.value || [])
})

const openDrawer = (type, data) => {
  drawerType.value = type
  drawerData.value = data
  drawerVisible.value = true
}

const handleRefresh = () => {
  store.loadData()
}

const handleSearch = ({ type, data }) => {
  if (type === 'computer') {
    openDrawer('computer', store.state.computers.find(c => c.id === data.id) || data)
  } else if (type === 'os_instance') {
    openDrawer('os_instance', store.getOsInstanceById(data.id) || data)
  } else if (type === 'service') {
    openDrawer('service', data)
  } else if (type === 'cpu' || type === 'ram' || type === 'disk') {
    if (data.computerId) {
      openDrawer('computer', store.state.computers.find(c => c.id === data.computerId) || { id: data.computerId })
    } else {
      ElMessage.info('该硬件未分配到任何主机')
    }
  }
}

// 添加系统相关
const openAddOsDialog = (computerId) => {
  console.log('openAddOsDialog called with:', computerId)
  addOsTargetComputerId.value = computerId
  osForm.value = {
    name: '',
    os_type: 'Linux',
    parent_os_id: null,
    ip_address: '',
    mac_address: '',
    notes: ''
  }
  showAddOsDialog.value = true
}

// 编辑系统相关
const openEditOsDialog = (osData) => {
  editOsTargetComputerId.value = osData.computerId
  editOsForm.value = {
    id: osData.id,
    name: osData.name,
    os_type: osData.type,
    parent_os_id: osData.parentOsId,
    ip_address: osData.ipAddress || '',
    mac_address: osData.macAddress || '',
    notes: osData.notes || ''
  }
  showEditOsDialog.value = true
}

// 编辑服务相关
const openEditServiceDialog = (serviceData) => {
  editServiceForm.value = {
    id: serviceData.id,
    name: serviceData.name,
    type: serviceData.type || '',
    protocol: serviceData.protocol || 'http',
    ip_address: serviceData.ip_address || '',
    port: serviceData.port || 80,
    osInstanceId: serviceData.osInstanceId,
    description: serviceData.description || ''
  }
  showEditServiceDialog.value = true
}

const saveOsInstance = async () => {
  if (!osForm.value.name || !osForm.value.os_type) {
    ElMessage.warning('请填写名称和类型')
    return
  }
  if (!addOsTargetComputerId.value) {
    ElMessage.error('未指定主机')
    return
  }
  try {
    await store.saveOsInstance(addOsTargetComputerId.value, osForm.value)
    showAddOsDialog.value = false
    handleRefresh()
    ElMessage.success('添加成功')
  } catch (e) {
    ElMessage.error('添加失败')
  }
}

const saveEditOsInstance = async () => {
  if (!editOsForm.value.name || !editOsForm.value.os_type) {
    ElMessage.warning('请填写名称和类型')
    return
  }
  try {
    await store.updateOsInstance(editOsForm.value.id, editOsForm.value)
    showEditOsDialog.value = false
    handleRefresh()
    ElMessage.success('保存成功')
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

const saveEditService = async () => {
  if (!editServiceForm.value.name || !editServiceForm.value.osInstanceId) {
    ElMessage.warning('请填写服务名和选择宿主系统')
    return
  }
  try {
    await store.saveService(editServiceForm.value.osInstanceId, {
      name: editServiceForm.value.name,
      type: editServiceForm.value.type,
      protocol: editServiceForm.value.protocol,
      ip_address: editServiceForm.value.ip_address,
      port: editServiceForm.value.port,
      osInstanceId: editServiceForm.value.osInstanceId,
      description: editServiceForm.value.description
    }, editServiceForm.value.id)
    showEditServiceDialog.value = false
    handleRefresh()
    ElMessage.success('保存成功')
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

// Provide openDrawer to child components
provide('openDrawer', openDrawer)
</script>

<style>
/* Global styles */
html, body {
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
}

#app {
  height: 100%;
  width: 100%;
}

* {
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  background-color: #f5f7fa;
}
</style>

<style scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
  overflow: hidden;
}

.app-body {
  display: flex;
  flex: 1;
  overflow: hidden;
  min-height: 0; /* Important for flex child to shrink */
}

.main-content {
  flex: 1 1 auto;
  overflow-y: auto;
  overflow-x: hidden;
  background: #f5f7fa;
  padding: 20px;
  min-width: 0; /* Allow shrinking */
}
</style>
