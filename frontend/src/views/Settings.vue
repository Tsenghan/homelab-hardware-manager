<template>
  <div class="settings-view">
    <h2 class="page-title">配置管理</h2>
    <div class="settings-container">
    <!-- OS类型配置 -->
    <div class="settings-section">
      <div class="section-header">
        <span class="settings-section-title">操作系统类型</span>
        <el-button type="primary" size="small" @click="showAddOsDialog = true">
          <el-icon><Plus /></el-icon> 添加
        </el-button>
      </div>

      <el-table :data="osTypeList" stripe style="width: 100%">
        <el-table-column label="颜色" width="80">
          <template #default="{ row }">
            <el-color-picker v-model="row.color" size="small" @change="updateTypeConfig(row)" />
          </template>
        </el-table-column>
        <el-table-column label="名称" prop="name" />
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="danger" text @click="confirmDeleteType(row)">
              <el-icon><Delete /></el-icon> 删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 服务协议配置 -->
    <div class="settings-section">
      <div class="section-header">
        <span class="settings-section-title">服务协议</span>
        <el-button type="primary" size="small" @click="showAddProtocolDialog = true">
          <el-icon><Plus /></el-icon> 添加
        </el-button>
      </div>

      <el-table :data="protocolList" stripe style="width: 100%">
        <el-table-column label="颜色" width="80">
          <template #default="{ row }">
            <el-color-picker v-model="row.color" size="small" @change="updateTypeConfig(row)" />
          </template>
        </el-table-column>
        <el-table-column label="名称" prop="name" />
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="danger" text @click="confirmDeleteType(row)">
              <el-icon><Delete /></el-icon> 删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    </div>

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
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Plus, Delete } from '@element-plus/icons-vue'
import { useAppStore } from '../stores/app'
import { ElMessage, ElMessageBox } from 'element-plus'

const store = useAppStore()

const showAddOsDialog = ref(false)
const showAddProtocolDialog = ref(false)

const newOsType = ref({ name: '', color: '#409EFF' })
const newProtocol = ref({ name: '', color: '#409EFF' })

const osTypeList = computed(() =>
  store.state.typeConfigs.filter(t => t.category === 'os_type')
)

const protocolList = computed(() =>
  store.state.typeConfigs.filter(t => t.category === 'protocol')
)

const addType = async (category) => {
  const form = category === 'os_type' ? newOsType.value : newProtocol.value

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
    } else {
      showAddProtocolDialog.value = false
    }
    ElMessage.success('添加成功')
  } catch (e) {
    ElMessage.error('添加失败')
  }
}

const updateTypeConfig = async (item) => {
  try {
    await store.updateTypeConfig(item.id, { name: item.name, color: item.color })
  } catch (e) {
    ElMessage.error('更新失败')
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

/* --- ✨ 统一 Element Plus 表格美化 --- */
:deep(.el-table) {
  --el-table-border-color: var(--border-light, #ebeef5);
  --el-table-header-bg-color: #f8fafc; /* 浅灰蓝表头 */
  --el-table-header-text-color: #64748b;
  border-radius: 6px; /* 让表格也有一点圆角 */
  overflow: hidden;
}

:deep(.el-table::before) {
  display: none; /* 去掉表格底部默认的白线 */
}

:deep(.el-table th.el-table__cell) {
  font-weight: 500;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* 统一斑马纹颜色 */
:deep(.el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell) {
  background-color: #fafafa;
}

/* 修改颜色选择器的对齐问题 */
:deep(.el-color-picker) {
  vertical-align: middle;
}
</style>