import grpc

from concurrent import futures
from pb.proto import deployment_plan_pb2_grpc, deployment_plan_pb2

from app.models import DeploymentPlan


class DeploymentPlanService(deployment_plan_pb2_grpc):
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
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
