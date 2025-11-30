# Structured Insight Extractor from Emails
## Objective
Extract structured data and intent from raw email content for use in CRM automation or
routing systems.

## Model used
- Input generation : gemini-3-pro-preview
- Extracting attributes : openai/gpt-oss-120b  through groq

### Why? 
To mimic emails in a realworld scenario, gemini-3-pro was used to create rich and realistic emails that depict real world emails recieved to a support team.

For extracting the attributes from the email, we don't need a very strong model, instead a simple model with fast inferencing and replicable results is crucial.
Groq provides a free, fast inference api to OpenAI's open source model (gpt-oss-120b ). The API also supports structured outputs which is required fir the task at hand.

## Usage

If you dont have uv installed: pip install uv

install requirements for the project

uv sync

Get an API key from: groq https://console.groq.com/home
set the api key as env variable: GROQ_API_KEY

Then you can run through the assignment3 notebook

To tesk for one simple example. Use the test.py file, change the subject and email body in the script and run 

uv run test.py


## App

I have also built a streamlit app with a simple incidents dashboard that does the following: 
1. Checks for emails at : helpdeskpega@gmail.com for every 10 seconds
2. If there is an email: 
 - fetches the email
 - Extracts relevant fields like user, email address, subject and body
 - Uses the attribute_parsing module to extract, relevant attributes
 - Creates a new incident record into the DB (sqlite)

The app is hosted at: https://assignmentpega.streamlit.app/dashboard
It has two tabs :
1. Check the emails attributes manually
![alt text](image.png)
2. Dedicated dashboard
![alt text](image-1.png)

The app uses IMAP to listent to a gmail account which refreshes after every 10 sec

## Key Challenges
1. 
- The major challenge was finding a dataset. While there are few email dataset that exist online, they are not a perfect fit for the problem. 
- Hence I had to synthesize a dataset that coveres real world scenarios for a CRM support system. 
- This was done to ensure that the solution being built can be tested properly from a real world scenario