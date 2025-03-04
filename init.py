from database import db_schema
import os
from router import gmes, worst

ACCESS_TOKEN = os.getenv("HF_TOKEN")

SYSTEM_PROMPT = f"""Nhiệm vụ của bạn là tạo ra DuckDB SQL hợp lệ để trả lời câu hỏi sau, với một lược đồ cơ sở dữ liệu DuckDB.

Sau đây là lược đồ cơ sở dữ liệu mà truy vấn SQL sẽ chạy trên đó:
{db_schema}

{gmes}

{worst}

Trả về truy vấn SQL như sau:
```sql
<truy vấn SQL>
```

Lưu ý: Chỉ báo cáo khi mà bạn đã truy vấn SQL trước đó không tự ý báo dữ liệu giả.
"""

####################################################################################################
# cấu trúc system prompt = 
