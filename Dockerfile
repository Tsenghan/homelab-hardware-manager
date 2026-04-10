# ============================================
# Stage 1: Build frontend
# ============================================
FROM node:20-alpine AS frontend-builder

WORKDIR /app

# Copy package files
COPY frontend/package.json frontend/package-lock.json* ./

# Install dependencies
RUN npm install

# Copy frontend source
COPY frontend/ ./

# Build production assets
RUN npm run build

# ============================================
# Stage 2: Python backend
# ============================================
FROM python:3.11-slim AS backend

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

# Environment
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "wsgi:app"]
