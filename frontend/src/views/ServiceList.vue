<template>
  <div class="service-list">
    <div class="view-header">
      <h2 class="page-title">服务列表</h2>
      <el-button type="primary" @click="openAddDialog">
        <el-icon><Plus /></el-icon>
        添加服务
      </el-button>
    </div>

    <div class="filter-bar">
      <el-input v-model="filterText" placeholder="搜索服务..." clearable style="width: 300px">
        <template #prefix><el-icon><Search /></el-icon></template>
      </el-input>
    </div>

    <div class="service-table">
      <el-table :data="filteredServices" stripe style="width: 100%">
        <el-table-column label="服务名" prop="name" min-width="150" />
        <el-table-column label="协议" width="80">
          <template #default="{ row }">
            <el-tag size="small" :type="row.protocol === 'https' ? 'success' : 'info'">
              {{ row.protocol?.toUpperCase() }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="地址" min-width="200">
          <template #default="{ row }">
            <span class="mono">{{ row.ip_address }}:{{ row.port }}</span>
          </template>
        </el-table-column>
        <el-table-column label="宿主系统" min-width="150">
          <template #default="{ row }">
            {{ getOsInstanceName(row.osInstanceId) }}
          </template>
        </el-table-column>
        <el-table-column label="描述" min-width="150">
          <template #default="{ row }">
            {{ row.description || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" text @click="openServiceUrl(row)">
              <el-icon><Link /></el-icon> 打开
            </el-button>
            <el-button size="small" type="primary" text @click="editService(row)">
              <el-icon><Edit /></el-icon> 编辑
            </el-button>
            <el-button size="small" type="danger" text @click="confirmDelete(row)">
              <el-icon><Delete /></el-icon> 删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="filteredServices.length === 0" description="暂无服务" />
    </div>

    <!-- Service Dialog -->
    <el-dialog v-model="showDialog" :title="editingService ? '编辑服务' : '添加服务'" width="500px">
      <el-form label-width="80px">
        <el-form-item label="服务名" required>
          <el-input v-model="form.name" placeholder="如 HomeAssistant" />
        </el-form-item>
        <el-form-item label="协议">
          <el-select v-model="form.protocol" placeholder="选择协议" style="width:100%">
            <el-option v-for="p in protocolOptions" :key="p?.name" :label="p?.name?.toUpperCase()" :value="p?.name" />
          </el-select>
        </el-form-item>
        <el-form-item label="IP地址">
          <el-input v-model="form.ip_address" placeholder="如 192.168.1.50" />
        </el-form-item>
        <el-form-item label="端口">
          <el-input-number v-model="form.port" :min="1" :max="65535" />
        </el-form-item>
        <el-form-item label="宿主" required>
          <el-select v-model="form.osInstanceId" placeholder="选择宿主系统" style="width:100%">
            <el-option v-for="os in store.state.allOsInstances" :key="os?.id" :label="os?.name + ' (' + os?.computerName + ')'" :value="os?.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" rows="2" placeholder="服务描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="saveService">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Plus, Search, Link, Edit, Delete } from '@element-plus/icons-vue'
import { useAppStore } from '../stores/app'
import { ElMessage, ElMessageBox } from 'element-plus'

const store = useAppStore()

const filterText = ref('')
const showDialog = ref(false)
const editingService = ref(null)

const form = ref({
  id: null,
  name: '',
  protocol: 'http',
  ip_address: '',
  port: 80,
  osInstanceId: null,
  description: ''
})

const protocolOptions = computed(() => {
  const configs = store.protocolConfigs
  if (!configs) return []
  return Array.isArray(configs) ? configs : (configs.value || [])
})

const filteredServices = computed(() => {
  if (!filterText.value) return store.state.services
  const q = filterText.value.toLowerCase()
  return store.state.services.filter(s =>
    s.name?.toLowerCase().includes(q) ||
    (s.ip_address && s.ip_address.includes(q))
  )
})

const getOsInstanceName = (id) => {
  return store.getOsInstanceName(id)
}

const openServiceUrl = (s) => {
  window.open(`${s.protocol}://${s.ip_address}:${s.port}`, '_blank')
}

const openAddDialog = () => {
  editingService.value = null
  form.value = {
    id: null,
    name: '',
    protocol: 'http',
    ip_address: '',
    port: 80,
    osInstanceId: null,
    description: ''
  }
  showDialog.value = true
}

const editService = (s) => {
  editingService.value = s
  form.value = { ...s }
  showDialog.value = true
}

const saveService = async () => {
  if (!form.value.name || !form.value.osInstanceId) {
    ElMessage.warning('请填写服务名和选择宿主系统')
    return
  }
  try {
    await store.saveService(form.value.osInstanceId, form.value, editingService.value?.id)
    showDialog.value = false
    editingService.value = null
    store.loadData()
    ElMessage.success('保存成功')
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

const confirmDelete = (s) => {
  ElMessageBox.confirm(`确定要删除服务 "${s.name}" 吗?`, '确认删除', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await store.deleteService(s.id)
      store.loadData()
      ElMessage.success('删除成功')
    } catch (e) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}
</script>

<style scoped>
.service-list {
  padding: 0;
}

.filter-bar {
  display: flex;
  margin-bottom: 16px;
}

.service-table {
  background: var(--bg-white);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.mono {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  color: var(--primary-color);
}
</style>