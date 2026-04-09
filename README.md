# HomeLab 硬件资产管理系统

专为个人及 HomeLab 场景设计的硬件与虚拟化资产管理系统。

## 技术栈

- **前端**: Vue 3 + Vite + Element Plus
- **后端**: Python Flask + SQLite
- **部署**: Docker + Docker Compose

## 功能特性

- **拓扑视图**: 树形结构展示 物理机 → 系统 → 服务 层级
- **物理主机管理**: 添加、编辑、分配硬件
- **硬件库**: 统一管理未分配的 CPU、内存、硬盘
- **服务管理**: 端口、协议、访问链接
- **IP 网络视图**: 按分组展示 IP 分配情况
- **配置管理**: OS 类型和服务协议的配色管理

## 本地开发

### 前端

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:5173

### 后端

```bash
cd backend
pip install -r requirements.txt
python main.py
```

API 服务运行在 http://localhost:5000

## Docker 生产部署

### 方式一：Docker Compose（推荐）

```bash
# 拉取并启动
docker-compose up -d

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

访问 http://your-server:5000

### 方式二：手动构建

```bash
# 构建镜像
docker build -t homelab-manager .

# 运行容器
docker run -d \
  --name homelab \
  -p 5000:5000 \
  -v homelab-data:/app/backend/data \
  homelab-manager
```

## 数据持久化

数据库文件存储在 Docker volume `homelab-data` 中，可通过以下命令查看：

```bash
# 查看 volume 路径
docker volume inspect homelab-manager_homelab-data
```

## 项目结构

```
homelab-manager/
├── frontend/              # Vue 3 前端
│   ├── src/
│   │   ├── views/        # 页面组件
│   │   ├── components/  # 公共组件
│   │   ├── stores/      # 状态管理
│   │   └── api/          # API 接口
│   └── vite.config.js
├── backend/              # Flask 后端
│   ├── routes/           # API 路由
│   ├── models.py         # 数据模型
│   ├── main.py           # 应用入口
│   └── init_db.py         # 数据库初始化
├── dist/                  # 前端构建产物（自动生成）
├── Dockerfile
├── docker-compose.yml
└── wsgi.py
```

## API 接口

| 接口 | 说明 |
|------|------|
| GET /api/computers | 获取主机列表 |
| POST /api/computers | 创建主机 |
| GET /api/type-configs | 获取配置列表 |
| ... | 更多接口见后端代码 |

## 初始化示例数据

首次启动后，如需加载示例数据：

```bash
# 进入后端目录
docker exec -it homelab-manager_homelab-1 python -c "
from backend.main import create_app
from backend.init_db import load_example_data
app = create_app()
with app.app_context():
    load_example_data()
"
```

或者直接运行初始化脚本后重启：

```bash
cd backend
python init_db.py
```

## 注意事项

- 数据库使用 SQLite，存储在 `/app/backend/data/hardware.db`
- 首次启动会自动创建数据库表结构
- 前端静态文件由 Flask 直接服务，无需额外 nginx 配置
