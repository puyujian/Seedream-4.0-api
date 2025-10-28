# Build stage - Build frontend
ARG NODE_VERSION=20
ARG NGINX_VERSION=1.27-alpine
FROM node:${NODE_VERSION}-alpine AS frontend-build

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies with clean cache
RUN npm ci --ignore-scripts && \
    npm cache clean --force

# Copy source code
COPY frontend/ ./

# Build the application
RUN npm run build

# Production stage - Nginx for serving frontend and proxying to backend
ARG NGINX_VERSION=1.27-alpine
FROM nginx:${NGINX_VERSION}

# Copy nginx configuration
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Copy built frontend from build stage
COPY --from=frontend-build /app/dist /usr/share/nginx/html

# Create nginx cache directories
RUN mkdir -p /var/cache/nginx/client_temp && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /usr/share/nginx/html

# Expose port
EXPOSE 80

# Health check (wget provided by BusyBox in base image)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:80 || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
