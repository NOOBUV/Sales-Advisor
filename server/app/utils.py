import os
from groq import Groq
import duckdb
import pandas as pd

def chat_with_groq(client, prompt, model, response_format):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format=response_format
    )
    return completion.choices[0].message.content

def execute_duckdb_query(query):
    original_cwd = os.getcwd()
    print(original_cwd)
    os.chdir('./app/templates/data')

    try:
        conn = duckdb.connect(database=':memory:', read_only=False)
        query_result = conn.execute(query).fetchdf().reset_index(drop=True)
    finally:
        os.chdir(original_cwd)

    return query_result

def get_summarization(client, user_question, df, model):
    prompt = '''
    A user asked the following question pertaining to local database tables:
    
    {user_question}
    
    To answer the question, a dataframe was returned:
    
    Dataframe:
    {df}

    Based on the data in the table, provide actionable insights and recommendations. For example:
    - Identify the age range and gender that predominantly purchase the product and suggest targeting that audience.
    - Recommend an optimal price point based on the data.
    - Identify customers whose purchase frequency has dropped and recommend reaching out for feedback, including their phone numbers for direct contact.
    '''.format(user_question=user_question, df=df)

    return chat_with_groq(client, prompt, model, None)
