<template>
  <div class="settings-view">
    <div class="view-header">
      <h2 class="page-title">配置管理</h2>
      <div class="header-actions">
        <el-button @click="handleExport">
          <el-icon><Download /></el-icon> 导出
        </el-button>
        <el-button type="primary" @click="triggerImport">
          <el-icon><Upload /></el-icon> 导入
        </el-button>
        <input ref="fileInput" type="file" accept=".json" style="display:none" @change="handleImport" />
      </div>
    </div>
    <div class="settings-container">
    <!-- OS类型配置 -->
    <div class="settings-section">
      <div class="section-header">
        <span class="settings-section-title">操作系统类型</span>
        <el-button type="primary" size="small" @click="showAddOsDialog = true">
          <el-icon><Plus /></el-icon> 添加
        </el-button>
      </div>
      <div class="tag-list">
        <el-tag
          v-for="item in osTypeList"
          :key="item.id"
          closable
          :style="{ backgroundColor: item.color, borderColor: item.color, color: '#fff' }"
          @click="openEditDialog(item, 'os_type')"
          @close="confirmDeleteType(item)"
        >
          {{ item.name }}
        </el-tag>
      </div>
    </div>

    <!-- 服务协议配置 -->
    <div class="settings-section">
      <div class="section-header">
        <span class="settings-section-title">服务协议</span>
        <el-button type="primary" size="small" @click="showAddProtocolDialog = true">
          <el-icon><Plus /></el-icon> 添加
        </el-button>
      </div>
      <div class="tag-list">
        <el-tag
          v-for="item in protocolList"
          :key="item.id"
          closable
          :style="{ backgroundColor: item.color, borderColor: item.color, color: '#fff' }"
          @click="openEditDialog(item, 'protocol')"
          @close="confirmDeleteType(item)"
        >
          {{ item.name }}
        </el-tag>
      </div>
    </div>

    <!-- 服务类型配置 -->
    <div class="settings-section">
      <div class="section-header">
        <span class="settings-section-title">服务类型</span>
        <el-button type="primary" size="small" @click="showAddServiceTypeDialog = true">
          <el-icon><Plus /></el-icon> 添加
        </el-button>
      </div>
      <div class="tag-list">
        <el-tag
          v-for="item in serviceTypeList"
          :key="item.id"
          closable
          :style="{ backgroundColor: item.color, borderColor: item.color, color: '#fff' }"
          @click="openEditDialog(item, 'service_type')"
          @close="confirmDeleteType(item)"
        >
          {{ item.name }}
        </el-tag>
      </div>
    </div>
    </div>

    <!-- Edit Tag Dialog -->
    <el-dialog v-model="showEditDialog" title="编辑配置" width="400px">
      <el-form label-width="80px">
        <el-form-item label="名称" required>
          <el-input v-model="editForm.name" placeholder="名称" />
        </el-form-item>
        <el-form-item label="颜色">
          <el-color-picker v-model="editForm.color" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="saveEdit">保存</el-button>
      </template>
    </el-dialog>

    <!-- Add OS Type Dialog -->
    <el-dialog v-model="showAddOsDialog" title="添加操作系统类型" width="400px">
      <el-form label-width="80px">
        <el-form-item label="名称" required>
          <el-input v-model="newOsType.name" placeholder="如 Ubuntu" />
        </el-form-item>
        <el-form-item label="颜色">
          <el-color-picker v-model="newOsType.color" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddOsDialog = false">取消</el-button>
        <el-button type="primary" @click="addType('os_type')">添加</el-button>
      </template>
    </el-dialog>

    <!-- Add Protocol Dialog -->
    <el-dialog v-model="showAddProtocolDialog" title="添加服务协议" width="400px">
      <el-form label-width="80px">
        <el-form-item label="名称" required>
          <el-input v-model="newProtocol.name" placeholder="如 http" />
        </el-form-item>
        <el-form-item label="颜色">
          <el-color-picker v-model="newProtocol.color" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddProtocolDialog = false">取消</el-button>
        <el-button type="primary" @click="addType('protocol')">添加</el-button>
      </template>
    </el-dialog>

    <!-- Add Service Type Dialog -->
    <el-dialog v-model="showAddServiceTypeDialog" title="添加服务类型" width="400px">
      <el-form label-width="80px">
        <el-form-item label="名称" required>
          <el-input v-model="newServiceType.name" placeholder="如 Web服务" />
        </el-form-item>
        <el-form-item label="颜色">
          <el-color-picker v-model="newServiceType.color" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddServiceTypeDialog = false">取消</el-button>
        <el-button type="primary" @click="addType('service_type')">添加</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Plus, Upload, Download } from '@element-plus/icons-vue'
import { useAppStore } from '../stores/app'
import { ElMessage, ElMessageBox } from 'element-plus'

const store = useAppStore()
const fileInput = ref(null)

const showAddOsDialog = ref(false)
const showAddProtocolDialog = ref(false)
const showAddServiceTypeDialog = ref(false)
const showEditDialog = ref(false)
const editingItem = ref(null)
const editForm = ref({ name: '', color: '#409EFF' })

