import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from temporal_.activities import say_hello
from temporal_.workflow import SayHello


async def main():
    client = await Client.connect("localhost:7233", namespace="default")
    worker = Worker(
        client, task_queue="hello_task_queue", workflows=[SayHello], activities=[say_hello],

    )
    await worker.run()

if __name__ == f"__main__":
    asyncio.run(main())
