# Script Xử Lý Dữ Liệu Khảo Sát Hài Lòng

Script Python để tạo và xử lý dữ liệu khảo sát hài lòng với 53 câu hỏi, tạo dữ liệu ngẫu nhiên có kiểm soát và tính toán phần trăm mức độ hài lòng.

## Tính năng

- Tạo dữ liệu ngẫu nhiên có kiểm soát cho 53 câu hỏi khảo sát
- Đảm bảo tính tự nhiên của dữ liệu (tránh kết quả giống nhau liên tiếp)
- Tính toán phần trăm mức độ hài lòng cho từng câu hỏi
- Phân bố kết quả theo yêu cầu:
  - 15-20% câu hỏi có mức độ hài lòng 80-90%
  - Phần còn lại 90-100%
  - 1-2 câu hỏi có mức độ 75-80%
  - Không có câu hỏi nào đạt 100%

## Cài đặt

```bash
pip install -r requirements.txt
```

## Sử dụng

```bash
python satisfaction_survey_processor.py
```

## Kết quả

Script sẽ tạo file `ket_qua_khao_sat_hai_long.xlsx` với 2 sheet:

1. **Dữ liệu khảo sát**: Dữ liệu gốc với câu trả lời ngẫu nhiên cho 64 học sinh
2. **Kết quả phân tích**: Phần trăm mức độ hài lòng cho từng câu hỏi

## Cấu trúc dữ liệu

- **Cột STT**: Số thứ tự học sinh
- **Cột Họ và tên**: Tên học sinh
- **53 cột câu hỏi**: Câu trả lời từ 1-5 cho mỗi câu hỏi

## Công thức tính toán

- % Mức độ hài lòng (mức X của câu hỏi Y) = (Số lượng chọn mức X) / Tổng số học sinh × 100
- Mức độ hoàn toàn hài lòng = % Mức 3 + % Mức 4 + % Mức 5