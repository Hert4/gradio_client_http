from huggingface_hub import InferenceClient
from init import ACCESS_TOKEN, SYSTEM_PROMPT
from utils import extract_sql, is_sql
from database import execute


client = InferenceClient(api_key=ACCESS_TOKEN)


def respond(message, history, system_message, max_tokens, temperature, top_p):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    # Xử lý lịch sử chat
    for val in history:
        if val[0]:
            messages.append({"role": "user", "content": val[0]})
        if val[1]:
            messages.append({"role": "assistant", "content": val[1]})

    messages.append({"role": "user", "content": message})

    # Tạo response đầu tiên
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

    # Xử lý logic SQL và retry
    if is_sql(response):
        sql_query = extract_sql(response)
        max_attempts = 3
        attempts = 0
        sql_result = None
        last_error = None

        while attempts < max_attempts:
            try:
                sql_result = execute(sql_query)
                break
            except Exception as e:
                last_error = str(e)
                attempts += 1
                if attempts < max_attempts:
                    # Thêm thông tin lỗi vào context và yêu cầu mô hình hỏi lại người dùng
                    clarification_prompt = f"""Tôi gặp lỗi khi thực hiện truy vấn SQL: {last_error}
                    Bạn có thể cung cấp thêm thông tin hoặc chỉnh sửa câu hỏi để tôi có thể sửa truy vấn không?"""
                    messages += [
                        {"role": "assistant", "content": response},
                        {"role": "user", "content": clarification_prompt},
                    ]

                    # Tạo response yêu cầu thông tin thêm
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

                    # Nếu mô hình cung cấp SQL mới, tiếp tục thử
                    if is_sql(response):
                        sql_query = extract_sql(response)
                else:
                    # Nếu sau 3 lần vẫn lỗi, tiếp tục hỏi lại người dùng thay vì in lỗi
                    retry_prompt = f"""Tôi đã thử {max_attempts} lần nhưng vẫn gặp lỗi: {last_error}
                    Bạn có thể cung cấp thêm chi tiết về dữ liệu cần truy vấn không?"""
                    messages.append({"role": "assistant", "content": retry_prompt})
                    yield retry_prompt
                    return

        # Nếu thực hiện truy vấn thành công
        if sql_result is not None:
            reformulation_prompt = f"""Kết quả truy vấn SQL:
            {sql_result}
            Hãy tóm tắt kết quả thành phản hồi tự nhiên cho người dùng."""
            messages += [
                {"role": "assistant", "content": response},
                {"role": "user", "content": reformulation_prompt},
            ]

            # Tạo response tóm tắt
            reformulated_response = ""
            for message in client.chat.completions.create(
                model="Qwen/Qwen2.5-3B-Instruct",
                max_tokens=512,
                stream=True,
                temperature=temperature,
                top_p=top_p,
                messages=messages,
            ):
                token = message.choices[0].delta.content
                reformulated_response += token
                yield reformulated_response
