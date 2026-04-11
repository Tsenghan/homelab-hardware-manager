# HomeLab 硬件资产管理系统

<div align="center">

[![Stars](https://img.shields.io/github/stars/Tsenghan/homelab-hardware-manager?style=flat-square&logo=github)](https://github.com/Tsenghan/homelab-hardware-manager)
[![License](https://img.shields.io/github/license/Tsenghan/homelab-hardware-manager?style=flat-square)](https://github.com/Tsenghan/homelab-hardware-manager/blob/main/LICENSE)
[![Docker](https://img.shields.io/docker/pulls/tsenghan/homelab-hardware-manager?style=flat-square&logo=docker)](https://github.com/Tsenghan/homelab-hardware-manager)

*专为个人及 HomeLab 场景设计的硬件与虚拟化资产管理系统*

**中文 | [English Version](README_en.md)**

</div>

---

## 功能特性

### 核心管理

| 功能 | 说明 |
|------|------|
| **物理主机管理** | 添加、编辑、删除物理服务器，关联位置与备注信息 |
| **硬件库** | 统一管理未分配的 CPU、内存、硬盘，支持批量录入与克隆 |
| **OS 实例** | 支持 PVE/ESXi/Linux/Windows/LXC 等类型，可嵌套展示 VM/LXC |
| **服务管理** | 管理端口、协议、服务地址，一键跳转访问 |

### 可视化与交互

| 功能 | 说明 |
|------|------|
| **拓扑视图** | 树形结构展示 `物理机 → OS实例 → 服务` 的完整层级关系 |
| **全局搜索** | 跨层级模糊匹配，支持服务名、IP、硬件型号等快速定位 |
| **抽屉式详情** | 点击节点右侧滑出详情面板，保持上下文不丢失 |
| **IP 网络视图** | 按分组展示 IP 分配情况，直观管理地址段 |
| **配置管理** | 自定义 OS 类型和服务协议的名称与配色方案 |

### 数据模型（三层结构）

```
L1 硬件层     → Computer / CPU / RAM / Disk
L2 系统层     → OsInstance（支持嵌套 VM/LXC）
L3 应用层     → Service
```

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端框架 | Vue 3 + Composition API + Vite |
| UI 组件 | Element Plus |
| 后端框架 | Python Flask + Flask-SQLAlchemy |
| 数据库 | SQLite |
| 部署 | Docker + Docker Compose |

---

## 快速开始

### 方式一：Docker 部署（推荐）

```bash
git clone https://github.com/Tsenghan/homelab-hardware-manager.git
cd homelab-hardware-manager
docker-compose up -d
```

访问 **http://your-server:5000** 即可。

> 镜像自动从 Docker Hub 拉取，每次更新后重启容器即可使用最新版本。

---

### 方式二：本地开发

**前端**

```bash
cd frontend
npm install
npm run dev
```

**后端**（另起终端）

```bash
cd backend
pip install -r requirements.txt
python main.py
```

访问 **http://localhost:5173**，Vite 自动代理 `/api` 到 Flask。

---

## 部署指南

### Docker Compose

```bash
# 启动
docker-compose up -d

# 更新（拉取最新镜像）
docker-compose pull && docker-compose up -d

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止
docker-compose down
```

### 数据持久化

数据库文件存储在 `data/` 目录（主机挂载），确保数据不丢失。

### 初始化数据

首次启动时，系统会自动创建数据库表并写入示例数据（示例主机 PVE-Server-1、IP 分组、OS 类型、协议配置等）。

如需重新初始化，删除 `data/` 目录后重启容器即可：
```bash
rm -rf data && docker-compose up -d
```

---

## 项目结构

```
homelab-hardware-manager/
├── frontend/
│   ├── src/
│   │   ├── views/          # 页面组件
│   │   ├── components/      # 公共组件
│   │   │   └── details/     # 详情抽屉组件
│   │   ├── stores/          # 状态管理
│   │   └── api/             # API 接口封装
│   ├── public/
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── backend/
│   ├── routes/              # API 路由
│   │   ├── computers.py
│   │   ├── os_instances.py
│   │   ├── services.py
│   │   ├── search.py
│   │   ├── ip_groups.py
│   │   └── type_configs.py
│   ├── main.py              # Flask 入口
│   ├── models.py            # 数据模型
│   └── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── wsgi.py
└── nginx.conf               # 可选：配合 Nginx 反向代理
```

---

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/computers` | 获取主机列表 |
| POST | `/api/computers` | 创建主机 |
| PUT | `/api/computers/<id>` | 更新主机 |
| DELETE | `/api/computers/<id>` | 删除主机 |
| GET | `/api/os-instances` | 获取 OS 实例列表 |
| POST | `/api/os-instances` | 创建 OS 实例 |
| GET | `/api/services` | 获取服务列表 |
| POST | `/api/services` | 创建服务 |
| GET | `/api/storage` | 获取存储池列表 |
| GET | `/api/search?q=` | 全局搜索 |
| GET | `/api/ip-groups` | 获取 IP 分组 |
| POST | `/api/ip-groups` | 创建 IP 分组 |
| GET | `/api/type-configs` | 获取配置项（OS 类型/协议） |
| POST | `/api/type-configs` | 创建配置项 |

---

## 参与开发

### 开发环境要求

- Node.js >= 18
- Python >= 3.10
- Docker & Docker Compose（可选）

### 开发流程

1. **Fork & Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/homelab-hardware-manager.git
   cd homelab-hardware-manager
   ```

2. **安装前端依赖**
   ```bash
   cd frontend
   npm install
   ```

3. **启动后端开发服务器**
   ```bash
   cd backend
   pip install -r requirements.txt
   python main.py
   ```

4. **启动前端开发服务器**
   ```bash
   cd frontend
   npm run dev
   ```

5. **提交规范**

   - `feat:` 新功能
   - `fix:` Bug 修复
   - `refactor:` 重构
   - `style:` 样式/格式调整
   - `docs:` 文档变更

   ```bash
   git checkout -b feat/your-feature-name
   git commit -m "feat: add new feature"
   git push origin feat/your-feature-name
   ```

6. **提交 Pull Request**

---

## 许可证

本项目基于 [MIT License](LICENSE) 开源。

---

## 求 Star ⭐

如果这个项目对你有帮助，请帮我点一个 Star！你的支持是我持续维护的动力。

[![Star](https://img.shields.io/github/stars/Tsenghan/homelab-hardware-manager?style=social&logo=github)](https://github.com/Tsenghan/homelab-hardware-manager)

---

## 关于 AI

本项目从零到一完全由 AI 构建，代码、架构设计与文档均借助 AI 辅助完成。

感谢 **Claude Code (Anthropic)** 和 **MiniMax M2.7** 的协助。
