# Frontend Dev Container Guide

This project ships with a dev-friendly Dockerfile that runs `npm run dev` inside a container. Use it if you prefer Docker over a local Node setup.

## Prerequisites
- Docker installed
- (Optional) `.env.local` with any frontend env vars, e.g.:
  ```
  NEXT_PUBLIC_USE_MOCK_AUTH=true
  ```

## Build the dev image
From the `frontend/` directory:
```sh
docker build -t resumax-frontend-dev .
```

## Run the dev server in Docker
### Quick run (no mounts, defaults)
```sh
docker run -p 3000:3000 resumax-frontend-dev
```
- App available at http://localhost:3000
- Uses defaults baked into the image (no env overrides, code inside image)

### With env vars
Pass env vars inline:
```sh
docker run -p 3000:3000 -e NEXT_PUBLIC_USE_MOCK_AUTH=true resumax-frontend-dev
```
Or use an env file (recommended if multiple vars):
```sh
docker run -p 3000:3000 --env-file .env.local resumax-frontend-dev
```

### With live code changes (bind mount)
Mount your working directory so code changes reflect without rebuilding:
```sh
docker run -p 3000:3000 -v "$PWD":/app resumax-frontend-dev
```
Combine with env vars:
```sh
docker run -p 3000:3000 \
  -v "$PWD":/app \
  --env-file .env.local \
  resumax-frontend-dev
```

## Notes
- The dev container uses `npm install` (matches local workflow) and runs `npm run dev` binding to `0.0.0.0:3000`.
- `.env*` files are ignored in the image; you must pass env vars at runtime.
- Stop the container with `Ctrl+C` or `docker stop <container_id>`.
