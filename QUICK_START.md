# Hướng Dẫn Sử Dụng Nhanh

## 🚀 Cài đặt nhanh

```bash
pip3 install -r requirements.txt
```

## 📝 Sử dụng cơ bản

### 1. Chạy với tham số dòng lệnh (Khuyến nghị)

```bash
# Tạo khảo sát với 100 học sinh và 30 câu hỏi
python3 run_survey.py 100 30

# Tạo khảo sát với 50 học sinh và 20 câu hỏi  
python3 run_survey.py 50 20
```

### 2. Chạy với input thủ công

```bash
python3 run_survey.py
# Nhập số học sinh và số câu hỏi khi được yêu cầu
```

### 3. Sử dụng trong code Python

```python
from satisfaction_survey_processor import SatisfactionSurveyProcessor

# Tạo processor với 25 câu hỏi
processor = SatisfactionSurveyProcessor(25)

# Xử lý dữ liệu cho 80 học sinh
output_file = processor.process_survey_data(80, 25)
```

## 📊 Kết quả

Script sẽ tạo file Excel với tên: `ket_qua_khao_sat_hai_long_[số_hs]hs_[số_câu]cau.xlsx`

**Ví dụ:** `ket_qua_khao_sat_hai_long_100hs_30cau.xlsx`

## 📋 Cấu trúc file Excel

### Sheet 1: "Dữ liệu khảo sát"
- Cột STT: Số thứ tự học sinh
- Cột Họ và tên: Tên học sinh (Học sinh 001, Học sinh 002, ...)
- N cột câu hỏi: Câu trả lời từ 1-5 cho mỗi câu hỏi

### Sheet 2: "Kết quả phân tích"
- Câu hỏi: Số thứ tự câu hỏi
- Mức 1-5 (%): Phần trăm học sinh chọn mỗi mức độ
- Mức độ hoàn toàn hài lòng (%): Tổng % mức 3 + 4 + 5

## ✅ Đặc điểm

- **Tùy biến hoàn toàn**: Số học sinh và câu hỏi tùy ý
- **Dữ liệu tự nhiên**: Tránh kết quả giống nhau liên tiếp
- **Phân bố hợp lý**: 
  - 1-2 câu hỏi ở mức 75-80%
  - 15-20% câu hỏi ở mức 80-90%
  - Phần còn lại ở mức 90-100%
  - Không có câu hỏi nào đạt 100%

## 🔧 Demo

Chạy script demo để xem các ví dụ sử dụng:

```bash
python3 demo_usage.py
```

## 📁 Files quan trọng

- `satisfaction_survey_processor.py` - Script chính
- `run_survey.py` - Script chạy nhanh với tham số
- `demo_usage.py` - Script demo các cách sử dụng
- `requirements.txt` - Dependencies cần thiết
- `README.md` - Hướng dẫn chi tiết