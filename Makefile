create-network:
	docker network create -d bridge shared-network

start-services:
	# RabbitMQ
	docker run -d --name rmq_service -e RABBITMQ_DEFAULT_USER=queue_user -e RABBITMQ_DEFAULT_PASS=1234 --network=shared-network rabbitmq:3.13.2-alpine

	# Admin App
	docker-compose -f src/services/admin/docker-compose.yml up -d

	# User App
	docker-compose -f src/services/user/docker-compose.yml up -d
	
	# Deployer App
	docker-compose -f src/services/deployer/docker-compose.yml up -d

	# API Gateway
	docker run --name api_gateway -d -p 8000:8000 \
		-v ./src/api_gateway/nginx.conf:/etc/nginx/conf.d/default.conf \
		--network shared-network nginx:1.25.4-alpine

stop-services:
	# Admin App
	docker-compose -f src/services/admin/docker-compose.yml down --remove-orphans

	# User App
	docker-compose -f src/services/user/docker-compose.yml down --remove-orphans

	# Deployer App
	docker-compose -f src/services/deployer/docker-compose.yml down --remove-orphans

	# RabbitMQ
	docker container stop rmq_service
	docker container rm rmq_service
	
	# API Gateway
	docker container stop api_gateway
	docker container rm api_gateway
