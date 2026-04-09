<template>
  <div class="settings-view">
    <h2 class="page-title">配置管理</h2>

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
  max-width: 800px;
}

.settings-section {
  margin-bottom: 24px;
  background: var(--bg-white);
  padding: 20px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.settings-section-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #303133;
}
</style>
