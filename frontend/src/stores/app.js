import { reactive, computed, provide, inject } from 'vue'
import * as api from '../api'

const STORE_KEY = 'appStore'

export function createAppStore() {
  const state = reactive({
    // Data stores
    computers: [],
    allHardware: { cpus: [], rams: [], disks: [] },
    allOsInstances: [],
    services: [],
    typeConfigs: [],
    ipGroups: [],

    // UI state
    loading: false,
    error: null
  })

  // ==================== Computed ====================
  const totalCpuCores = computed(() =>
    state.allHardware.cpus.reduce((sum, c) => sum + (c.cores || 0), 0)
  )

  const totalRam = computed(() =>
    state.allHardware.rams.reduce((sum, r) => sum + (r.capacity ?? 0), 0)
  )

  const totalDisk = computed(() =>
    state.allHardware.disks.reduce((sum, d) => sum + (d.capacity ?? 0), 0)
  )

  const totalVms = computed(() =>
    state.allOsInstances.filter(os => os.parent_os_id !== null).length
  )

  const recentVms = computed(() =>
    state.allOsInstances.filter(os => os.parent_os_id !== null).slice(0, 8)
  )

  const osTypeConfigs = computed(() =>
    state.typeConfigs.filter(t => t.category === 'os_type')
  )

  const protocolConfigs = computed(() =>
    state.typeConfigs.filter(t => t.category === 'protocol')
  )

  const serviceTypeConfigs = computed(() =>
    state.typeConfigs.filter(t => t.category === 'service_type')
  )

  // ==================== Data Loading ====================
  async function loadData() {
    state.loading = true
    state.error = null
    try {
      const [compRes, cpuRes, ramRes, diskRes, ipGroupRes, typeConfigRes] = await Promise.all([
        api.getComputers(),
        api.getAllCpus(),
        api.getAllRams(),
        api.getAllDisks(),
        api.getIpGroups(),
        api.getTypeConfigs()
      ])

      state.computers = compRes
      state.ipGroups = ipGroupRes.map(g => ({
        id: g.id,
        name: g.name,
        subnet: g.subnet,
        startIp: g.startIp,
        endIp: g.endIp
      }))
      state.typeConfigs = typeConfigRes

      // Map backend field names to frontend field names
      state.allHardware.cpus = cpuRes.map(c => ({
        id: c.id,
        computerId: c.computer_id,
        model: c.model,
        cores: c.cores,
        clockSpeed: c.clock_speed,
        purchaseDate: c.purchase_date,
        remarks: c.remarks
      }))

      state.allHardware.rams = ramRes.map(r => ({
        id: r.id,
        computerId: r.computer_id,
        brand: r.brand,
        model: r.model,
        capacity: r.capacity_gb,
        type: r.ram_type,
        purchaseDate: r.purchase_date,
        remarks: r.remarks
      }))

      state.allHardware.disks = diskRes.map(d => ({
        id: d.id,
        computerId: d.computer_id,
        brand: d.brand,
        model: d.model,
        capacity: d.capacity_gb,
        interface: d.interface,
        fileSystem: d.file_system,
        mountMethod: d.mount_method,
        purpose: d.purpose,
        isBootDisk: d.is_boot_disk,
        purchaseDate: d.purchase_date,
        remarks: d.remarks
      }))

      // Build os instances from computers
      const osList = []
      state.computers.forEach(c => {
        if (c.os_instances) {
          osList.push(...c.os_instances.map(os => ({
            id: os.id,
            computerId: c.id,
            computerName: c.name,
            name: os.name,
            type: os.os_type,
            ipAddress: os.ip_address,
            macAddress: os.mac_address,
            port: os.port,
            parentOsId: os.parent_os_id,
            notes: os.notes,
            childVmIds: (os.children || []).map(child => child.id)
          })))
        }
      })
      state.allOsInstances = osList

      // Load services for all os instances in parallel
      const svcResults = await Promise.allSettled(
        osList.map(os => api.getServices(os.id).then(sres => ({ osId: os.id, services: sres })))
      )
      const svcList = []
      svcResults.forEach(result => {
        if (result.status === 'fulfilled') {
          svcList.push(...result.value.services.map(s => ({ ...s, osInstanceId: result.value.osId })))
        } else {
          console.error('Failed to load services:', result.reason)
        }
      })
      state.services = svcList

    } catch (e) {
      state.error = e.message
      console.error('Failed to load data:', e)
    } finally {
      state.loading = false
    }
  }

  // ==================== Helper Methods ====================
  function getComputerCpus(cid) {
    return state.allHardware.cpus.filter(c => c.computerId === cid)
  }

  function getComputerRams(cid) {
    return state.allHardware.rams.filter(r => r.computerId === cid)
  }

  function getComputerDisks(cid) {
    return state.allHardware.disks.filter(d => d.computerId === cid)
  }

  function getComputerOsInstances(cid) {
    return state.allOsInstances.filter(os => os.computerId === cid)
  }

  function getHostOsInstances(cid) {
    return state.allOsInstances.filter(os => os.computerId === cid && !os.parentOsId)
  }

  function getOsInstanceById(id) {
    return state.allOsInstances.find(os => os.id === id)
  }

  function getOsInstanceName(id) {
    return getOsInstanceById(id)?.name || '未知'
  }

  function getOsServices(osId) {
    return state.services.filter(s => s.osInstanceId === osId)
  }

  function getProtocolColor(p) {
    const config = state.typeConfigs.find(t => t.category === 'protocol' && t.name === p)
    if (config) return `linear-gradient(135deg, ${config.color}, ${config.color})`
    return ({
      https: 'linear-gradient(135deg, #67C23A, #5da934)',
      http: 'linear-gradient(135deg, #409EFF, #337ecc)',
      ssh: 'linear-gradient(135deg, #909399, #7a7a7a)',
      tcp: 'linear-gradient(135deg, #E6A23C, #d4922e)'
    }[p] || 'linear-gradient(135deg, #409EFF, #337ecc)')
  }

  function getVmTagType(type) {
    const config = state.typeConfigs.find(t => t.category === 'os_type' && t.name === type)
    if (config) {
      const colorMap = { '#67C23A': 'success', '#409EFF': '', '#E6A23C': 'warning', '#F56C6C': 'danger', '#909399': 'info' }
      return colorMap[config.color] || ''
    }
    return ({ PVE: '', LXC: 'warning', VM: 'info', Linux: '', Windows: '' }[type] || '')
  }

  // ==================== Computer CRUD ====================
  async function saveComputer(form, editingId = null) {
    if (editingId) {
      // Update existing computer
      await api.updateComputer(editingId, {
        name: form.name,
        location: form.location,
        remarks: form.remarks
      })

      // Reassign hardware
      const oldComputer = state.computers.find(c => c.id === editingId)
      if (oldComputer) {
        const oldCpuIds = oldComputer.cpuIds || []
        const newCpuIds = form.cpuIds || []

        for (const id of oldCpuIds.filter(id => !newCpuIds.includes(id))) {
          await api.updateCpu(id, { computer_id: null })
          const cpu = state.allHardware.cpus.find(c => c.id === id)
          if (cpu) cpu.computerId = null
        }
        for (const id of newCpuIds.filter(id => !oldCpuIds.includes(id))) {
          await api.updateCpu(id, { computer_id: editingId })
          const cpu = state.allHardware.cpus.find(c => c.id === id)
          if (cpu) cpu.computerId = editingId
        }

        const oldRamIds = oldComputer.ramIds || []
        const newRamIds = form.ramIds || []
        for (const id of oldRamIds.filter(id => !newRamIds.includes(id))) {
          await api.updateRam(id, { computer_id: null })
          const ram = state.allHardware.rams.find(r => r.id === id)
          if (ram) ram.computerId = null
        }
        for (const id of newRamIds.filter(id => !oldRamIds.includes(id))) {
          await api.updateRam(id, { computer_id: editingId })
          const ram = state.allHardware.rams.find(r => r.id === id)
          if (ram) ram.computerId = editingId
        }

        const oldDiskIds = oldComputer.diskIds || []
        const newDiskIds = form.diskIds || []
        for (const id of oldDiskIds.filter(id => !newDiskIds.includes(id))) {
          await api.updateDisk(id, { computer_id: null })
          const disk = state.allHardware.disks.find(d => d.id === id)
          if (disk) disk.computerId = null
        }
        for (const id of newDiskIds.filter(id => !oldDiskIds.includes(id))) {
          await api.updateDisk(id, { computer_id: editingId })
          const disk = state.allHardware.disks.find(d => d.id === id)
          if (disk) disk.computerId = editingId
        }
      }

      // Reload computer data
      const fullRes = await api.getComputer(editingId)
      const idx = state.computers.findIndex(c => c.id === editingId)
      if (idx >= 0) state.computers[idx] = fullRes

    } else {
      // Create new computer
      const res = await api.createComputer({
        name: form.name,
        location: form.location,
        remarks: form.remarks
      })
      const newId = res.id

      // Assign hardware
      for (const id of (form.cpuIds || [])) {
        await api.updateCpu(id, { computer_id: newId })
        const cpu = state.allHardware.cpus.find(c => c.id === id)
        if (cpu) cpu.computerId = newId
      }
      for (const id of (form.ramIds || [])) {
        await api.updateRam(id, { computer_id: newId })
        const ram = state.allHardware.rams.find(r => r.id === id)
        if (ram) ram.computerId = newId
      }
      for (const id of (form.diskIds || [])) {
        await api.updateDisk(id, { computer_id: newId })
        const disk = state.allHardware.disks.find(d => d.id === id)
        if (disk) disk.computerId = newId
      }

      // Fetch full computer data
      const fullRes = await api.getComputer(newId)
      state.computers.push(fullRes)

      // Update os instances list
      if (fullRes.os_instances) {
        fullRes.os_instances.forEach(os => {
          const exists = state.allOsInstances.find(o => o.id === os.id)
          if (!exists) {
            state.allOsInstances.push({ ...os, computerId: newId, computerName: fullRes.name })
          }
        })
      }
    }
  }

  async function deleteComputerById(id) {
    await api.deleteComputer(id)
    state.computers = state.computers.filter(c => c.id !== id)
    state.allHardware.cpus.forEach(c => { if (c.computerId === id) c.computerId = null })
    state.allHardware.rams.forEach(r => { if (r.computerId === id) r.computerId = null })
    state.allHardware.disks.forEach(d => { if (d.computerId === id) d.computerId = null })
    state.allOsInstances = state.allOsInstances.filter(os => os.computerId !== id)
  }

  // ==================== Hardware CRUD ====================
  async function saveHardware(type, form) {
    let payload
    if (type === 'cpu') {
      payload = {
        model: form.model,
        cores: form.cores,
        clock_speed: form.clockSpeed,
        purchase_date: form.purchaseDate,
        remarks: form.remarks,
        computer_id: null
      }
      const res = await api.createCpu(payload)
      state.allHardware.cpus.push({
        id: res.id,
        computerId: null,
        model: res.model,
        cores: res.cores,
        clockSpeed: res.clock_speed,
        purchaseDate: res.purchase_date,
        remarks: res.remarks
      })
    } else if (type === 'ram') {
      payload = {
        brand: form.brand,
        model: form.model,
        capacity_gb: form.capacity,
        ram_type: form.type,
        purchase_date: form.purchaseDate,
        remarks: form.remarks,
        computer_id: null
      }
      const res = await api.createRam(payload)
      state.allHardware.rams.push({
        id: res.id,
        computerId: null,
        brand: res.brand,
        model: res.model,
        capacity: res.capacity_gb,
        type: res.ram_type,
        purchaseDate: res.purchase_date,
        remarks: res.remarks
      })
    } else {
      payload = {
        brand: form.brand,
        model: form.model,
        capacity_gb: form.capacity,
        interface: form.interface,
        file_system: form.fileSystem,
        mount_method: form.mountMethod,
        purpose: form.purpose,
        is_boot_disk: form.isBootDisk,
        purchase_date: form.purchaseDate,
        computer_id: null
      }
      const res = await api.createDisk(payload)
      state.allHardware.disks.push({
        id: res.id,
        computerId: null,
        brand: res.brand,
        model: res.model,
        capacity: res.capacity_gb,
        interface: res.interface,
        fileSystem: res.file_system,
        mountMethod: res.mount_method,
        purpose: res.purpose,
        isBootDisk: res.is_boot_disk,
        purchaseDate: res.purchase_date
      })
    }
  }

  // ==================== Hardware Update ====================
  async function updateHardware(type, id, form) {
    if (type === 'cpu') {
      const payload = {
        model: form.model,
        cores: form.cores,
        clock_speed: form.clockSpeed,
        purchase_date: form.purchaseDate,
        remarks: form.remarks
      }
      await api.updateCpu(id, payload)
      const idx = state.allHardware.cpus.findIndex(c => c.id === id)
      if (idx >= 0) {
        state.allHardware.cpus[idx] = {
          ...state.allHardware.cpus[idx],
          model: form.model,
          cores: form.cores,
          clockSpeed: form.clockSpeed,
          purchaseDate: form.purchaseDate,
          remarks: form.remarks
        }
      }
    } else if (type === 'ram') {
      const payload = {
        brand: form.brand,
        model: form.model,
        capacity_gb: form.capacity,
        ram_type: form.type,
        purchase_date: form.purchaseDate,
        remarks: form.remarks
      }
      await api.updateRam(id, payload)
      const idx = state.allHardware.rams.findIndex(r => r.id === id)
      if (idx >= 0) {
        state.allHardware.rams[idx] = {
          ...state.allHardware.rams[idx],
          brand: form.brand,
          model: form.model,
          capacity: form.capacity,
          type: form.type,
          purchaseDate: form.purchaseDate,
          remarks: form.remarks
        }
      }
    } else {
      const payload = {
        brand: form.brand,
        model: form.model,
        capacity_gb: form.capacity,
        interface: form.interface,
        file_system: form.fileSystem,
        mount_method: form.mountMethod,
        purpose: form.purpose,
        is_boot_disk: form.isBootDisk,
        purchase_date: form.purchaseDate,
        remarks: form.remarks
      }
      await api.updateDisk(id, payload)
      const idx = state.allHardware.disks.findIndex(d => d.id === id)
      if (idx >= 0) {
        state.allHardware.disks[idx] = {
          ...state.allHardware.disks[idx],
          brand: form.brand,
          model: form.model,
          capacity: form.capacity,
          interface: form.interface,
          fileSystem: form.fileSystem,
          mountMethod: form.mountMethod,
          purpose: form.purpose,
          isBootDisk: form.isBootDisk,
          purchaseDate: form.purchaseDate,
          remarks: form.remarks
        }
      }
    }
  }

  async function deleteHardware(type, id) {
    if (type === 'cpu') {
      await api.deleteCpu(id)
      state.allHardware.cpus = state.allHardware.cpus.filter(c => c.id !== id)
    } else if (type === 'ram') {
      await api.deleteRam(id)
      state.allHardware.rams = state.allHardware.rams.filter(r => r.id !== id)
    } else {
      await api.deleteDisk(id)
      state.allHardware.disks = state.allHardware.disks.filter(d => d.id !== id)
    }
  }

  // ==================== OS Instance CRUD ====================
  async function saveOsInstance(computerId, form) {
    const res = await api.createOsInstance(computerId, {
      name: form.name,
      os_type: form.os_type,
      parent_os_id: form.parent_os_id || null,
      ip_address: form.ip_address,
      port: form.port,
      mac_address: form.mac_address,
      notes: form.notes
    })

    const computer = state.computers.find(c => c.id === computerId)
    const newOs = {
      id: res.id,
      computerId: computerId,
      computerName: computer?.name,
      name: res.name,
      type: res.os_type,
      ipAddress: res.ip_address,
      macAddress: res.mac_address,
      port: res.port,
      parentOsId: res.parent_os_id,
      notes: res.notes
    }
    state.allOsInstances.push(newOs)

    // Reload computer to get updated os_instances
    const fullRes = await api.getComputer(computerId)
    const idx = state.computers.findIndex(c => c.id === computerId)
    if (idx >= 0) state.computers[idx] = fullRes
  }

  async function updateOsInstanceById(id, form) {
    const res = await api.updateOsInstance(id, {
      name: form.name,
      os_type: form.os_type,
      parent_os_id: form.parent_os_id || null,
      ip_address: form.ip_address,
      mac_address: form.mac_address,
      notes: form.notes
    })
    const idx = state.allOsInstances.findIndex(os => os.id === id)
    if (idx >= 0) {
      state.allOsInstances[idx] = {
        ...state.allOsInstances[idx],
        name: res.name,
        type: res.os_type,
        ipAddress: res.ip_address,
        macAddress: res.mac_address,
        parentOsId: res.parent_os_id,
        notes: res.notes
      }
    }
  }

  async function deleteOsInstanceById(id) {
    // Find the os instance to get computerId before deleting
    const os = state.allOsInstances.find(o => o.id === id)
    const computerId = os?.computerId

    await api.deleteOsInstance(id)
    state.allOsInstances = state.allOsInstances.filter(o => o.id !== id)

    // Reload the computer to update its os_instances
    if (computerId) {
      const fullRes = await api.getComputer(computerId)
      const idx = state.computers.findIndex(c => c.id === computerId)
      if (idx >= 0) state.computers[idx] = fullRes
    }
  }

  // ==================== Service CRUD ====================
  async function saveService(osInstanceId, form, editingId = null) {
    if (editingId) {
      await api.updateService(editingId, form)
      const idx = state.services.findIndex(s => s.id === editingId)
      if (idx >= 0) Object.assign(state.services[idx], form)
    } else {
      const res = await api.createService(osInstanceId, form)
      state.services.push({ ...res, osInstanceId })
    }
  }

  async function deleteServiceById(id) {
    await api.deleteService(id)
    state.services = state.services.filter(s => s.id !== id)
  }

  // ==================== IP Group CRUD ====================
  async function saveIpGroup(form, editingId = null) {
    const payload = {
      name: form.name,
      subnet: form.subnet,
      startIp: form.startIp,
      endIp: form.endIp
    }

    if (editingId) {
      await api.updateIpGroup(editingId, payload)
      const idx = state.ipGroups.findIndex(g => g.id === editingId)
      if (idx >= 0) Object.assign(state.ipGroups[idx], payload)
    } else {
      const res = await api.createIpGroup(payload)
      state.ipGroups.push({ id: res.id, ...payload })
    }
  }

  async function deleteIpGroupById(id) {
    await api.deleteIpGroup(id)
    state.ipGroups = state.ipGroups.filter(g => g.id !== id)
  }

  // ==================== Type Config CRUD ====================
  async function addTypeConfig(category, name, color) {
    // 检查是否已存在同名配置
    if (state.typeConfigs.some(t => t.category === category && t.name === name)) {
      throw new Error('该配置项已存在')
    }
    const res = await api.createTypeConfig({ category, name, color: color || '#409EFF' })
    state.typeConfigs.push(res)
    return res
  }

  async function updateTypeConfigById(id, data) {
    // 检查是否与其他配置重名
    if (data.name && state.typeConfigs.some(t => t.id !== id && t.category === data.category && t.name === data.name)) {
      throw new Error('该配置项已存在')
    }
    await api.updateTypeConfig(id, data)
    const idx = state.typeConfigs.findIndex(t => t.id === id)
    if (idx >= 0) Object.assign(state.typeConfigs[idx], data)
  }

  async function deleteTypeConfigById(id) {
    await api.deleteTypeConfig(id)
    state.typeConfigs = state.typeConfigs.filter(t => t.id !== id)
  }

  // ==================== Export ====================
  function exportData() {
    const data = {
      version: 1,
      exportDate: new Date().toISOString(),
      typeConfigs: state.typeConfigs,
      ipGroups: state.ipGroups,
      computers: state.computers.map(c => ({
        id: c.id,
        name: c.name,
        location: c.location,
        remarks: c.remarks,
        cpuIds: c.cpuIds || [],
        ramIds: c.ramIds || [],
        diskIds: c.diskIds || []
      })),
      hardware: state.allHardware,
      osInstances: state.allOsInstances.map(os => {
        const computer = state.computers.find(c => c.id === os.computerId)
        return {
          id: os.id,
          computerId: os.computerId,
          computerName: computer?.name || '',
          name: os.name,
          type: os.type,
          ipAddress: os.ipAddress,
          macAddress: os.macAddress,
          port: os.port,
          parentOsId: os.parentOsId,
          notes: os.notes
        }
      }),
      services: state.services.map(s => {
        const osInstance = state.allOsInstances.find(o => o.id === s.osInstanceId)
        return {
          id: s.id,
          osInstanceId: s.osInstanceId,
          osInstanceName: osInstance?.name || '',
          name: s.name,
          type: s.type,
          protocol: s.protocol,
          ip_address: s.ip_address,
          port: s.port,
          description: s.description
        }
      })
    }
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `homelab-data-${new Date().toISOString().slice(0,10)}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  async function importData(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.onload = async (e) => {
        try {
          const data = JSON.parse(e.target.result)
          console.log('Importing data:', data)

          // Import type configs
          if (data.typeConfigs && Array.isArray(data.typeConfigs)) {
            for (const tc of data.typeConfigs) {
              const exists = state.typeConfigs.find(t => t.category === tc.category && t.name === tc.name)
              if (!exists) {
                await api.createTypeConfig({ category: tc.category, name: tc.name, color: tc.color })
              }
            }
          }

          // Import IP groups
          if (data.ipGroups && Array.isArray(data.ipGroups)) {
            for (const g of data.ipGroups) {
              const exists = state.ipGroups.find(t => t.name === g.name && t.subnet === g.subnet)
              if (!exists) {
                await api.createIpGroup({ name: g.name, subnet: g.subnet, startIp: g.startIp, endIp: g.endIp })
              }
            }
          }

          // Import computers first
          if (data.computers && Array.isArray(data.computers)) {
            for (const c of data.computers) {
              const exists = state.computers.find(t => t.name === c.name)
              if (!exists) {
                await api.createComputer({ name: c.name, location: c.location, remarks: c.remarks })
              }
            }
          }

          // Reload to get updated computer list with IDs
          await loadData()

          // Import hardware (CPU, RAM, Disk)
          if (data.hardware) {
            // Import CPUs
            if (data.hardware.cpus && Array.isArray(data.hardware.cpus)) {
              for (const cpu of data.hardware.cpus) {
                // Find computer by name if cpu has a computerId
                let computerId = null
                if (cpu.computerId && data.computers) {
                  const oldComputer = data.computers.find(c => c.id === cpu.computerId)
                  if (oldComputer) {
                    const newComputer = state.computers.find(c => c.name === oldComputer.name)
                    computerId = newComputer?.id
                  }
                }
                const exists = state.allHardware.cpus.find(h => h.model === cpu.model && h.computerId === computerId)
                if (!exists) {
                  await api.createCpu({
                    model: cpu.model,
                    cores: cpu.cores,
                    clockSpeed: cpu.clockSpeed,
                    purchaseDate: cpu.purchaseDate,
                    computer_id: computerId || null,
                    remarks: cpu.remarks
                  })
                }
              }
            }

            // Import RAMs
            if (data.hardware.rams && Array.isArray(data.hardware.rams)) {
              for (const ram of data.hardware.rams) {
                let computerId = null
                if (ram.computerId && data.computers) {
                  const oldComputer = data.computers.find(c => c.id === ram.computerId)
                  if (oldComputer) {
                    const newComputer = state.computers.find(c => c.name === oldComputer.name)
                    computerId = newComputer?.id
                  }
                }
                const exists = state.allHardware.rams.find(h => h.model === ram.model && h.capacity === ram.capacity)
                if (!exists) {
                  await api.createRam({
                    brand: ram.brand,
                    model: ram.model,
                    capacity_gb: ram.capacity,
                    ram_type: ram.type,
                    purchase_date: ram.purchaseDate,
                    computer_id: computerId || null,
                    remarks: ram.remarks
                  })
                }
              }
            }

            // Import Disks
            if (data.hardware.disks && Array.isArray(data.hardware.disks)) {
              for (const disk of data.hardware.disks) {
                let computerId = null
                if (disk.computerId && data.computers) {
                  const oldComputer = data.computers.find(c => c.id === disk.computerId)
                  if (oldComputer) {
                    const newComputer = state.computers.find(c => c.name === oldComputer.name)
                    computerId = newComputer?.id
                  }
                }
                const exists = state.allHardware.disks.find(h => h.model === disk.model && h.capacity === disk.capacity)
                if (!exists) {
                  await api.createDisk({
                    brand: disk.brand,
                    model: disk.model,
                    capacity_gb: disk.capacity,
                    interface: disk.interface,
                    file_system: disk.fileSystem,
                    mount_method: disk.mountMethod,
                    purpose: disk.purpose,
                    is_boot_disk: disk.isBootDisk,
                    purchase_date: disk.purchaseDate,
                    computer_id: computerId || null,
                    remarks: disk.remarks
                  })
                }
              }
            }
          }

          // Reload to get updated hardware
          await loadData()

          // Import OS instances
          if (data.osInstances && Array.isArray(data.osInstances)) {
            for (const os of data.osInstances) {
              // Check if already exists by name
              const exists = state.allOsInstances.find(o => o.name === os.name)
              if (!exists) {
                // Find the computer by name
                console.log('Looking for computer:', os.computerName, 'in', state.computers.map(c => c.name))
                const computer = state.computers.find(c => c.name === os.computerName)
                if (computer) {
                  await api.createOsInstance(computer.id, {
                    name: os.name,
                    os_type: os.type,
                    parent_os_id: os.parentOsId,
                    ip_address: os.ipAddress,
                    mac_address: os.macAddress,
                    port: os.port,
                    pcie_passthrough: os.pciePassthrough,
                    notes: os.notes
                  })
                } else {
                  console.warn('Computer not found for OS:', os.computerName)
                }
              }
            }
          }

          // Reload to get updated OS instances
          await loadData()

          // Import services
          if (data.services && Array.isArray(data.services)) {
            for (const svc of data.services) {
              // Find OS instance by name first, then by old ID
              let osInstance = state.allOsInstances.find(o => o.name === svc.osInstanceName)
              if (!osInstance && svc.osInstanceId) {
                // Try to find by old ID if name didn't match
                osInstance = state.allOsInstances.find(o => o.id === svc.osInstanceId)
              }
              if (osInstance) {
                const exists = state.services.find(s => s.name === svc.name && s.osInstanceId === osInstance.id)
                if (!exists) {
                  await api.createService(osInstance.id, {
                    name: svc.name,
                    type: svc.type,
                    protocol: svc.protocol,
                    ip_address: svc.ip_address,
                    port: svc.port,
                    description: svc.description
                  })
                }
              } else {
                console.warn('OS Instance not found for service:', svc.name, svc.osInstanceName)
              }
            }
          }

          // Final reload
          await loadData()
          resolve()
        } catch (err) {
          console.error('Import error:', err)
          reject(err)
        }
      }
      reader.onerror = () => reject(new Error('Failed to read file'))
      reader.readAsText(file)
    })
  }

  const store = {
    // State
    state,

    // Computed
    totalCpuCores,
    totalRam,
    totalDisk,
    totalVms,
    recentVms,
    osTypeConfigs,
    protocolConfigs,
    serviceTypeConfigs,

    // Data Loading
    loadData,

    // Helper Methods
    getComputerCpus,
    getComputerRams,
    getComputerDisks,
    getComputerOsInstances,
    getHostOsInstances,
    getOsInstanceById,
    getOsInstanceName,
    getOsServices,
    getProtocolColor,
    getVmTagType,

    // CRUD Operations
    saveComputer,
    deleteComputer: deleteComputerById,
    saveHardware,
    updateHardware,
    deleteHardware,
    saveOsInstance,
    updateOsInstance: updateOsInstanceById,
    deleteOsInstance: deleteOsInstanceById,
    saveService,
    deleteService: deleteServiceById,
    saveIpGroup,
    deleteIpGroup: deleteIpGroupById,
    addTypeConfig,
    updateTypeConfig: updateTypeConfigById,
    deleteTypeConfig: deleteTypeConfigById,

    // Export
    exportData,
    importData
  }

  provide(STORE_KEY, store)
  return store
}

export function useAppStore() {
  const store = inject(STORE_KEY)
  if (!store) {
    throw new Error('App store not provided. Make sure AppStore is installed.')
  }
  return store
}

export { STORE_KEY }
