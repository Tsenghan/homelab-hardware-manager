<template>
  <div class="computer-list">
    <div class="view-header">
      <h2 class="page-title">
        物理主机
        <el-input v-model="filterText" placeholder="搜索主机..." clearable style="width: 200px; margin-left: 16px">
          <template #prefix><el-icon><Search /></el-icon></template>
        </el-input>
      </h2>
      <el-button type="primary" @click="showDialog = true">
        <el-icon><Plus /></el-icon>
        添加主机
      </el-button>
    </div>

    <div class="computer-grid">
      <div
        v-for="computer in filteredComputers"
        :key="computer.id"
        class="computer-card"
        @click="openDrawer('computer', computer)"
      >
        <div class="card-header">
          <div class="computer-icon">
            <Computer theme="outline" size="28" stroke="currentColor" />
          </div>
          <div class="computer-info">
            <div class="computer-name-row">
              <span class="computer-name">{{ computer.name }}</span>
              <span v-if="computer.location" class="computer-location">{{ computer.location }}</span>
            </div>
            <div v-if="computer.remarks" class="computer-remarks">{{ computer.remarks }}</div>
          </div>
        </div>

        <div class="card-body">
          <div class="info-row">
            <span class="label">CPU</span>
            <span class="value">{{ getComputerCpuName(computer.id) }}</span>
          </div>
          <div class="info-row">
            <span class="label">内存</span>
            <span class="value">{{ getComputerTotalRam(computer.id) }}</span>
          </div>
          <div class="info-row">
            <span class="label">硬盘</span>
            <span class="value">{{ getComputerTotalDisk(computer.id) }}</span>
          </div>
          <div class="info-row">
            <span class="label">虚拟机</span>
            <span class="value">{{ computer.osInstanceIds?.length || 0 }} 台</span>
          </div>
        </div>

        <div class="card-footer">
          <span></span>
          <el-button size="small" @click.stop="editComputer(computer)">
            <el-icon><Edit /></el-icon>
          </el-button>
          <el-button size="small" type="danger" @click.stop="confirmDelete(computer)">
            <el-icon><Delete /></el-icon>
          </el-button>
        </div>
      </div>
    </div>

    <el-empty v-if="store.state.computers.length === 0" description="暂无主机数据" />

    <!-- Computer Dialog -->
    <el-dialog v-model="showDialog" :title="editingComputer ? '编辑主机' : '添加主机'" width="800px">
      <el-form label-width="100px">
        <el-form-item label="主机名称" required>
          <el-input v-model="form.name" placeholder="如 PVE-Server-1" />
        </el-form-item>
        <el-form-item label="物理位置">
          <el-input v-model="form.location" placeholder="如 机柜A-3U" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.remarks" type="textarea" rows="2" placeholder="备注信息" />
        </el-form-item>
        <el-divider>选择 CPU</el-divider>
        <div class="checkbox-grid">
          <div
            v-for="cpu in store.state.allHardware.cpus"
            :key="cpu.id"
            class="checkbox-item"
            :class="{ selected: form.cpuIds.includes(cpu.id), assigned: cpu.computerId && cpu.computerId !== editingComputer?.id }"
            @click="toggleHardwareSelection('cpu', cpu.id, cpu.computerId)"
          >
            <div style="display:flex;justify-content:space-between;align-items:center">
              <div>
                <div>{{ cpu.model }}</div>
                <div style="font-size:12px;color:#909399">{{ cpu.cores }}核 @ {{ cpu.clockSpeed || '-' }}GHz</div>
              </div>
              <el-button size="small" text @click.stop="openHardwareEdit('cpu', cpu)">
                <el-icon><Edit /></el-icon>
              </el-button>
            </div>
            <el-tag v-if="cpu.computerId && cpu.computerId === editingComputer?.id" size="small" type="warning" style="margin-top:4px">已占用</el-tag>
            <el-tag v-else-if="cpu.computerId" size="small" type="info" style="margin-top:4px">已分配</el-tag>
            <el-tag v-else size="small" type="success" style="margin-top:4px">空闲</el-tag>
          </div>
        </div>
        <el-divider>选择 内存</el-divider>
        <div class="checkbox-grid">
          <div
            v-for="ram in store.state.allHardware.rams"
            :key="ram.id"
            class="checkbox-item"
            :class="{ selected: form.ramIds.includes(ram.id), assigned: ram.computerId && ram.computerId !== editingComputer?.id }"
            @click="toggleHardwareSelection('ram', ram.id, ram.computerId)"
          >
            <div style="display:flex;justify-content:space-between;align-items:center">
              <div>
                <div>{{ ram.brand }} {{ ram.model }}</div>
                <div style="font-size:12px;color:#909399">{{ ram.capacity }}GB {{ ram.type }}</div>
              </div>
              <el-button size="small" text @click.stop="openHardwareEdit('ram', ram)">
                <el-icon><Edit /></el-icon>
              </el-button>
            </div>
            <el-tag v-if="ram.computerId && ram.computerId === editingComputer?.id" size="small" type="warning" style="margin-top:4px">已占用</el-tag>
            <el-tag v-else-if="ram.computerId" size="small" type="info" style="margin-top:4px">已分配</el-tag>
            <el-tag v-else size="small" type="success" style="margin-top:4px">空闲</el-tag>
          </div>
        </div>
        <el-divider>选择 硬盘</el-divider>
        <div class="checkbox-grid">
          <div
            v-for="disk in store.state.allHardware.disks"
            :key="disk.id"
            class="checkbox-item"
            :class="{ selected: form.diskIds.includes(disk.id), assigned: disk.computerId && disk.computerId !== editingComputer?.id }"
            @click="toggleHardwareSelection('disk', disk.id, disk.computerId)"
          >
            <div style="display:flex;justify-content:space-between;align-items:center">
              <div>
                <div>{{ disk.brand }} {{ disk.model }}</div>
                <div style="font-size:12px;color:#909399">{{ disk.capacity }}GB {{ disk.interface }} {{ disk.isBootDisk ? '(启动盘)' : '' }}</div>
              </div>
              <el-button size="small" text @click.stop="openHardwareEdit('disk', disk)">
                <el-icon><Edit /></el-icon>
              </el-button>
            </div>
            <el-tag v-if="disk.computerId && disk.computerId === editingComputer?.id" size="small" type="warning" style="margin-top:4px">已占用</el-tag>
            <el-tag v-else-if="disk.computerId" size="small" type="info" style="margin-top:4px">已分配</el-tag>
            <el-tag v-else size="small" type="success" style="margin-top:4px">空闲</el-tag>
          </div>
        </div>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="saveComputer">保存</el-button>
      </template>
    </el-dialog>

    <!-- CPU Edit Dialog -->
    <el-dialog v-model="showHardwareEditDialog" :title="editingHardware.type === 'cpu' ? '编辑 CPU' : editingHardware.type === 'ram' ? '编辑 内存' : '编辑 硬盘'" width="500px">
      <el-form label-width="100px">
        <template v-if="editingHardware.type === 'cpu'">
          <el-form-item label="型号">
            <el-input v-model="hardwareEditForm.model" placeholder="如 Intel i9-13900K" />
          </el-form-item>
          <el-form-item label="核心数">
            <el-input-number v-model="hardwareEditForm.cores" :min="1" />
          </el-form-item>
          <el-form-item label="频率 (GHz)">
            <el-input-number v-model="hardwareEditForm.clockSpeed" :min="0" :precision="2" />
          </el-form-item>
          <el-form-item label="购买日期">
            <el-input v-model="hardwareEditForm.purchaseDate" placeholder="如 2024-01" />
          </el-form-item>
          <el-form-item label="备注">
            <el-input v-model="hardwareEditForm.remarks" type="textarea" rows="2" />
          </el-form-item>
        </template>
        <template v-else-if="editingHardware.type === 'ram'">
          <el-form-item label="品牌">
            <el-input v-model="hardwareEditForm.brand" placeholder="如 Kingston" />
          </el-form-item>
          <el-form-item label="型号">
            <el-input v-model="hardwareEditForm.model" placeholder="如 DDR4-3200" />
          </el-form-item>
          <el-form-item label="容量 (GB)">
            <el-input-number v-model="hardwareEditForm.capacity" :min="1" />
          </el-form-item>
          <el-form-item label="类型">
            <el-input v-model="hardwareEditForm.type" placeholder="如 DDR4" />
          </el-form-item>
          <el-form-item label="购买日期">
            <el-input v-model="hardwareEditForm.purchaseDate" placeholder="如 2024-01" />
          </el-form-item>
          <el-form-item label="备注">
            <el-input v-model="hardwareEditForm.remarks" type="textarea" rows="2" />
          </el-form-item>
        </template>
        <template v-else>
          <el-form-item label="品牌">
            <el-input v-model="hardwareEditForm.brand" placeholder="如 Samsung" />
          </el-form-item>
          <el-form-item label="型号">
            <el-input v-model="hardwareEditForm.model" placeholder="如 980 PRO" />
          </el-form-item>
          <el-form-item label="容量 (GB)">
            <el-input-number v-model="hardwareEditForm.capacity" :min="1" />
          </el-form-item>
          <el-form-item label="接口">
            <el-input v-model="hardwareEditForm.interface" placeholder="如 NVMe PCIe 4.0" />
          </el-form-item>
          <el-form-item label="文件系统">
            <el-input v-model="hardwareEditForm.fileSystem" placeholder="如 ext4" />
          </el-form-item>
          <el-form-item label="用途">
            <el-input v-model="hardwareEditForm.purpose" placeholder="如 数据存储" />
          </el-form-item>
          <el-form-item label="启动盘">
            <el-switch v-model="hardwareEditForm.isBootDisk" />
          </el-form-item>
          <el-form-item label="购买日期">
            <el-input v-model="hardwareEditForm.purchaseDate" placeholder="如 2024-01" />
          </el-form-item>
          <el-form-item label="备注">
            <el-input v-model="hardwareEditForm.remarks" type="textarea" rows="2" />
          </el-form-item>
        </template>
      </el-form>
      <template #footer>
        <el-button @click="showHardwareEditDialog = false">取消</el-button>
        <el-button type="primary" @click="saveHardwareEdit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, inject } from 'vue'
