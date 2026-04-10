# HomeLab Hardware Asset Manager

<div align="center">

[![Stars](https://img.shields.io/github/stars/Tsenghan/homelab-hardware-manager?style=flat-square&logo=github)](https://github.com/Tsenghan/homelab-hardware-manager)
[![License](https://img.shields.io/github/license/Tsenghan/homelab-hardware-manager?style=flat-square)](https://github.com/Tsenghan/homelab-hardware-manager/blob/main/LICENSE)
[![Docker](https://img.shields.io/docker/pulls/tsenghan/homelab-hardware-manager?style=flat-square&logo=docker)](https://github.com/Tsenghan/homelab-hardware-manager)

*A hardware and virtualization asset management system designed for personal HomeLab environments.*

**[中文](README.md) | English**

</div>

---

## Features

### Core Management

| Feature | Description |
|---------|-------------|
| **Physical Host Management** | Add, edit, and delete physical servers with location and notes |
| **Hardware Pool** | Manage unassigned CPUs, RAM modules, and disks; support batch entry and cloning |
| **OS Instances** | Support PVE/ESXi/Linux/Windows/LXC, nested VM/LXC display |
| **Services** | Manage ports, protocols, and service URLs with one-click access |

### Visualization & Interaction

| Feature | Description |
|---------|-------------|
| **Topology View** | Tree structure: `Physical Host → OS Instance → Service` |
| **Global Search** | Cross-layer fuzzy search — find by service name, IP, hardware model, etc. |
| **Drawer Panel** | Slide-out detail panel on node click, never loses context |
| **IP Network View** | IP allocation overview by group with address range management |
| **Settings** | Customize OS type names and protocol color schemes |

### Data Model (3-Layer Architecture)

```
L1 Hardware       → Computer / CPU / RAM / Disk
L2 System         → OsInstance (supports nested VM/LXC)
L3 Application    → Service
```

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend Framework | Vue 3 + Composition API + Vite |
| UI Components | Element Plus |
| Backend Framework | Python Flask + Flask-SQLAlchemy |
| Database | SQLite |
| Deployment | Docker + Docker Compose |

---

## Quick Start

### Option 1: Docker (Recommended for Production)

```bash
git clone https://github.com/Tsenghan/homelab-hardware-manager.git
cd homelab-hardware-manager
docker-compose up -d
```

Visit **http://your-server:5000**

---

### Option 2: Local Development

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

**Backend** (in a separate terminal)

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Visit **http://localhost:5173**, Vite proxies `/api` requests to Flask automatically.

---

## Deployment

### Docker Compose (Production)

```bash
# Start
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Manual Docker

```bash
docker build -t homelab-manager .
docker run -d --name homelab -p 5000:5000 homelab-manager
```

### Data Persistence

Database is stored in Docker volume `homelab-data`:

```bash
docker volume inspect homelab-hardware-manager_homelab-data
```

### Seed Data

On first startup, the system automatically creates database tables and populates sample data (example host PVE-Server-1, IP groups, OS types, protocol configs, etc.).

To manually re-initialize, simply restart the container — `seed_data_if_empty()` will run automatically.

---

## Project Structure

```
homelab-hardware-manager/
├── frontend/
│   ├── src/
│   │   ├── views/          # Page components
│   │   ├── components/      # Shared components
│   │   │   └── details/     # Detail drawer components
│   │   ├── stores/          # State management
│   │   └── api/             # API wrappers
│   ├── public/
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── backend/
│   ├── routes/             # API routes
│   │   ├── computers.py
│   │   ├── os_instances.py
│   │   ├── services.py
│   │   ├── search.py
│   │   ├── ip_groups.py
│   │   └── type_configs.py
│   ├── main.py             # Flask entry point
│   ├── models.py           # Data models
│   └── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── wsgi.py
└── nginx.conf              # Optional: Nginx reverse proxy config
```

---

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/computers` | List all hosts |
| POST | `/api/computers` | Create a host |
| PUT | `/api/computers/<id>` | Update a host |
| DELETE | `/api/computers/<id>` | Delete a host |
| GET | `/api/os-instances` | List OS instances |
| POST | `/api/os-instances` | Create an OS instance |
| GET | `/api/services` | List services |
| POST | `/api/services` | Create a service |
| GET | `/api/storage` | List storage pools |
| GET | `/api/search?q=` | Global search |
| GET | `/api/ip-groups` | List IP groups |
| POST | `/api/ip-groups` | Create an IP group |
| GET | `/api/type-configs` | List type configs (OS types / protocols) |
| POST | `/api/type-configs` | Create a type config |

---

## Contributing

### Prerequisites

- Node.js >= 18
- Python >= 3.10
- Docker & Docker Compose (optional)

### Development Workflow

1. **Fork & Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/homelab-hardware-manager.git
   cd homelab-hardware-manager
   ```

2. **Install Frontend Dependencies**
   ```bash
   cd frontend
   npm install
   ```

3. **Start Backend Dev Server**
   ```bash
   cd backend
   pip install -r requirements.txt
   python main.py
   ```

4. **Start Frontend Dev Server**
   ```bash
   cd frontend
   npm run dev
   ```

5. **Commit Convention**

   - `feat:` New feature
   - `fix:` Bug fix
   - `refactor:` Refactoring
   - `style:` Style/format adjustment
   - `docs:` Documentation change

   ```bash
   git checkout -b feat/your-feature-name
   git commit -m "feat: add new feature"
   git push origin feat/your-feature-name
   ```

6. **Open a Pull Request**

---

## License

This project is open source under the [MIT License](LICENSE).

---

## Please Star ⭐

If this project is helpful to you, please give it a Star! Your support drives my motivation to keep improving.

[![Star](https://img.shields.io/github/stars/Tsenghan/homelab-hardware-manager?style=social&logo=github)](https://github.com/Tsenghan/homelab-hardware-manager)

---

## About AI

This project was built entirely from scratch with AI assistance — code, architecture, and documentation all created with the help of AI.

Special thanks to **Claude Code (Anthropic)** and **MiniMax M2.7**.
