#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script chạy nhanh để tạo dữ liệu khảo sát hài lòng
Sử dụng: python3 run_survey.py [số_học_sinh] [số_câu_hỏi]
"""

import sys
from satisfaction_survey_processor import SatisfactionSurveyProcessor

def main():
    """
    Hàm chính để chạy script với tham số dòng lệnh
    """
    print("Script xử lý dữ liệu khảo sát hài lòng")
    print("=" * 50)
    
    # Kiểm tra tham số dòng lệnh
    if len(sys.argv) == 3:
        try:
            num_students = int(sys.argv[1])
            num_questions = int(sys.argv[2])
            
            if num_students <= 0 or num_questions <= 0:
                print("❌ Số lượng học sinh và câu hỏi phải lớn hơn 0!")
                return 1
                
        except ValueError:
            print("❌ Vui lòng nhập số nguyên hợp lệ!")
            print("Sử dụng: python3 run_survey.py [số_học_sinh] [số_câu_hỏi]")
            return 1
            
    elif len(sys.argv) == 1:
        # Chạy với input từ người dùng
        from satisfaction_survey_processor import get_user_input
        num_students, num_questions = get_user_input()
        
    else:
        print("❌ Số lượng tham số không đúng!")
        print("Sử dụng: python3 run_survey.py [số_học_sinh] [số_câu_hỏi]")
        print("Hoặc: python3 run_survey.py (để nhập thủ công)")
        return 1
    
    try:
        # Tạo processor với số câu hỏi được chỉ định
        processor = SatisfactionSurveyProcessor(num_questions)
        
        # Xử lý dữ liệu
        output_file = processor.process_survey_data(num_students, num_questions)
        
        print(f"\n✅ Hoàn thành! File kết quả: {output_file}")
        print("\nHướng dẫn sử dụng:")
        print("1. Mở file Excel kết quả")
        print("2. Sheet 'Dữ liệu khảo sát': Dữ liệu gốc với câu trả lời ngẫu nhiên")
        print("3. Sheet 'Kết quả phân tích': Phần trăm mức độ hài lòng cho từng câu hỏi")
        
    except KeyboardInterrupt:
        print("\n\n❌ Script đã bị hủy bởi người dùng.")
        return 1
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())