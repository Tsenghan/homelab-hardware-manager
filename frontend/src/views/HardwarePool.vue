<template>
  <div class="hardware-pool">
    <div class="view-header">
      <h2 class="page-title">硬件库</h2>
      <div>
        <el-button-group>
          <el-button :type="hardwareTab === 'cpu' ? 'primary' : ''" @click="hardwareTab = 'cpu'">
            <el-icon><Cpu /></el-icon> CPU
          </el-button>
          <el-button :type="hardwareTab === 'ram' ? 'primary' : ''" @click="hardwareTab = 'ram'">
            <el-icon><Histogram /></el-icon> 内存
          </el-button>
          <el-button :type="hardwareTab === 'disk' ? 'primary' : ''" @click="hardwareTab = 'disk'">
            <el-icon><Folder /></el-icon> 硬盘
          </el-button>
        </el-button-group>
        <el-button type="primary" style="margin-left: 12px" @click="addHardware">
          <el-icon><Plus /></el-icon> 添加硬件
        </el-button>
      </div>
    </div>

    <!-- CPU Table -->
    <div v-if="hardwareTab === 'cpu'" class="hardware-section">
      <table class="hardware-table">
        <thead>
          <tr>
            <th>型号</th>
            <th>核心数</th>
            <th>主频</th>
            <th>购买日期</th>
            <th>备注</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cpu in store.state.allHardware.cpus" :key="cpu.id">
            <td>{{ cpu.model }}</td>
            <td>{{ cpu.cores }} 核</td>
            <td>{{ cpu.clockSpeed }} GHz</td>
            <td>{{ cpu.purchaseDate || '-' }}</td>
            <td>{{ cpu.remarks || '-' }}</td>
            <td>
              <el-tag v-if="cpu.computerId" size="small" type="success">
                {{ getComputerName(cpu.computerId) }}
              </el-tag>
              <el-tag v-else size="small" type="info">闲置</el-tag>
            </td>
            <td>
              <el-button size="small" type="danger" :disabled="!!cpu.computerId" @click="deleteHardware('cpu', cpu.id)">
                删除
              </el-button>
            </td>
          </tr>
        </tbody>
      </table>
      <el-empty v-if="store.state.allHardware.cpus.length === 0" description="暂无CPU数据" />
    </div>

    <!-- RAM Table -->
    <div v-if="hardwareTab === 'ram'" class="hardware-section">
      <table class="hardware-table">
        <thead>
          <tr>
            <th>品牌</th>
            <th>型号</th>
            <th>容量</th>
            <th>类型</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="ram in store.state.allHardware.rams" :key="ram.id">
            <td>{{ ram.brand }}</td>
            <td>{{ ram.model }}</td>
            <td>{{ ram.capacity }} GB</td>
            <td>{{ ram.type }}</td>
            <td>
              <el-tag v-if="ram.computerId" size="small" type="success">
                {{ getComputerName(ram.computerId) }}
              </el-tag>
              <el-tag v-else size="small" type="info">闲置</el-tag>
            </td>
            <td>
              <el-button size="small" type="danger" :disabled="!!ram.computerId" @click="deleteHardware('ram', ram.id)">
                删除
              </el-button>
            </td>
          </tr>
        </tbody>
      </table>
      <el-empty v-if="store.state.allHardware.rams.length === 0" description="暂无内存数据" />
    </div>

    <!-- Disk Table -->
    <div v-if="hardwareTab === 'disk'" class="hardware-section">
      <table class="hardware-table">
        <thead>
          <tr>
            <th>品牌</th>
            <th>型号</th>
            <th>容量</th>
            <th>接口</th>
            <th>文件系统</th>
            <th>用途</th>
            <th>备注</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="disk in store.state.allHardware.disks" :key="disk.id">
            <td>{{ disk.brand }}</td>
            <td>{{ disk.model }}</td>
            <td>{{ disk.capacity }} GB</td>
            <td>{{ disk.interface }}</td>
            <td>{{ disk.fileSystem || '-' }}</td>
            <td>{{ disk.purpose || '-' }}</td>
            <td>{{ disk.remarks || '-' }}</td>
            <td>
              <el-tag v-if="disk.computerId" size="small" type="success">
                {{ getComputerName(disk.computerId) }}
              </el-tag>
              <el-tag v-else size="small" type="info">闲置</el-tag>
            </td>
            <td>
              <el-button size="small" type="danger" :disabled="!!disk.computerId" @click="deleteHardware('disk', disk.id)">
                删除
              </el-button>
            </td>
          </tr>
        </tbody>
      </table>
      <el-empty v-if="store.state.allHardware.disks.length === 0" description="暂无硬盘数据" />
    </div>

    <!-- Hardware Dialog -->
    <el-dialog v-model="showDialog" :title="'添加' + hardwareTab.toUpperCase()" width="550px">
      <el-form label-width="90px">
        <template v-if="hardwareTab === 'cpu'">
          <el-form-item label="型号"><el-input v-model="hardwareForm.cpu.model" placeholder="如 Intel Xeon E-2286G" /></el-form-item>
          <el-form-item label="核心数"><el-input-number v-model="hardwareForm.cpu.cores" :min="1" :max="128" /></el-form-item>
          <el-form-item label="主频(GHz)"><el-input-number v-model="hardwareForm.cpu.clockSpeed" :min="0.1" :max="10" :step="0.1" /></el-form-item>
          <el-form-item label="购买日期"><el-date-picker v-model="hardwareForm.cpu.purchaseDate" type="date" placeholder="选择日期" style="width:100%" /></el-form-item>
          <el-form-item label="备注"><el-input v-model="hardwareForm.cpu.remarks" placeholder="备注信息" /></el-form-item>
        </template>
        <template v-if="hardwareTab === 'ram'">
          <el-form-item label="品牌"><el-input v-model="hardwareForm.ram.brand" placeholder="如 Samsung" /></el-form-item>
          <el-form-item label="型号"><el-input v-model="hardwareForm.ram.model" placeholder="如 M393A2G40AB2" /></el-form-item>
          <el-form-item label="容量(GB)"><el-input-number v-model="hardwareForm.ram.capacity" :min="1" :max="512" /></el-form-item>
          <el-form-item label="类型">
            <el-select v-model="hardwareForm.ram.type" placeholder="选择类型" style="width:100%">
              <el-option label="DDR4" value="DDR4" />
              <el-option label="DDR5" value="DDR5" />
            </el-select>
          </el-form-item>
        </template>
        <template v-if="hardwareTab === 'disk'">
          <el-form-item label="品牌"><el-input v-model="hardwareForm.disk.brand" placeholder="如 Samsung" /></el-form-item>
          <el-form-item label="型号"><el-input v-model="hardwareForm.disk.model" placeholder="如 PM983" /></el-form-item>
          <el-form-item label="容量(GB)"><el-input-number v-model="hardwareForm.disk.capacity" :min="1" :max="100000" /></el-form-item>
          <el-form-item label="接口">
            <el-select v-model="hardwareForm.disk.interface" placeholder="选择接口" style="width:100%">
              <el-option label="NVMe" value="NVMe" />
              <el-option label="SATA" value="SATA" />
              <el-option label="USB" value="USB" />
              <el-option label="RDM" value="RDM" />
              <el-option label="控制器直通" value="控制器直通" />
            </el-select>
          </el-form-item>
          <el-form-item label="文件系统">
            <el-select v-model="hardwareForm.disk.fileSystem" placeholder="选择文件系统" style="width:100%">
              <el-option label="ext4" value="ext4" />
              <el-option label="ZFS" value="ZFS" />
              <el-option label="NTFS" value="NTFS" />
              <el-option label="Btrfs" value="Btrfs" />
              <el-option label="XFS" value="XFS" />
            </el-select>
          </el-form-item>
          <el-form-item label="用途"><el-input v-model="hardwareForm.disk.purpose" placeholder="如 系统盘、数据存储" /></el-form-item>
          <el-form-item label="系统盘"><el-switch v-model="hardwareForm.disk.isBootDisk" /></el-form-item>
          <el-form-item label="备注"><el-input v-model="hardwareForm.disk.remarks" placeholder="备注信息" /></el-form-item>
        </template>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="saveHardware">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Cpu, Histogram, Folder, Plus } from '@element-plus/icons-vue'
