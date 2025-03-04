from huggingface_hub import InferenceClient
from init import ACCESS_TOKEN, SYSTEM_PROMPT
from utils import extract_sql, is_sql
from database import execute

client = InferenceClient(api_key=ACCESS_TOKEN)
messages = [{"role": "system", "content": SYSTEM_PROMPT}]


def respond(message, history, system_message, max_tokens, temperature, top_p):
    for val in history:
        if val[0]:
            messages.append({"role": "user", "content": val[0]})
        if val[1]:
            messages.append({"role": "assistant", "content": val[1]})

    messages.append({"role": "user", "content": message})

    response = ""
    for message in client.chat.completions.create(
        model="Qwen/Qwen2.5-3B-Instruct",
        max_tokens=max_tokens,
        stream=True,
        temperature=temperature,
        top_p=top_p,
        messages=messages,
    ):
        token = message.choices[0].delta.content
        response += token
        yield response
    if is_sql(response):
        sql_query = extract_sql(response)
        sql_result = execute(sql_query)

        reformulation_prompt = f"Kết quả truy vấn SQL:\n{sql_result}\n\nHãy diễn đạt lại kết quả cho người dùng một cách dễ hiểu."
        messages.append({"role": "user", "content": reformulation_prompt})

        reformulated_response = ""
        for msg in client.chat.completions.create(
            model="Qwen/Qwen2.5-3B-Instruct",
            max_tokens=512,
            stream=True,
            temperature=temperature,
            top_p=top_p,
            messages=messages,
        ):
            token = msg.choices[0].delta.content
            reformulated_response += token
            yield reformulated_response
