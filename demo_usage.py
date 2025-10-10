#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script cho thấy cách sử dụng SatisfactionSurveyProcessor trong code Python
"""

from satisfaction_survey_processor import SatisfactionSurveyProcessor

def demo_basic_usage():
    """
    Demo sử dụng cơ bản
    """
    print("=== DEMO SỬ DỤNG CƠ BẢN ===")
    
    # Tạo processor với 20 câu hỏi
    processor = SatisfactionSurveyProcessor(20)
    
    # Tạo dữ liệu cho 30 học sinh
    output_file = processor.process_survey_data(30, 20)
    
    print(f"✅ Đã tạo file: {output_file}")

def demo_multiple_surveys():
    """
    Demo tạo nhiều khảo sát khác nhau
    """
    print("\n=== DEMO TẠO NHIỀU KHẢO SÁT ===")
    
    # Danh sách các khảo sát cần tạo
    surveys = [
        (25, 10),   # 25 học sinh, 10 câu hỏi
        (50, 20),   # 50 học sinh, 20 câu hỏi
        (75, 30),   # 75 học sinh, 30 câu hỏi
    ]
    
    for num_students, num_questions in surveys:
        print(f"\nTạo khảo sát: {num_students} học sinh, {num_questions} câu hỏi")
        
        # Tạo processor
        processor = SatisfactionSurveyProcessor(num_questions)
        
        # Tạo dữ liệu
        output_file = processor.process_survey_data(num_students, num_questions)
        
        print(f"✅ Hoàn thành: {output_file}")

def demo_custom_analysis():
    """
    Demo phân tích dữ liệu tùy chỉnh
    """
    print("\n=== DEMO PHÂN TÍCH DỮ LIỆU TÙY CHỈNH ===")
    
    # Tạo processor
    processor = SatisfactionSurveyProcessor(15)
    
    # Tạo dữ liệu
    survey_data = processor.generate_controlled_random_data(40)
    
    # Tính toán kết quả
    results = processor.calculate_satisfaction_percentages(survey_data)
    
    # Phân tích tùy chỉnh
    print("Phân tích chi tiết:")
    print(f"- Tổng số câu hỏi: {len(results)}")
    print(f"- Tổng số học sinh: {len(survey_data)}")
    
    # Tìm câu hỏi có mức độ hài lòng cao nhất và thấp nhất
    high_satisfaction = results['Mức độ hoàn toàn hài lòng (%)']
    max_idx = high_satisfaction.idxmax()
    min_idx = high_satisfaction.idxmin()
    
    print(f"- Câu hỏi có mức độ hài lòng cao nhất: Câu {max_idx + 1} ({high_satisfaction[max_idx]:.2f}%)")
    print(f"- Câu hỏi có mức độ hài lòng thấp nhất: Câu {min_idx + 1} ({high_satisfaction[min_idx]:.2f}%)")
    
    # Đếm số câu hỏi theo mức độ
    excellent = (high_satisfaction >= 95).sum()
    good = ((high_satisfaction >= 85) & (high_satisfaction < 95)).sum()
    average = ((high_satisfaction >= 75) & (high_satisfaction < 85)).sum()
    
    print(f"- Số câu hỏi xuất sắc (≥95%): {excellent}")
    print(f"- Số câu hỏi tốt (85-95%): {good}")
    print(f"- Số câu hỏi trung bình (75-85%): {average}")

def main():
    """
    Hàm chính chạy tất cả demo
    """
    try:
        demo_basic_usage()
        demo_multiple_surveys()
        demo_custom_analysis()
        
        print("\n🎉 Tất cả demo đã hoàn thành!")
        print("\nCác file Excel đã được tạo trong thư mục hiện tại.")
        
    except Exception as e:
        print(f"❌ Lỗi trong quá trình demo: {str(e)}")

if __name__ == "__main__":
    main()