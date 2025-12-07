BACKEND_DIR=apps/api

.PHONY: backend
backend:
	./scripts/run_api.sh

.PHONY: frontend
frontend:
	FRONTEND_MOCK=true ./scripts/run_frontend.sh

.PHONY: test-backend
test-backend:
	./scripts/test_api.sh

.PHONY: dev
dev:
	./scripts/run_full.sh

.PHONY: test-frontend
test-frontend:
	./scripts/test_frontend.sh

.PHONY: test
test:
	./scripts/test_full.sh

.PHONY: setup-backend
setup-backend:
	./scripts/setup_backend.sh

.PHONY: setup-frontend
setup-frontend:
	./scripts/setup_frontend.sh

.PHONY: setup
setup:
	./scripts/setup_full.sh

.PHONY: docker-build
docker-build:
	./scripts/docker_build.sh

.PHONY: docker-up
docker-up:
	./scripts/docker_up.sh
