import asyncio

import grpc
import grpc.experimental.aio
from sqlalchemy import select

import env
import deployment_plan_pb2
import deployment_plan_pb2_grpc
from dependencies import get_db_session
from plan.models import Plan
from instance.models import Instance


class DeploymentService(deployment_plan_pb2.DeploymentPlanService):
    async def GetDeploymentPlans(self, request, context):
        session = await get_db_session()
        results = await session.execute(select(Plan.name, Instance.type).join(
            Instance, Plan.instance_id == Instance.id))

        for result in results:
            yield deployment_plan_pb2.DeploymentPlanResponse(plan=result.name, instance_type=result.type)


async def main():
    grpc.experimental.aio.init_grpc_aio()
    server = grpc.experimental.aio.server()
    deployment_plan_pb2_grpc.add_DeploymentPlanServiceServicer_to_server(
        DeploymentService(), server)
    server.add_insecure_port(f"[::]:{env.GRPC_PORT}")

    await server.start()
    await server.wait_for_termination()


asyncio.run(main())
