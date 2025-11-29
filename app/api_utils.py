from groq import Groq
from pydantic import BaseModel
from typing import Literal
import json
import os 
api_key =os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

system_prompt = f"Extract request attributes from the email content. The extracted attributes are to be used in a routing system of a support ticketing system"

# define the base structure in which we expect the output
from pydantic import BaseModel,Field

class RequestAttributes(BaseModel):
    intent:str = Field(description="Nature of request. For example: refund, replacement")
    customer_name:str | None = Field(description="Name of the customer. None if name not mentioned ")
    product:str =Field(description= "Name of the product. For example bluetooth speaker, mixer grinder")
    requested_action:str | None =Field(description="What is the customer's recommended action. For example: refund, replacement. None if theres is no enough information ")


def get_email_attributes(email_content):
    try:
        response = client.chat.completions.create(model="openai/gpt-oss-120b",
                                                        temperature=0,
                                                        reasoning_effort="low",
                                                        messages=[{"role": "system", "content": system_prompt},
                                                                    {"role": "user","content": email_content,}],
                                                        response_format={"type": "json_schema",
                                                                        "json_schema": {"name": "email_request_attributes",
                                                                                        "schema": RequestAttributes.model_json_schema()
                                                                                            }
                                                                    })

        review = RequestAttributes.model_validate(json.loads(response.choices[0].message.content))
        return review.model_dump()
    except Exception as e:
        # On failure print first 100 chars and return an empty dictionary
        print("Request failed for: ",email_content[100:])
        print(e)
        return {}
    

email_structure = "Subject:{subject}\nBody:{body}"