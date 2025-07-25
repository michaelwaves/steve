import uuid
import pytest
from temporalio.worker import Worker
from temporalio.testing import WorkflowEnvironment


from backend.temporal_.activities import say_hello
from backend.temporal_.workflow import SayHello


@pytest.mark.asyncio
async def test_execute_workflow():
    task_queue_name = str(uuid.uuid4())
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue=task_queue_name,
            workflows=[SayHello],
            activities=[say_hello],
        ):
            assert "Hello, World!" == await env.client.execute_workflow(SayHello.run,
                                                                        "World",
                                                                        id=str(
                                                                            uuid.uuid4()),
                                                                        task_queue=task_queue_name)
