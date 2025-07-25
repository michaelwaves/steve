import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from temporal_.activities import say_hello, send_email, search_sanctions
from temporal_.workflow import SayHello, EmailWorkflow, SanctionsWorkflow, KYCWorkflow


async def main():
    client = await Client.connect("localhost:7233", namespace="default")
    worker = Worker(
        client, 
        task_queue="kyc_task_queue", 
        workflows=[SayHello, EmailWorkflow, SanctionsWorkflow, KYCWorkflow], 
        activities=[say_hello, send_email, search_sanctions],
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
