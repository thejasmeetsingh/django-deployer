up:

	docker network create -d bridge shared-network

	docker run -d --name rmq_service \
		-e RABBITMQ_DEFAULT_USER=queue_user \
		-e RABBITMQ_DEFAULT_PASS=1234 \
		--network=shared-network rabbitmq:3.13.2-alpine

	docker-compose -f src/services/admin/docker-compose.yml up -d

	docker-compose -f src/services/user/docker-compose.yml up -d
	
	docker-compose -f src/services/deployer/docker-compose.yml up -d

	docker run --name api_gateway -d -p 80:80 \
		-v ./src/api_gateway/nginx.conf:/etc/nginx/conf.d/default.conf \
		--network shared-network nginx:1.25.4-alpine

down:

	docker-compose -f src/services/admin/docker-compose.yml down --remove-orphans

	docker-compose -f src/services/user/docker-compose.yml down --remove-orphans

	docker-compose -f src/services/deployer/docker-compose.yml down --remove-orphans

	docker container stop rmq_service
	docker container rm rmq_service
	
	docker container stop api_gateway
	docker container rm api_gateway

	docker network rm shared-network
