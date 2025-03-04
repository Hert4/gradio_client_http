### Router methods
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("sentence-transformers/stsb-xlm-r-multilingual")

gmes = """## **1. Bảng gmes_production_report**
Bảng này lưu trữ **dữ liệu hiệu suất sản xuất** cho các mô hình và quy trình khác nhau. Bảng theo dõi tỷ lệ năng suất, tổng số lượng sản xuất và hiệu suất hàng ngày theo thời gian.

### **Cột:**
- **Mô hình (`TEXT`)** – Tên hoặc mã định danh của mô hình sản phẩm đang được sản xuất.
- **Quy trình (`TEXT`)** – Quy trình hoặc giai đoạn sản xuất cụ thể (ví dụ: lắp ráp, thử nghiệm).
- **Tổng_năng suất (`FLOAT`)** – Tỷ lệ năng suất chung cho mô hình trong quy trình đó, được tính là `(Tổng_đồng ý / Tổng) * 100`.
- **Total_OK (`INTEGER`)** – Tổng số đơn vị đã vượt qua kiểm soát chất lượng.
- **Total_NG (`INTEGER`)** – Tổng số đơn vị bị lỗi (không tốt) không vượt qua kiểm soát chất lượng.
- **Total (`INTEGER`)** – Tổng số đơn vị đã xử lý (tổng của `Total_OK` và `Total_NG`).
- **Yield_2024_02_12 (`FLOAT`)** – Tỷ lệ phần trăm sản lượng được ghi nhận vào **ngày 12 tháng 2 năm 2024**.
- **Yield_2024_02_13 (`FLOAT`)** – Tỷ lệ phần trăm sản lượng được ghi nhận vào **ngày 13 tháng 2 năm 2024**.
- **Yield_2024_02_14 (`FLOAT`)** – Tỷ lệ phần trăm sản lượng được ghi nhận vào **ngày 14 tháng 2 năm 2024**.

### **Cách sử dụng:**
- Giúp theo dõi **hiệu quả sản xuất** theo thời gian.
- Cho phép **phân tích xu hướng năng suất** hàng ngày.
- Hỗ trợ **đánh giá kiểm soát chất lượng** bằng cách so sánh tỷ lệ lỗi giữa các mô hình và quy trình khác nhau.
"""


worst = """## **2. table_worst Bảng**
Bảng này theo dõi **thông tin liên quan đến lỗi**, làm nổi bật các lỗi phổ biến nhất xảy ra trong quá trình sản xuất.

### **Cột:**
- **Mô hình (`TEXT`)** – Mô hình sản phẩm liên quan đến lỗi đã ghi lại.
- **Quy trình (`TEXT`)** – Quy trình sản xuất cụ thể nơi xảy ra lỗi.
- **Error_Name (`TEXT`)** – Tên hoặc danh mục lỗi (ví dụ: "Lỗi A", "Sai lệch").
- **Error_Count (`INTEGER`)** – Số lần lỗi này được ghi lại đối với mô hình và quy trình đã cho.
- **Error_Percentage (`FLOAT`)** – Tỷ lệ phần trăm các đơn vị bị lỗi do lỗi cụ thể này, được tính là `(Error_Count / Total) * 100`.

### **Cách sử dụng:**
- Giúp xác định **các lỗi có vấn đề** trong dây chuyền sản xuất.
- Cho phép **phân tích nguyên nhân gốc rễ** bằng cách liên kết các lỗi với các quy trình cụ thể.
- Hỗ trợ **cải tiến liên tục** trong kiểm soát chất lượng bằng cách giải quyết các lỗi thường gặp nhất.

"""


def create_metadata_embedings(metadata: list, model):
    embeddings = model.encode(metadata)
    return embeddings


def find_best_fit(embeddings, model, user_query):
    query_embedding = model.encode([user_query])
    similarities = cosine_similarity(query_embedding, embeddings)
    best_match_table = similarities.argmax()
    if best_match_table == 0:
        table_metadata = gmes
    elif best_match_table == 1:
        table_metadata = worst

    return table_metadata


user_query = "Tôi muốn biết tổng lỗi lặp của Model A"

metadata = [gmes, worst]
embeddings = create_metadata_embedings(metadata, model)
table_metadata = find_best_fit(embeddings, model, user_query)


print(table_metadata)
