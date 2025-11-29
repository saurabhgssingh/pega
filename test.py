from groq_utils import get_email_attributes, email_structure

subject = "Stop my subscription"
body = """Hi,
Please cancel my subscription to FitLife Pro effective immediately. I am not using the app enough to justify the monthly cost. I want to make sure I am not charged for next month (December).
Greg Norman"""

email_content = email_structure.format(subject=subject,
                                       body=body)

async def main():
    response = await get_email_attributes(email_content)
    print(response)

if __name__=="__main__":
    import asyncio
    asyncio.run(main())