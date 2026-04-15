# ============================================
# Build arguments
# ============================================
ARG VERSION=1.0.1

# ============================================
# Stage 1: Build frontend
# ============================================
FROM node:22-alpine AS frontend-builder

ARG VERSION

WORKDIR /app

# Copy package files
COPY frontend/package.json frontend/package-lock.json* ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy frontend source
COPY frontend/ ./

# Build production assets (npm_package_version 自动注入)
RUN npm run build

# ============================================
# Stage 2: Python backend
# ============================================
FROM python:3.11-slim AS backend

ARG VERSION

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

# Copy backend source
COPY backend/ ./backend/
COPY wsgi.py .

# Copy built frontend from stage 1
COPY --from=frontend-builder /app/dist ./dist

# Create data directory for SQLite
RUN mkdir -p backend/data

# Labels
LABEL version="${VERSION}"
LABEL description="Homelab 硬件资产管理系统"

# Environment
ENV PYTHONUNBUFFERED=1
ENV APP_VERSION=${VERSION}

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "wsgi:app"]
