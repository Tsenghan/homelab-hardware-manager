import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

api.interceptors.request.use(config => config)

api.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// ==================== Computer ====================
export const getComputers = () => api.get('/computers')
export const getComputer = (id) => api.get(`/computers/${id}`)
export const createComputer = (data) => api.post('/computers', data)
export const updateComputer = (id, data) => api.put(`/computers/${id}`, data)
export const deleteComputer = (id) => api.delete(`/computers/${id}`)

// ==================== CPU ====================
export const getAllCpus = () => api.get('/cpus')
export const createCpu = (data) => api.post('/cpus', data)
export const updateCpu = (id, data) => api.put(`/cpus/${id}`, data)
export const deleteCpu = (id) => api.delete(`/cpus/${id}`)

// ==================== RAM ====================
export const getAllRams = () => api.get('/rams')
export const createRam = (data) => api.post('/rams', data)
export const updateRam = (id, data) => api.put(`/rams/${id}`, data)
export const deleteRam = (id) => api.delete(`/rams/${id}`)

// ==================== Disk ====================
export const getAllDisks = () => api.get('/disks')
export const createDisk = (data) => api.post('/disks', data)
export const updateDisk = (id, data) => api.put(`/disks/${id}`, data)
export const deleteDisk = (id) => api.delete(`/disks/${id}`)

// ==================== OS Instance ====================
export const getOsInstances = (computerId) => api.get(`/computers/${computerId}/os-instances`)
export const getOsInstance = (id) => api.get(`/os-instances/${id}`)
export const createOsInstance = (computerId, data) => api.post(`/computers/${computerId}/os-instances`, data)
export const updateOsInstance = (id, data) => api.put(`/os-instances/${id}`, data)
export const deleteOsInstance = (id) => api.delete(`/os-instances/${id}`)

// ==================== Service ====================
export const getServices = (osInstanceId) => api.get(`/os-instances/${osInstanceId}/services`)
export const createService = (osInstanceId, data) => api.post(`/os-instances/${osInstanceId}/services`, data)
export const updateService = (id, data) => api.put(`/services/${id}`, data)
export const deleteService = (id) => api.delete(`/services/${id}`)

// ==================== IP Group ====================
export const getIpGroups = () => api.get('/ip-groups')
export const createIpGroup = (data) => api.post('/ip-groups', data)
export const updateIpGroup = (id, data) => api.put(`/ip-groups/${id}`, data)
export const deleteIpGroup = (id) => api.delete(`/ip-groups/${id}`)

// ==================== Type Config ====================
export const getTypeConfigs = () => api.get('/type-configs')
export const createTypeConfig = (data) => api.post('/type-configs', data)
export const updateTypeConfig = (id, data) => api.put(`/type-configs/${id}`, data)
export const deleteTypeConfig = (id) => api.delete(`/type-configs/${id}`)

export default api
