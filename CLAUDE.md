# HomeLab 硬件资产管理系统

## 项目概述

硬件与虚拟化资产管理系统，支持物理主机、OS 实例、服务的管理和拓扑可视化。

## 技术栈

- **前端**: Vue 3 + Composition API + Vite + Element Plus + icon-park
- **后端**: Python Flask + Flask-SQLAlchemy + SQLite
- **部署**: Docker + Docker Compose + GitHub Actions

## 关键文件

| 文件 | 说明 |
|------|------|
| `backend/models.py` | SQLAlchemy 数据模型 |
| `backend/routes/` | Flask API 路由 |
| `frontend/src/stores/app.js` | Vue 前端状态管理 |
| `frontend/src/views/` | Vue 页面组件 |
| `docker-compose.yml` | Docker 部署配置 |

## 数据库

SQLite，文件位于 `backend/data/hardware.db`。启动时自动迁移和填充示例数据。

## gstack

本项目使用 [gstack](https://github.com/garrytan/gstack) 进行网页浏览和测试。

### 规则

- 对所有网页浏览操作使用 `/browse` 技能
- 永远不要使用 `mcp__claude-in-chrome__*` 工具

### 可用技能

- `/plan-ceo-review` - CEO 级别的计划审查
- `/plan-eng-review` - 工程计划审查
- `/review` - 代码审查
- `/ship` - 发布检查
- `/browse` - 网页浏览（使用 gstack）
- `/qa` - QA 测试
- `/setup-browser-cookies` - 设置浏览器 Cookie
- `/retro` - 回顾
