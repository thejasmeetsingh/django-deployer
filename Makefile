create-network:
	docker network create -d bridge shared-network

start-services:
	# Admin App
	docker-compose -f src/services/admin/docker-compose.yml up -d
	
	# API Gateway
	docker run --name api_gateway -d -p 8000:8000 \
		-v ./src/api_gateway/nginx.conf:/etc/nginx/conf.d/default.conf \
		--network shared-network nginx:1.25.4-alpine

stop-services:
	# Admin App
	docker-compose -f src/services/admin/docker-compose.yml down
	
	# API Gateway
	docker container stop api_gateway
	docker container rm api_gateway
