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
