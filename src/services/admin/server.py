try:
    import os
    import sys
    from concurrent import futures

    import grpc
    import django
    from dotenv import load_dotenv

    load_dotenv()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

    project_path = os.getenv('DJANGO_PROJECT_FULL_PATH')
    if project_path:
        sys.path.extend([project_path])
        if 'setup' in dir(django):
            django.setup()
    else:
        raise ImportError('DJANGO_PROJECT_FULL_PATH environment variable not set.')

except ModuleNotFoundError as e:
    print("Error: ", e)
    sys.exit(1)

try:
    from app.models import DeploymentPlan
    from app.grpc import deployment_plan_pb2, deployment_plan_pb2_grpc
except ModuleNotFoundError as e:
    print("Error: ", e)
    sys.exit(1)


GRPC_PORT = os.getenv('GRPC_PORT', '50051')


class DeploymentPlanService(deployment_plan_pb2_grpc.DeploymentPlanServicer):
    def GetDeploymentPlans(self, request, context):
        deployment_plans = DeploymentPlan.objects.only(
            'plan',
            'instance_tier',
            'instance_type'
        )

        for deployment_plan in deployment_plans:
            yield deployment_plan_pb2.DeploymentPlanResponse(
                plan=deployment_plan.plan,
                instance_tier=deployment_plan.instance_tier,
                instance_type=deployment_plan.instance_type
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    deployment_plan_pb2_grpc.add_DeploymentPlanServicer_to_server(
        DeploymentPlanService(), server)
    server.add_insecure_port(f'[::]:{GRPC_PORT}')
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
