import asyncio
from run_worker import SayHello
from temporalio.client import Client


async def main():
    client = await Client.connect("localhost:7233")

    result = await client.execute_workflow(
        SayHello.run, "Temporal", id="hello_workflow", task_queue="hello_task_queue"
    )
    print(f'Result: {result}')

if __name__ == "__main__":
    asyncio.run(main())
