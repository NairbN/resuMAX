# syntax=docker/dockerfile:1
FROM node:20-alpine

WORKDIR /app

# Install dependencies (npm install to match your local workflow)
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the app (for non-mounted use). When developing with a bind mount, this can be overridden.
COPY . .

ENV NODE_ENV=development
ENV PORT=3000

EXPOSE 3000

# Start Next.js in dev mode, listening on all interfaces
CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0", "--port", "3000"]
