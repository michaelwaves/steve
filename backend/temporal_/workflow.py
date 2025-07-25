from datetime import timedelta
from temporalio import workflow


with workflow.unsafe.imports_passed_through():
    from temporal_.activities import say_hello, send_email, search_sanctions


@workflow.defn
class SayHello:
    @workflow.run
    async def run(self, name: str) -> str:
        return await workflow.execute_activity(
            say_hello, name, start_to_close_timeout=timedelta(seconds=5)
        )

@workflow.defn
class EmailWorkflow:
    @workflow.run
    async def run(self, message_html: str, message_text: str, recipient: str = "", sender: str = "", subject: str = "") -> str:
        return await workflow.execute_activity(
            send_email, message_html, message_text, recipient, sender, subject, 
            start_to_close_timeout=timedelta(seconds=30)
        )

@workflow.defn
class SanctionsWorkflow:
    @workflow.run
    async def run(self, first_name: str, last_name: str) -> list:
        return await workflow.execute_activity(
            search_sanctions, first_name, last_name, 
            start_to_close_timeout=timedelta(seconds=30)
        )

@workflow.defn 
class KYCWorkflow:
    @workflow.run
    async def run(self, first_name: str, last_name: str, recipient_email: str) -> str:
        # Step 1: Search sanctions
        sanctions_results = await workflow.execute_activity(
            search_sanctions, first_name, last_name,
            start_to_close_timeout=timedelta(seconds=30)
        )
        
        # Step 2: Generate report (simplified for demo)
        report_html = f"""
        <h1>KYC Report for {first_name} {last_name}</h1>
        <h2>Sanctions Check Results:</h2>
        <p>Found {len(sanctions_results)} potential matches</p>
        <ul>
        """
        for result in sanctions_results:
            report_html += f"<li>{result}</li>"
        report_html += "</ul>"
        
        report_text = f"KYC Report for {first_name} {last_name}\n\nSanctions Check: Found {len(sanctions_results)} potential matches"
        
        # Step 3: Send email with report
        message_id = await workflow.execute_activity(
            send_email, report_html, report_text, recipient_email, "", f"KYC Report - {first_name} {last_name}",
            start_to_close_timeout=timedelta(seconds=30)
        )
        
        return f"KYC workflow completed. Report sent with message ID: {message_id}"
