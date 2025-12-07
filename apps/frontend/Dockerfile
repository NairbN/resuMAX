FROM node:22-alpine AS base
WORKDIR /app

# Enable pnpm via corepack
RUN corepack enable

# Build args for env wiring at build time
ARG NEXT_PUBLIC_API_BASE=http://localhost:8000
ARG NEXT_PUBLIC_USE_AUTH_MOCK=false

COPY apps/frontend/package.json apps/frontend/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY apps/frontend /app

# Regenerate .env.local for the container build to ensure correct env at build time
RUN echo "NEXT_PUBLIC_API_BASE=${NEXT_PUBLIC_API_BASE}" > .env.local && \
    echo "NEXT_PUBLIC_USE_AUTH_MOCK=${NEXT_PUBLIC_USE_AUTH_MOCK}" >> .env.local

RUN pnpm build

EXPOSE 3000

CMD ["pnpm", "start", "-H", "0.0.0.0", "-p", "3000"]
