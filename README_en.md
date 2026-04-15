# HomeLab Hardware Asset Manager

<div align="center">

[![Stars](https://img.shields.io/github/stars/Tsenghan/homelab-hardware-manager?style=flat-square&logo=github)](https://github.com/Tsenghan/homelab-hardware-manager)
[![License](https://img.shields.io/github/license/Tsenghan/homelab-hardware-manager?style=flat-square)](https://github.com/Tsenghan/homelab-hardware-manager/blob/main/LICENSE)
[![Docker](https://img.shields.io/docker/pulls/tsenghan/homelab-manager?style=flat-square&logo=docker)](https://hub.docker.com/r/tsenghan/homelab-manager)

*A hardware and virtualization asset management system designed for personal HomeLab environments.*

**[中文](README.md) | [English](README_en.md)**

</div>

---

## Features

### Core Management

| Feature | Description |
|---------|-------------|
| **Physical Host Management** | Add, edit, delete physical servers with location and notes |
| **Hardware Pool** | Unified management of unassigned CPU, RAM, disk; support batch entry |
| **OS Instances** | Support PVE/ESXi/Linux/Windows/LXC with nested VM/LXC display |
| **Services** | Manage ports, protocols, service URLs with one-click access |

### Visualization & Interaction

| Feature | Description |
|---------|-------------|
| **Topology View** | Tree structure: `Physical Host → OS Instance → VM/LXC → Service` |
| **Global Search** | Cross-layer fuzzy search — find by service name, IP, hardware model, etc. |
| **Drawer Panel** | Slide-out detail panel on node click, never loses context |
| **IP Network View** | IP allocation overview by group |
| **Settings** | Customize OS type, protocol, and service type color schemes |

### Data Model

```
L1 Hardware    → Computer / CPU / RAM / Disk
L2 System      → OsInstance (supports nested VM/LXC)
L3 Application → Service
```

---

## Screenshots

| Topology View | IP List |
|:---:|:---:|
| ![Topology View](screenshots/PixPin_2026-04-11_22-06-59.png) | ![IP List](screenshots/PixPin_2026-04-11_22-07-24.png) |

| Services | Settings |
|:---:|:---:|
| ![Services](screenshots/PixPin_2026-04-11_22-08-21.png) | ![Settings](screenshots/PixPin_2026-04-11_22-08-42.png) |

---

## Quick Start

### Docker (Recommended)

```bash
git clone https://github.com/Tsenghan/homelab-hardware-manager.git
cd homelab-hardware-manager
docker-compose up -d
```

Visit **http://your-server:5000**

> Sample data is created automatically on first startup.

### Local Development

**Frontend**
```bash
cd frontend
npm install --legacy-peer-deps
npm run dev
```

**Backend** (separate terminal)
```bash
cd backend
pip install -r requirements.txt
python main.py
```

Visit **http://localhost:5173**, Vite proxies `/api` to Flask.

---

## Deployment

### Docker Compose

```bash
docker-compose up -d      # Start
docker-compose pull       # Pull latest
docker-compose up -d      # Update and restart
docker-compose logs -f    # View logs
docker-compose down       # Stop
```

### Data Persistence

Database file is stored in `data/` directory (host mount). Delete this directory and restart to reinitialize.

---

## Project Structure

```
homelab-hardware-manager/
├── frontend/
│   ├── src/
│   │   ├── views/          # Page components
│   │   ├── components/      # Shared components
│   │   │   └── details/     # Detail drawer components
│   │   ├── stores/         # State management
│   │   ├── api/            # API wrappers
│   │   └── router/         # Router config
│   ├── public/
│   └── vite.config.js
├── backend/
│   ├── routes/             # API routes
│   │   ├── computers.py
│   │   ├── os_instances.py
│   │   ├── services.py
│   │   ├── ip_groups.py
│   │   ├── search.py
│   │   └── type_configs.py
│   ├── main.py             # Flask entry point
│   ├── models.py           # Data models
│   ├── init_db.py          # Database initialization
│   └── requirements.txt
├── screenshots/            # UI screenshots
├── docker-compose.yml
└── nginx.conf              # Optional Nginx reverse proxy config
```

---

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/computers` | List hosts |
| POST | `/api/computers` | Create host |
| PUT | `/api/computers/<id>` | Update host |
| DELETE | `/api/computers/<id>` | Delete host |
| GET | `/api/os-instances` | List OS instances |
| POST | `/api/os-instances` | Create OS instance |
| DELETE | `/api/os-instances/<id>` | Delete OS instance |
| GET | `/api/services` | List services |
| POST | `/api/services` | Create service |
| PUT | `/api/services/<id>` | Update service |
| DELETE | `/api/services/<id>` | Delete service |
| GET | `/api/ip-groups` | List IP groups |
| POST | `/api/ip-groups` | Create IP group |
| PUT | `/api/ip-groups/<id>` | Update IP group |
| DELETE | `/api/ip-groups/<id>` | Delete IP group |
| GET | `/api/type-configs` | List type configs |
| POST | `/api/type-configs` | Create type config |
| GET | `/api/search?q=` | Global search |
| POST | `/api/import` | Import data |
| GET | `/api/export` | Export data |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Vue 3 + Composition API + Vite + Element Plus + icon-park |
| Backend | Python Flask + Flask-SQLAlchemy |
| Database | SQLite |
| Deployment | Docker + Docker Compose |

---

## Contributing

### Prerequisites

- Node.js >= 18
- Python >= 3.10
- Docker & Docker Compose (optional)

### Development

1. Fork & Clone
2. Install deps: `cd frontend && npm install --legacy-peer-deps`
3. Start backend: `cd backend && pip install -r requirements.txt && python main.py`
4. Start frontend: `cd frontend && npm run dev`
5. Commit convention: `feat:` `fix:` `refactor:` `style:` `docs:`

---

## License

[MIT License](LICENSE)

---

## About AI

This project was built from scratch with AI assistance.

Special thanks to **Claude Code (Anthropic)** and **MiniMax M2.7**.
