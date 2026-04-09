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
        <el-form-item label="IP地址">
          <el-input v-model="osForm.ip_address" placeholder="如 192.168.1.1" />
        </el-form-item>
        <el-form-item label="端口">
          <el-input-number v-model="osForm.port" :min="1" :max="65535" placeholder="端口" style="width: 100%" />
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
  port: null,
  mac_address: '',
  notes: ''
})
const addOsTargetComputerId = ref(null)

const osTypeOptions = computed(() => {
  const configs = store.osTypeConfigs
  console.log('osTypeOptions computed, store.osTypeConfigs:', configs)
  if (Array.isArray(configs)) return configs
  if (configs?.value && Array.isArray(configs.value)) return configs.value
  return []
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
  } else if (type === 'cpu') {
    openDrawer('computer', store.state.computers.find(c => c.id === data.computerId) || { id: data.computerId })
  }
}

// 添加系统相关
const openAddOsDialog = (computerId) => {
  console.log('openAddOsDialog called with:', computerId)
  addOsTargetComputerId.value = computerId
  osForm.value = {
    name: '',
    os_type: 'Linux',
    ip_address: '',
    port: null,
    mac_address: '',
    notes: ''
  }
  showAddOsDialog.value = true
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
