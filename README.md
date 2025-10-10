# Script Xử Lý Dữ Liệu Khảo Sát Hài Lòng

Script Python để tạo và xử lý dữ liệu khảo sát hài lòng với số lượng câu hỏi và học sinh tùy biến, tạo dữ liệu ngẫu nhiên có kiểm soát và tính toán phần trăm mức độ hài lòng.

## Tính năng

- **Tùy biến số lượng câu hỏi và học sinh** theo nhu cầu sử dụng
- Tạo dữ liệu ngẫu nhiên có kiểm soát cho bất kỳ số lượng câu hỏi nào
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

### Cách 1: Chạy với tham số dòng lệnh (Khuyến nghị)

```bash
# Tạo khảo sát với 100 học sinh và 30 câu hỏi
python3 run_survey.py 100 30

# Tạo khảo sát với 50 học sinh và 20 câu hỏi
python3 run_survey.py 50 20
```

### Cách 2: Chạy với input thủ công

```bash
python3 run_survey.py
# Hoặc
python3 satisfaction_survey_processor.py
```

### Cách 3: Sử dụng trong code Python

```python
from satisfaction_survey_processor import SatisfactionSurveyProcessor

# Tạo processor với 25 câu hỏi
processor = SatisfactionSurveyProcessor(25)

# Xử lý dữ liệu cho 80 học sinh
output_file = processor.process_survey_data(80, 25)
```

## Kết quả

Script sẽ tạo file `ket_qua_khao_sat_hai_long_[số_hs]hs_[số_câu]cau.xlsx` với 2 sheet:

1. **Dữ liệu khảo sát**: Dữ liệu gốc với câu trả lời ngẫu nhiên
2. **Kết quả phân tích**: Phần trăm mức độ hài lòng cho từng câu hỏi

## Cấu trúc dữ liệu

- **Cột STT**: Số thứ tự học sinh
- **Cột Họ và tên**: Tên học sinh (Học sinh 001, Học sinh 002, ...)
- **N cột câu hỏi**: Câu trả lời từ 1-5 cho mỗi câu hỏi (N = số câu hỏi)

## Công thức tính toán

- % Mức độ hài lòng (mức X của câu hỏi Y) = (Số lượng chọn mức X) / Tổng số học sinh × 100
- Mức độ hoàn toàn hài lòng = % Mức 3 + % Mức 4 + % Mức 5

## Ví dụ sử dụng

```bash
# Tạo khảo sát mẫu với 64 học sinh và 53 câu hỏi
python3 run_survey.py 64 53

# Tạo khảo sát nhỏ với 20 học sinh và 10 câu hỏi
python3 run_survey.py 20 10

# Tạo khảo sát lớn với 200 học sinh và 100 câu hỏi
python3 run_survey.py 200 100
```