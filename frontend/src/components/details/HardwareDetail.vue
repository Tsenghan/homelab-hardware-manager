<template>
  <div class="detail-container">
    <div class="info-section">
      <template v-if="type === 'cpu'">
        <div class="info-row">
          <span class="label">型号</span>
          <span class="value">{{ data.model }}</span>
        </div>
        <div class="info-row">
          <span class="label">核心数</span>
          <span class="value">{{ data.cores }} 核</span>
        </div>
        <div class="info-row">
          <span class="label">主频</span>
          <span class="value">{{ data.clock_speed_ghz }} GHz</span>
        </div>
        <div class="info-row">
          <span class="label">购买日期</span>
          <span class="value">{{ data.purchase_date || '未知' }}</span>
        </div>
        <div class="info-row">
          <span class="label">价格</span>
          <span class="value">{{ data.price ? `¥${data.price}` : '未知' }}</span>
        </div>
        <div class="info-row">
          <span class="label">备注</span>
          <span class="value">{{ data.notes || '无' }}</span>
        </div>
      </template>

      <template v-else-if="type === 'ram'">
        <div class="info-row">
          <span class="label">品牌</span>
          <span class="value">{{ data.brand }}</span>
        </div>
        <div class="info-row">
          <span class="label">型号</span>
          <span class="value">{{ data.model }}</span>
        </div>
        <div class="info-row">
          <span class="label">容量</span>
          <span class="value">{{ data.capacity }} GB</span>
        </div>
        <div class="info-row">
          <span class="label">类型</span>
          <span class="value">{{ data.type }}</span>
        </div>
        <div class="info-row">
          <span class="label">槽位</span>
          <span class="value">{{ data.slots_occupied }}</span>
        </div>
        <div class="info-row">
          <span class="label">购买日期</span>
          <span class="value">{{ data.purchase_date || '未知' }}</span>
        </div>
        <div class="info-row">
          <span class="label">备注</span>
          <span class="value">{{ data.notes || '无' }}</span>
        </div>
      </template>

      <template v-else-if="type === 'disk'">
        <div class="info-row">
          <span class="label">品牌</span>
          <span class="value">{{ data.brand }}</span>
        </div>
        <div class="info-row">
          <span class="label">型号</span>
          <span class="value">{{ data.model }}</span>
        </div>
        <div class="info-row">
          <span class="label">容量</span>
          <span class="value">{{ data.capacity }} GB</span>
        </div>
        <div class="info-row">
          <span class="label">接口</span>
          <span class="value">{{ data.interface }}</span>
        </div>
        <div class="info-row">
          <span class="label">槽位</span>
          <span class="value">{{ data.slot_info || '未知' }}</span>
        </div>
        <div class="info-row">
          <span class="label">系统盘</span>
          <span class="value">
            <el-tag :type="data.is_boot_disk ? 'success' : 'info'" size="small">
              {{ data.is_boot_disk ? '是' : '否' }}
            </el-tag>
          </span>
        </div>
        <div class="info-row">
          <span class="label">购买日期</span>
          <span class="value">{{ data.purchase_date || '未知' }}</span>
        </div>
        <div class="info-row">
          <span class="label">备注</span>
          <span class="value">{{ data.notes || '无' }}</span>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
defineProps({
  type: String,
  data: Object
})
</script>

<style scoped>
.detail-container {
  padding: 20px;
}

.info-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-row {
  display: flex;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 8px;
}

.info-row .label {
  width: 100px;
  color: #909399;
  font-size: 14px;
}

.info-row .value {
  flex: 1;
  color: #303133;
  font-size: 14px;
}
</style>
