import asyncio
from temporal_.workflow import SayHello, EmailWorkflow, SanctionsWorkflow, KYCWorkflow
from temporalio.client import Client


async def main():
    client = await Client.connect("localhost:7233")

    # Example: Run KYC workflow
    result = await client.execute_workflow(
        KYCWorkflow.run, 
        "Michael", 
        "Yu", 
        "ryanymark@gmail.com",
        id="kyc_workflow", 
        task_queue="kyc_task_queue"
    )
    print(f'KYC Workflow Result: {result}')

    # Example: Run sanctions check only
    sanctions_result = await client.execute_workflow(
        SanctionsWorkflow.run, 
        "John", 
        "Doe", 
        id="sanctions_workflow", 
        task_queue="kyc_task_queue"
    )
    print(f'Sanctions Result: {sanctions_result}')

    # Example: Send email only
    email_result = await client.execute_workflow(
        EmailWorkflow.run,
        "<h1>Test Email</h1><p>This is a test email.</p>",
        "Test Email\n\nThis is a test email.",
        "test@example.com",
        "",
        "Test Subject",
        id="email_workflow",
        task_queue="kyc_task_queue"
    )
    print(f'Email Result: {email_result}')

if __name__ == "__main__":
    asyncio.run(main())