const newOsType = ref({ name: '', color: '#409EFF' })
const newProtocol = ref({ name: '', color: '#409EFF' })
const newServiceType = ref({ name: '', color: '#409EFF' })

const triggerImport = () => {
  fileInput.value.click()
}

const handleExport = () => {
  store.exportData()
}

const handleImport = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  try {
    await store.importData(file)
    ElMessage.success('导入成功')
  } catch (e) {
    ElMessage.error('导入失败: ' + e.message)
  }
  event.target.value = ''
}

const osTypeList = computed(() =>
  store.state.typeConfigs.filter(t => t.category === 'os_type')
)

const protocolList = computed(() =>
  store.state.typeConfigs.filter(t => t.category === 'protocol')
)

const serviceTypeList = computed(() =>
  store.state.typeConfigs.filter(t => t.category === 'service_type')
)

const addType = async (category) => {
  let form
  if (category === 'os_type') {
    form = newOsType.value
  } else if (category === 'protocol') {
    form = newProtocol.value
  } else {
    form = newServiceType.value
  }

  if (!form.name.trim()) {
    ElMessage.warning('请输入名称')
    return
  }

  try {
    await store.addTypeConfig(category, form.name.trim(), form.color)
    form.name = ''
    form.color = '#409EFF'
    if (category === 'os_type') {
      showAddOsDialog.value = false
    } else if (category === 'protocol') {
      showAddProtocolDialog.value = false
    } else {
      showAddServiceTypeDialog.value = false
    }
    ElMessage.success('添加成功')
  } catch (e) {
    ElMessage.error('添加失败')
  }
}

const openEditDialog = (item, category) => {
  editingItem.value = item
  editForm.value = { name: item.name, color: item.color }
  showEditDialog.value = true
}

const saveEdit = async () => {
  if (!editForm.value.name.trim()) {
    ElMessage.warning('请输入名称')
    return
  }
  try {
    await store.updateTypeConfig(editingItem.value.id, { name: editForm.value.name.trim(), color: editForm.value.color })
    showEditDialog.value = false
    ElMessage.success('保存成功')
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

const confirmDeleteType = (item) => {
  ElMessageBox.confirm(`确定要删除 "${item.name}" 吗?`, '确认删除', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await store.deleteTypeConfig(item.id)
      ElMessage.success('删除成功')
    } catch (e) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}
</script>

<style scoped>
.settings-view {
  padding: 0;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.view-header {
  margin-bottom: 24px;
}

/* --- ✨ 核心重构：双列响应式网格 --- */
/* 屏幕宽时左右并排，屏幕窄时自动上下堆叠 */
.settings-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 24px;
  align-items: start; /* 防止左右两个卡片因为内容不一样高而被强制拉伸 */
}

/* --- 卡片质感 --- */
.settings-section {
  background: var(--bg-white, #ffffff);
  padding: 20px;
  border-radius: var(--radius-lg, 12px);
  border: 1px solid var(--border-light, #e4e7ed);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.03); /* 统一呼吸感阴影 */
  transition: box-shadow 0.3s ease;
}

.settings-section:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
}

/* --- 卡片头部与标题 --- */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-light, #ebeef5); /* 增加一条浅色分隔线 */
}

.settings-section-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  display: flex;
  align-items: center;
}

/* ✨ 给标题加个左侧主色小点缀，呼应之前拓扑图的设计 */
.settings-section-title::before {
  content: '';
  display: inline-block;
  width: 4px;
  height: 16px;
  background: var(--primary-color, #409eff);
  border-radius: 2px;
  margin-right: 8px;
}

/* 修改颜色选择器的对齐问题 */
:deep(.el-color-picker) {
  vertical-align: middle;
}

/* 去除颜色选择器的边框 */
:deep(.el-color-picker__trigger) {
  border: none !important;
  padding: 0;
}

:deep(.el-color-picker__color) {
  border: none !important;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-list .el-tag {
  cursor: pointer;
  padding: 6px 12px;
  font-size: 0.8125rem;
  transition: transform 0.15s, opacity 0.15s;
}

.tag-list .el-tag:hover {
  transform: translateY(-1px);
  opacity: 0.9;
}

:deep(.el-tag--success) {
  --el-tag-success-bg-color: #67c23a;
  --el-tag-success-border-color: #67c23a;
  --el-tag-success-text-color: #fff;
}

:deep(.el-tag--warning) {
  --el-tag-warning-bg-color: #e6a23c;
  --el-tag-warning-border-color: #e6a23c;
  --el-tag-warning-text-color: #fff;
}

:deep(.el-tag--danger) {
  --el-tag-danger-bg-color: #f56c6c;
  --el-tag-danger-border-color: #f56c6c;
  --el-tag-danger-text-color: #fff;
}

:deep(.el-tag--info) {
  --el-tag-info-bg-color: #909399;
  --el-tag-info-border-color: #909399;
  --el-tag-info-text-color: #fff;
}
</style>