.PHONY: dev-backend dev-frontend dev test deploy-backend deploy-frontend

dev-backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	cd frontend && npm run dev

dev:
	docker-compose up --build

test:
	cd backend && pytest tests/ -v

deploy-backend:
	cd infrastructure/terraform && terraform apply -target=google_cloud_run_v2_service.backend -auto-approve

deploy-frontend:
	cd infrastructure/terraform && terraform apply -target=google_cloud_run_v2_service.frontend -auto-approve