import { Plus, Search, Edit, Delete } from '@element-plus/icons-vue'
import { Computer } from '@icon-park/vue-next'
import { ElMessage } from 'element-plus'
import { useAppStore } from '../stores/app'
import { ElMessageBox } from 'element-plus'

const store = useAppStore()
const openDrawer = inject('openDrawer')

const filterText = ref('')
const showDialog = ref(false)
const editingComputer = ref(null)

// Hardware edit dialog
const showHardwareEditDialog = ref(false)
const editingHardware = ref({ type: '', data: null })
const hardwareEditForm = ref({})

const form = ref({
  name: '',
  location: '',
  remarks: '',
  cpuIds: [],
  ramIds: [],
  diskIds: []
})

const filteredComputers = computed(() => {
  if (!filterText.value) return store.state.computers
  const q = filterText.value.toLowerCase()
  return store.state.computers.filter(c =>
    c.name.toLowerCase().includes(q) ||
    (c.location && c.location.toLowerCase().includes(q)) ||
    (c.remarks && c.remarks.toLowerCase().includes(q))
  )
})

const toggleHardwareSelection = (type, id, computerId) => {
  // 如果已分配给其他主机，不允许操作
  if (computerId && computerId !== editingComputer.value?.id) return
  if (type === 'cpu') {
    const idx = form.value.cpuIds.indexOf(id)
    if (idx > -1) form.value.cpuIds.splice(idx, 1)
    else form.value.cpuIds.push(id)
  } else if (type === 'ram') {
    const idx = form.value.ramIds.indexOf(id)
    if (idx > -1) form.value.ramIds.splice(idx, 1)
    else form.value.ramIds.push(id)
  } else {
    const idx = form.value.diskIds.indexOf(id)
    if (idx > -1) form.value.diskIds.splice(idx, 1)
    else form.value.diskIds.push(id)
  }
}

