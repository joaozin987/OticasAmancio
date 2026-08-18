<<<<<<< HEAD
FROM node:20-alpine AS builder
WORKDIR /app

# Install dependencies and build the app
COPY package*.json ./
RUN npm install --production=false
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app

# Install a small static server
RUN npm install -g serve

# Copy built static files
COPY --from=builder /app/dist ./dist

# Default port (Railway provides $PORT at runtime)
ENV PORT 3000
EXPOSE 3000

# Serve the built files and bind to the port provided by Railway
CMD ["sh", "-c", "serve -s dist -l tcp:$PORT"]
=======
# Use a lightweight Node image for development
FROM node:20-alpine AS base
WORKDIR /app

# Install dependencies first for better caching
COPY package*.json ./
RUN npm install

# Copy project files
COPY . .

# Expose Vite dev server port and start app on all interfaces
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
>>>>>>> 7f9f2fd095c463eb750ab97f4e8a09082e955d80
