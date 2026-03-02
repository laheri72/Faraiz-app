.PHONY: all setup backend frontend db up down tests clean

# Run entire stack via docker-compose
up:
	docker-compose up --build -d

# Stop entire stack
down:
	docker-compose down

# Local Development Commands
setup-backend:
	cd backend && pip install -r requirements.txt

setup-frontend:
	cd frontend && npm install

backend:
	cd backend && uvicorn app.main:app --reload --port 8000

frontend:
	cd frontend && npm run dev

# Testing
test-engine:
	cd backend && python tests/comprehensive_test.py
test-api:
	cd backend && python tests/verify_api.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "node_modules" -exec rm -rf {} +
