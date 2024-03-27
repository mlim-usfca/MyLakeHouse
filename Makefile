build-be:
	docker build -t caspian-back-end ./app

run-be:
	docker-compose up -d fastapi_app

stop-be:
	docker stop fastapi_app

remove-be:
	docker rm fastapi_app

remove-img:
	docker rmi caspian-back-end:latest