import { useAppStore } from '../stores/app'
import { ElMessage } from 'element-plus'

const store = useAppStore()

const hardwareTab = ref('cpu')
const showDialog = ref(false)

const getComputerName = (computerId) => {
  const computer = store.state.computers.find(c => c.id === computerId)
  return computer?.name || '未知'
}

const hardwareForm = ref({
  cpu: { model: '', cores: 8, clockSpeed: 3.0, purchaseDate: '', remarks: '' },
  ram: { brand: '', model: '', capacity: 32, type: 'DDR4' },
  disk: { brand: '', model: '', capacity: 500, interface: 'NVMe', fileSystem: '', purpose: '', isBootDisk: false, remarks: '' }
})

const addHardware = () => {
  showDialog.value = true
}

const saveHardware = async () => {
  try {
    await store.saveHardware(hardwareTab.value, hardwareForm.value[hardwareTab.value])
    showDialog.value = false
    // Reset form
    if (hardwareTab.value === 'cpu') {
      hardwareForm.value.cpu = { model: '', cores: 8, clockSpeed: 3.0, purchaseDate: '', remarks: '' }
    } else if (hardwareTab.value === 'ram') {
      hardwareForm.value.ram = { brand: '', model: '', capacity: 32, type: 'DDR4' }
    } else {
      hardwareForm.value.disk = { brand: '', model: '', capacity: 500, interface: 'NVMe', fileSystem: '', purpose: '', isBootDisk: false, remarks: '' }
    }
    ElMessage.success('添加成功')
  } catch (e) {
    ElMessage.error('添加失败')
  }
}

const deleteHardware = async (type, id) => {
  try {
    await store.deleteHardware(type, id)
    ElMessage.success('删除成功')
  } catch (e) {
    ElMessage.error('删除失败')
  }
}
</script>

<style scoped>
.hardware-pool {
  padding: 0;
}

.hardware-section {
  background: var(--bg-white);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.hardware-table {
  width: 100%;
  border-collapse: collapse;
}

.hardware-table th,
.hardware-table td {
  padding: 10px 14px;
  text-align: left;
  border-bottom: 1px solid var(--border-light);
}

.hardware-table th {
  background: var(--bg-gray-50);
  font-weight: 500;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-secondary);
}

.hardware-table tr:hover td {
  background: var(--bg-gray-50);
}

.hardware-table tr:last-child td {
  border-bottom: none;
}
</style>