const getComputerCpuName = (cid) => {
  const cpus = store.getComputerCpus(cid)
  if (cpus.length === 0) return '无'
  return cpus.map(c => c.model).join(', ') || '无'
}

const getComputerTotalRam = (cid) => {
  const rams = store.getComputerRams(cid)
  if (rams.length === 0) return '无'
  const total = rams.reduce((sum, r) => sum + (r.capacity || 0), 0)
  return `${total} GB`
}

const getComputerTotalDisk = (cid) => {
  const disks = store.getComputerDisks(cid)
  if (disks.length === 0) return '无'
  const total = disks.reduce((sum, d) => sum + (d.capacity || 0), 0)
  return `${total} GB`
}

const editComputer = (c) => {
  editingComputer.value = c
  form.value = {
    id: c.id,
    name: c.name,
    location: c.location || '',
    remarks: c.remarks || '',
    cpuIds: [...(c.cpuIds || [])],
    ramIds: [...(c.ramIds || [])],
    diskIds: [...(c.diskIds || [])]
  }
  showDialog.value = true
}

const saveComputer = async () => {
  try {
    await store.saveComputer(form.value, editingComputer.value?.id)
    showDialog.value = false
    editingComputer.value = null
    resetForm()
    ElMessage.success('保存成功')
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

const confirmDelete = (computer) => {
  ElMessageBox.confirm(`确定要删除主机 "${computer.name}" 吗?`, '确认删除', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await store.deleteComputer(computer.id)
      ElMessage.success('删除成功')
    } catch (e) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

// Hardware edit
const openHardwareEdit = (type, hardware) => {
  editingHardware.value = { type, data: hardware }
  if (type === 'cpu') {
    hardwareEditForm.value = {
      model: hardware.model,
      cores: hardware.cores,
      clockSpeed: hardware.clockSpeed,
      purchaseDate: hardware.purchaseDate,
      remarks: hardware.remarks
    }
  } else if (type === 'ram') {
    hardwareEditForm.value = {
      brand: hardware.brand,
      model: hardware.model,
      capacity: hardware.capacity,
      type: hardware.type,
      purchaseDate: hardware.purchaseDate,
      remarks: hardware.remarks
    }
  } else {
    hardwareEditForm.value = {
      brand: hardware.brand,
      model: hardware.model,
      capacity: hardware.capacity,
      interface: hardware.interface,
      fileSystem: hardware.fileSystem,
      purpose: hardware.purpose,
      isBootDisk: hardware.isBootDisk,
      purchaseDate: hardware.purchaseDate,
      remarks: hardware.remarks
    }
  }
  showHardwareEditDialog.value = true
}

const saveHardwareEdit = async () => {
  try {
    await store.updateHardware(editingHardware.value.type, editingHardware.value.data.id, hardwareEditForm.value)
    showHardwareEditDialog.value = false
    ElMessage.success('保存成功')
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

const resetForm = () => {
  form.value = {
    name: '',
    location: '',
    remarks: '',
    cpuIds: [],
    ramIds: [],
    diskIds: []
  }
}
</script>

<style scoped>
.computer-list {
  padding: 0;
}

/* --- 顶部与搜索区 --- */
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
  margin-bottom: 16px;
  display: flex;
}

/* --- 网格布局优化 --- */
.computer-grid {
  display: grid;
  /* ✨ 核心调整：稍微缩小卡片基础宽度，避免过度拉伸导致的空洞感 */
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

/* --- 卡片整体质感 --- */
.computer-card {
  background: var(--bg-white, #ffffff);
  border: 1px solid var(--border-light, #e4e7ed);
  border-radius: var(--radius-lg, 12px); /* 加大一点圆角，更现代 */
  padding: 20px;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
  display: flex;
  flex-direction: column;
}

.computer-card:hover {
  border-color: var(--primary-color, #409eff);
  transform: translateY(-2px); /* ✨ 增加微微上浮的动效 */
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.06); /* 悬浮时阴影加深 */
}

/* --- 卡片头部 --- */
.card-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-light, #ebeef5);
}

.computer-icon {
  width: 48px;
  height: 48px;
  /* ✨ 使用渐变色提升硬件质感 */
  background: linear-gradient(135deg, var(--primary-color, #409eff), #2563eb);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
  box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2); /* 给图标发一点点光 */
}

.computer-icon :deep(.i-icon) {
  display: flex;
  align-items: center;
}

.computer-info {
  flex: 1;
  overflow: hidden; /* 防止长名字溢出 */
}

.computer-name-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.computer-name {
  font-size: 1.05rem;
  font-weight: 600;
  color: #1e293b;
}

.computer-location {
  font-size: 0.75rem;
  color: #475569;
  background: #f1f5f9;
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid #e2e8f0;
}

.computer-remarks {
  font-size: 0.7rem;
  color: #94a3b8;
  margin-top: 4px;
}

/* --- 卡片数据区 --- */
.card-body {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1; /* 撑满剩余空间，让 footer 到底部对齐 */
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline; /* ✨ 让不同大小的文字底部对齐 */
  font-size: 0.8125rem;
  /* ✨ 终极绝招：添加引导虚线，解决左右分离造成的视觉断层 */
  background-image: linear-gradient(to right, #cbd5e1 33%, rgba(255,255,255,0) 0%);
  background-position: bottom;
  background-size: 3px 1px;
  background-repeat: repeat-x;
  padding-bottom: 2px;
}

.info-row .label {
  color: #64748b;
  background: white; /* 遮挡虚线 */
  padding-right: 8px;
}

.info-row .value {
  color: #1e293b;
  font-weight: 500;
  background: white; /* 遮挡虚线 */
  padding-left: 8px;
}

/* --- 卡片底部操作区 --- */
.card-footer {
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid transparent; /* 留出空间，但不显示生硬的线 */
  display: flex;
  justify-content: flex-end;
  gap: 4px;
}

/* 调整按钮大小和样式，使其更精致 */
.card-footer .el-button {
  padding: 6px 8px;
  border-radius: 6px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  color: #64748b;
  transition: all 0.2s;
}

.card-footer .el-button:hover {
  background: #f1f5f9;
  color: #1e293b;
  border-color: #cbd5e1;
}

.card-footer .el-button--danger:hover {
  background: #fef2f2;
  color: #ef4444;
  border-color: #fca5a5;
}

/* --- 弹窗内的复选框网格美化 --- */
.checkbox-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 12px;
}

.checkbox-item {
  padding: 10px 12px;
  background: #f8fafc;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid #e2e8f0;
}

.checkbox-item:hover {
  border-color: #94a3b8;
  background: #f1f5f9;
}

.checkbox-item.selected {
  border-color: var(--primary-color, #409eff);
  background: rgba(64, 158, 255, 0.05);
  box-shadow: 0 0 0 1px var(--primary-color, #409eff) inset;
}

.checkbox-item.assigned {
  opacity: 0.5;
  cursor: not-allowed;
  filter: grayscale(1);
}
</style>