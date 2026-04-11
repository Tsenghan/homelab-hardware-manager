<template>
  <div class="service-list">
    <div class="view-header">
      <h2 class="page-title">
        服务列表
        <el-input v-model="filterText" placeholder="搜索服务..." clearable style="width: 200px; margin-left: 16px">
          <template #prefix><el-icon><Search /></el-icon></template>
        </el-input>
      </h2>
      <el-button type="primary" @click="openAddDialog">
        <el-icon><Plus /></el-icon>
        添加服务
      </el-button>
    </div>

    <div class="service-table">
      <el-table :data="filteredServices" stripe style="width: 100%" @row-click="handleRowClick">
        <template #empty>
           <el-empty description="暂无服务" />
        </template>
        <el-table-column label="服务名" min-width="120">
          <template #header>
            <span class="th-sortable" @click="handleSort('name')">
              服务名 <span class="th-sort-icon">{{ sortState.prop === 'name' ? (sortState.order === 'asc' ? '↑' : '↓') : '' }}</span>
            </span>
          </template>
          <template #default="{ row }">
            {{ row.name }}
          </template>
        </el-table-column>
        <el-table-column label="类型" width="100" align="center">
          <template #header>
            <span class="th-sortable" @click="handleSort('type')">
              类型 <span class="th-sort-icon">{{ sortState.prop === 'type' ? (sortState.order === 'asc' ? '↑' : '↓') : '' }}</span>
            </span>
          </template>
          <template #default="{ row }">
            <el-tag v-if="row.type" size="small" :type="serviceTypeColorMap[row.type] || 'info'">
              {{ row.type }}
            </el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="协议" width="110" align="center">
          <template #header>
            <span class="th-sortable" @click="handleSort('protocol')">
              协议 <span class="th-sort-icon">{{ sortState.prop === 'protocol' ? (sortState.order === 'asc' ? '↑' : '↓') : '' }}</span>
            </span>
          </template>
          <template #default="{ row }">
            <el-tag size="small" :type="row.protocol === 'https' ? 'success' : 'info'">
              {{ row.protocol?.toUpperCase() }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="地址" min-width="130">
          <template #header>
            <span class="th-sortable" @click="handleSort('ip_address')">
              地址 <span class="th-sort-icon">{{ sortState.prop === 'ip_address' ? (sortState.order === 'asc' ? '↑' : '↓') : '' }}</span>
            </span>
          </template>
          <template #default="{ row }">
            <span class="mono">{{ row.ip_address }}:{{ row.port }}</span>
          </template>
        </el-table-column>
        <el-table-column label="宿主系统" min-width="120">
          <template #header>
            <span class="th-sortable" @click="handleSort('osInstanceId')">
              宿主系统 <span class="th-sort-icon">{{ sortState.prop === 'osInstanceId' ? (sortState.order === 'asc' ? '↑' : '↓') : '' }}</span>
            </span>
          </template>
          <template #default="{ row }">
            {{ osInstanceNameCache[row.osInstanceId] || '未知' }}
          </template>
        </el-table-column>
        <el-table-column label="描述" min-width="150">
          <template #header>
            <span class="th-sortable" @click="handleSort('description')">
              描述 <span class="th-sort-icon">{{ sortState.prop === 'description' ? (sortState.order === 'asc' ? '↑' : '↓') : '' }}</span>
            </span>
          </template>
          <template #default="{ row }">
            {{ row.description || ' ' }}
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- Service Dialog -->
    <el-dialog v-model="showDialog" :title="editingService ? '编辑服务' : '添加服务'" width="500px">
      <el-form label-width="80px">
        <el-form-item label="服务名" required>
          <el-input v-model="form.name" placeholder="如 HomeAssistant" />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="form.type" placeholder="选择类型" style="width:100%" clearable>
            <el-option v-for="t in serviceTypeOptions" :key="t?.name" :label="t?.name" :value="t?.name" />
          </el-select>
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
import { ref, computed, inject } from 'vue'
import { Plus, Search, Link, Edit, Delete } from '@element-plus/icons-vue'
import { useAppStore } from '../stores/app'
import { ElMessage, ElMessageBox } from 'element-plus'

const store = useAppStore()
const openDrawer = inject('openDrawer')

const filterText = ref('')
const showDialog = ref(false)
const editingService = ref(null)

// 排序状态
const sortState = ref({ prop: 'name', order: 'asc' })

// 排序处理
const handleSort = (prop) => {
  if (sortState.value.prop === prop) {
    sortState.value.order = sortState.value.order === 'asc' ? 'desc' : 'asc'
  } else {
    sortState.value.prop = prop
    sortState.value.order = 'asc'
  }
}

const form = ref({
  id: null,
  name: '',
  type: '',
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

const serviceTypeOptions = computed(() => {
  const configs = store.serviceTypeConfigs
  if (!configs) return []
  return Array.isArray(configs) ? configs : (configs.value || [])
})

// 服务类型颜色映射，O(1) 查找
const serviceTypeColorMap = computed(() => {
  const map = {}
  const colorMap = { '#67C23A': 'success', '#409EFF': '', '#E6A23C': 'warning', '#F56C6C': 'danger', '#909399': 'info' }
  const configs = store.state.typeConfigs || []
  configs.forEach(t => {
    if (t.category === 'service_type') {
      map[t.name] = colorMap[t.color] || 'info'
    }
  })
  return map
})

// 宿主系统名称缓存，用普通对象避免响应式开销
const osInstanceNameCache = computed(() => {
  const cache = {}
  store.state.allOsInstances.forEach(os => {
    cache[os.id] = os.name || '未知'
  })
  return cache
})

const filteredServices = computed(() => {
  let result = store.state.services || []
  const osCache = osInstanceNameCache.value

  // 过滤
  if (filterText.value) {
    const q = filterText.value.toLowerCase()
    result = result.filter(s =>
      s.name?.toLowerCase().includes(q) ||
      (s.ip_address && s.ip_address.includes(q))
    )
  }

  // 排序：预处理 sortValue，避免在比较器中重复计算
  const { prop, order } = sortState.value
  if (prop && order) {
    const isAsc = order === 'asc'

    const mapped = result.map(item => {
      let sortValue = item[prop] || ''

      if (prop === 'osInstanceId') {
        sortValue = osCache[item.osInstanceId] || ''
      } else if (prop === 'ip_address') {
        sortValue = item.ip_address ? Number(item.ip_address.slice(item.ip_address.lastIndexOf('.') + 1)) : 0
      }

      if (typeof sortValue === 'string') {
        sortValue = sortValue.toLowerCase()
      }

      return { original: item, sortValue }
    })

    mapped.sort((a, b) => {
      if (a.sortValue < b.sortValue) return isAsc ? -1 : 1
      if (a.sortValue > b.sortValue) return isAsc ? 1 : -1
      return 0
    })

    result = mapped.map(item => item.original)
  }

  return result
})

const handleRowClick = (row) => {
  openDrawer('service', row)
}

const openServiceUrl = (s) => {
  window.open(`${s.protocol}://${s.ip_address}:${s.port}`, '_blank')
}

const openAddDialog = () => {
  editingService.value = null
  form.value = {
    id: null,
    name: '',
    type: '',
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
  form.value = {
    id: s.id,
    name: s.name,
    type: s.type || '',
    protocol: s.protocol || 'http',
    ip_address: s.ip_address || '',
    port: s.port || 80,
    osInstanceId: s.osInstanceId,
    description: s.description || ''
  }
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

/* 确保标题和按钮对齐，虽然你可能在全局写了，但局部再稳固一下 */
.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  display: flex;
  align-items: center;
}

.filter-bar {
  display: flex;
  margin-bottom: 16px;
}

/* --- 表格容器质感提升 --- */
.service-table {
  background: var(--bg-white);
  border: 1px solid var(--border-color); /* 保留极细边框 */
  border-radius: var(--radius-lg);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04); /* ✨ 新增：增加非常柔和的阴影，产生呼吸感 */
  overflow: hidden;
}

/* --- Element Plus 表格深度美化 --- */
:deep(.el-table) {
  --el-table-border-color: var(--border-light, #ebeef5); /* 统一内边框颜色 */
  --el-table-header-bg-color: #f8fafc; /* ✨ 新增：给表头加一个极浅的灰蓝色背景，区分层级 */
}

/* 去掉 el-table 底部默认的那条丑陋的白线/灰线伪元素 */
:deep(.el-table::before) {
  display: none;
}

/* 让斑马纹的颜色更柔和一点 (可选) */
:deep(.el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell) {
  background-color: #fafafa;
}

/* --- 数据展示排版 --- */
.mono {
  font-family: var(--font-mono, ui-monospace, SFMono-Regular, Consolas, monospace);
  font-size: 0.8125rem;
  /* ✨ 优化：不再用刺眼的亮蓝，改用专业代码块风格 */
  color: #334155;
  background-color: #f1f5f9;
  padding: 3px 6px;
  border-radius: 4px;
  border: 1px solid #e2e8f0;
}

.th-sortable {
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.th-sortable:hover {
  color: var(--primary-color, #409eff);
}

.th-sort-icon {
  font-size: 10px;
}

.action-btns {
  display: flex;
  align-items: center;
  gap: 4px; /* ✨ 核心：这个值越小，按钮靠得越近，建议用 2px 或 4px */
}

/* ✨ 必须加上这行：强制干掉 Element Plus 按钮默认的左边距 */
.action-btns .el-button + .el-button {
  margin-left: 0 !important; 
}

/* (可选) 如果你觉得按钮本身的内边距也太宽，可以加上下面这行把按钮捏瘦一点 */
.action-btns .el-button {
  padding: 4px 6px; 
}
/* --- 修复操作列 Primary 文本按钮颜色 --- */
.action-btns .el-button--primary.is-text {
  color: var(--primary-bg, #f8fafc) !important; /* 强制文字为主色（蓝色） */
  background-color: var(--primary-color, #409EFF) !important;        /* 强制背景透明 */
}

/* 修复悬停时的对比度问题 */
.action-btns .el-button--primary.is-text:hover {
  /* 悬停时给一个极浅的蓝色背景，保持高对比度 */
  background-color: var(--el-color-primary-light-9, #ecf5ff) !important; 
  color: var(--primary-color, #409EFF) !important;
}

/* 顺便修复一下普通编辑/删除按钮的悬停底色，让它们统一 */
.action-btns .el-button.is-text:not(.el-button--primary):hover {
  background-color: var(--bg-gray-50, #f3f4f6) !important;
  color: var(--text-primary, #303133) !important;
}
</style>