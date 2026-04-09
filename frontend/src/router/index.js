import { createRouter, createWebHistory } from 'vue-router'
import Topology from '../views/Topology.vue'
import ComputerList from '../views/ComputerList.vue'
import HardwarePool from '../views/HardwarePool.vue'
import ServiceList from '../views/ServiceList.vue'
import NetworkView from '../views/NetworkView.vue'
import Settings from '../views/Settings.vue'

const routes = [
  { path: '/', name: 'Topology', component: Topology },
  { path: '/topology', redirect: '/' },
  { path: '/computers', name: 'Computers', component: ComputerList },
  { path: '/hardware', name: 'Hardware', component: HardwarePool },
  { path: '/services', name: 'Services', component: ServiceList },
  { path: '/network', name: 'Network', component: NetworkView },
  { path: '/settings', name: 'Settings', component: Settings }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
