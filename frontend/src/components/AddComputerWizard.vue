<template>
  <el-dialog
    :model-value="modelValue"
    title="添加物理主机"
    width="700px"
    @close="handleClose"
  >
    <el-steps :active="currentStep" finish-status="success" align-center class="wizard-steps">
      <el-step title="基础信息" />
      <el-step title="硬件配置" />
      <el-step title="宿主系统" />
    </el-steps>

    <div class="wizard-content">
      <!-- Step 1: 基础信息 -->
      <div v-if="currentStep === 0" class="step-form">
        <el-form :model="formData.basic" label-width="100px">
          <el-form-item label="主机名称" required>
            <el-input v-model="formData.basic.name" placeholder="如 PVE-Server-1" />
          </el-form-item>
          <el-form-item label="物理位置">
            <el-input v-model="formData.basic.location" placeholder="如 机柜A-3U" />
          </el-form-item>
          <el-form-item label="备注">
            <el-input v-model="formData.basic.notes" type="textarea" rows="3" />
          </el-form-item>
        </el-form>
      </div>

      <!-- Step 2: 硬件配置 -->
      <div v-if="currentStep === 1" class="step-form">
        <el-form :model="formData.hardware" label-width="100px">
          <el-form-item label="CPU型号">
            <el-input v-model="formData.hardware.cpuModel" placeholder="如 Intel Xeon E-2286G" />
          </el-form-item>
          <el-form-item label="核心数">
            <el-input-number v-model="formData.hardware.cpuCores" :min="1" :max="128" />
          </el-form-item>
          <el-form-item label="主频(GHz)">
            <el-input-number v-model="formData.hardware.clockSpeed" :min="0.1" :max="10" :step="0.1" />
          </el-form-item>
          <el-divider>内存</el-divider>
          <el-form-item label="总容量(GB)">
            <el-input-number v-model="formData.hardware.totalRam" :min="1" :max="1024" />
          </el-form-item>
          <el-form-item label="内存类型">
            <el-select v-model="formData.hardware.ramType" placeholder="选择类型">
              <el-option label="DDR4" value="DDR4" />
              <el-option label="DDR5" value="DDR5" />
              <el-option label="ECC DDR4" value="ECC DDR4" />
            </el-select>
          </el-form-item>
          <el-divider>硬盘</el-divider>
          <div v-for="(disk, index) in formData.hardware.disks" :key="index" class="disk-item">
            <el-form-item label="硬盘{{ index + 1 }}">
              <el-input v-model="disk.model" placeholder="型号" style="width: 200px; margin-right: 8px" />
              <el-input-number v-model="disk.capacity" :min="1" :max="100000" placeholder="GB" style="width: 120px" />
            </el-form-item>
          </div>
          <el-button size="small" @click="addDisk">+ 添加硬盘</el-button>
        </el-form>
      </div>

      <!-- Step 3: 宿主系统 -->
      <div v-if="currentStep === 3" class="step-form">
        <el-form :model="formData.os" label-width="100px">
          <el-form-item label="系统名称">
            <el-input v-model="formData.os.name" placeholder="如 Proxmox VE 8" />
          </el-form-item>
          <el-form-item label="类型">
            <el-select v-model="formData.os.type" placeholder="选择类型">
              <el-option label="Proxmox VE" value="PVE" />
              <el-option label="ESXi" value="ESXi" />
              <el-option label="Windows" value="Windows" />
              <el-option label="Linux" value="Linux" />
            </el-select>
          </el-form-item>
          <el-form-item label="业务IP">
            <el-input v-model="formData.os.ipAddress" placeholder="该系统的主业务IP" />
          </el-form-item>
          <el-form-item label="MAC地址">
            <el-input v-model="formData.os.macAddress" placeholder="如 00:11:22:33:44:55" />
          </el-form-item>
          <el-form-item label="备注">
            <el-input v-model="formData.os.notes" type="textarea" rows="3" />
          </el-form-item>
        </el-form>
      </div>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button v-if="currentStep > 0" @click="prevStep">上一步</el-button>
        <el-button v-if="currentStep < 2" type="primary" @click="nextStep">下一步</el-button>
        <el-button v-if="currentStep === 2" type="primary" @click="submitForm">完成</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive } from 'vue'

const props = defineProps({
  modelValue: Boolean
})

const emit = defineEmits(['update:modelValue', 'complete'])

const currentStep = ref(0)

const formData = reactive({
  basic: { name: '', location: '', notes: '' },
  hardware: {
    cpuModel: '',
    cpuCores: 8,
    clockSpeed: 3.0,
    totalRam: 32,
    ramType: 'DDR4',
    disks: [{ model: '', capacity: 500 }]
  },
  os: { name: '', type: 'PVE', ipAddress: '', macAddress: '', notes: '' }
})

const addDisk = () => {
  formData.hardware.disks.push({ model: '', capacity: 500 })
}

const nextStep = () => {
  if (currentStep.value < 2) currentStep.value++
}

const prevStep = () => {
  if (currentStep.value > 0) currentStep.value--
}

const submitForm = () => {
  console.log('Form submitted:', formData)
  emit('complete', formData)
  handleClose()
}

const handleClose = () => {
  emit('update:modelValue', false)
  currentStep.value = 0
}
</script>

<style scoped>
.wizard-steps {
  margin-bottom: 32px;
}

.wizard-content {
  min-height: 300px;
}

.step-form {
  padding: 20px 0;
}

.disk-item {
  margin-bottom: 16px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
