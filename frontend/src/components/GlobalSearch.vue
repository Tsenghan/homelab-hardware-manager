<template>
  <div class="global-search">
    <el-input
      v-model="searchQuery"
      placeholder="搜索... (Ctrl+K)"
      clearable
      @input="handleSearch"
      @focus="showResults = true"
      @blur="handleBlur"
    >
      <template #prefix>
        <el-icon><Search /></el-icon>
      </template>
    </el-input>

    <div v-if="showResults && searchResults.length > 0" class="search-results">
      <div v-for="(group, category) in groupedResults" :key="category" class="result-group">
        <div class="result-category">{{ getCategoryLabel(category) }}</div>
        <div
          v-for="item in group"
          :key="item.id"
          class="result-item"
          @mousedown.prevent="selectResult(item, category, $event)"
        >
          <component :is="getCategoryIcon(category)" theme="outline" size="18" stroke="#409EFF" class="result-icon" />
          <div class="result-info">
            <div class="result-name">{{ item.name || item.model }}</div>
            <div class="result-meta">{{ getItemMeta(item, category) }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { Computer, Cpu, MemoryOne, HardDisk, ComputerOne, System } from '@icon-park/vue-next'
import { useAppStore } from '../stores/app'

const emit = defineEmits(['select'])
const store = useAppStore()

const searchQuery = ref('')
const showResults = ref(false)
const searchResults = ref([])

const groupedResults = computed(() => {
  const groups = {}
  searchResults.value.forEach(item => {
    if (!groups[item.category]) {
      groups[item.category] = []
    }
    groups[item.category].push(item)
  })
  return groups
})

const handleSearch = () => {
  if (searchQuery.value.length < 1) {
    searchResults.value = []
    return
  }
  const q = searchQuery.value.toLowerCase()

  const items = [
    ...store.state.computers.map(c => ({ ...c, category: 'computer', name: c.name })),
    ...store.state.services.map(s => ({ ...s, category: 'service', name: s.name })),
    ...store.state.allOsInstances.map(os => ({ ...os, category: 'os_instance', name: os.name })),
    ...store.state.allHardware.cpus.map(h => ({ ...h, category: 'cpu', name: h.model })),
    ...store.state.allHardware.rams.map(h => ({ ...h, category: 'ram', name: h.model })),
    ...store.state.allHardware.disks.map(h => ({ ...h, category: 'disk', name: h.model }))
  ]

  searchResults.value = items.filter(item => {
    const searchText = [
      item.name,
      item.model,
      item.brand,
      item.ip_address,
      item.ip,
      item.remarks,
      item.location,
      item.description
    ].filter(Boolean).join(' ').toLowerCase()
    return searchText.includes(q)
  }).slice(0, 15)
}

const handleBlur = () => {
  // Delay to allow click events to fire first
  setTimeout(() => {
    if (showResults.value) {
      showResults.value = false
    }
  }, 300)
}

const selectResult = (item, category, event) => {
  if (event) {
    event.preventDefault()
    event.stopPropagation()
  }
  emit('select', { type: category, data: item })
  searchQuery.value = ''
  searchResults.value = []
  showResults.value = false
}

const getCategoryLabel = (category) => {
  const labels = {
    computer: '主机',
    os_instance: '系统',
    service: '服务',
    cpu: 'CPU',
    ram: '内存',
    disk: '硬盘'
  }
  return labels[category] || category
}

const getCategoryIcon = (category) => {
  const icons = {
    computer: Computer,
    cpu: Cpu,
    ram: MemoryOne,
    disk: HardDisk,
    os_instance: ComputerOne,
    service: System
  }
  return icons[category] || Computer
}

const getItemMeta = (item, category) => {
  if (category === 'computer') return item.location || ''
  if (category === 'service') return `${item.protocol}://${item.ip_address}:${item.port}`
  if (category === 'cpu') return `${item.cores}核 · ${item.clockSpeed}GHz`
  if (category === 'ram') return `${item.capacity}GB · ${item.type}`
  if (category === 'disk') return `${item.capacity}GB · ${item.interface}`
  if (category === 'os_instance') return `${item.type} · ${item.ipAddress || '无IP'}`
  return ''
}

// Keyboard shortcut
const handleKeydown = (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault()
    document.querySelector('.global-search .el-input__wrapper')?.querySelector('input')?.focus()
  }
}

if (typeof window !== 'undefined') {
  window.addEventListener('keydown', handleKeydown)
  onUnmounted(() => {
    window.removeEventListener('keydown', handleKeydown)
  })
}
</script>

<style scoped>
.global-search {
  position: relative;
  width: 100%;
}

.search-results {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  right: 0;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  max-height: 400px;
  overflow-y: auto;
  z-index: 1000;
}

.result-group {
  padding: 8px 0;
}

.result-group:not(:last-child) {
  border-bottom: 1px solid #f0f0f0;
}

.result-category {
  padding: 8px 16px 4px;
  font-size: 12px;
  color: #909399;
  font-weight: 600;
  text-transform: uppercase;
}

.result-item {
  display: flex;
  align-items: center;
  padding: 10px 16px;
  cursor: pointer;
  transition: background 0.2s;
}

.result-item:hover {
  background: #f5f7fa;
}

.result-icon {
  margin-right: 12px;
  flex-shrink: 0;
}

.result-info {
  flex: 1;
  min-width: 0;
}

.result-name {
  font-weight: 500;
  color: #303133;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.result-meta {
  font-size: 12px;
  color: #909399;
  margin-top: 2px;
}
</style>
