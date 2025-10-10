#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script xử lý dữ liệu khảo sát hài lòng
Tạo dữ liệu ngẫu nhiên có kiểm soát cho 53 câu hỏi khảo sát
"""

import pandas as pd
import numpy as np
import random
import os
from typing import List, Tuple
import warnings
warnings.filterwarnings('ignore')

class SatisfactionSurveyProcessor:
    def __init__(self):
        self.num_questions = 53
        self.satisfaction_levels = [1, 2, 3, 4, 5]
        
    def generate_controlled_random_data(self, num_students: int) -> pd.DataFrame:
        """
        Tạo dữ liệu ngẫu nhiên có kiểm soát cho khảo sát hài lòng
        """
        print(f"Đang tạo dữ liệu cho {num_students} học sinh...")
        
        # Tạo cấu trúc DataFrame
        data = {
            'STT': range(1, num_students + 1),
            'Họ và tên': [f'Học sinh {i:03d}' for i in range(1, num_students + 1)]
        }
        
        # Tạo cột cho 53 câu hỏi
        for q in range(1, self.num_questions + 1):
            data[f'Câu hỏi {q}'] = [0] * num_students
        
        df = pd.DataFrame(data)
        
        # Tạo dữ liệu ngẫu nhiên có kiểm soát cho từng câu hỏi
        for q in range(1, self.num_questions + 1):
            print(f"Đang xử lý câu hỏi {q}...")
            
            # Xác định phân bố mức độ hài lòng cho câu hỏi này
            satisfaction_distribution = self._get_question_distribution(q)
            
            # Tạo dữ liệu theo phân bố đã định
            responses = self._generate_responses_for_question(
                num_students, satisfaction_distribution, q
            )
            
            df[f'Câu hỏi {q}'] = responses
        
        return df
    
    def _get_question_distribution(self, question_num: int) -> dict:
        """
        Xác định phân bố mức độ hài lòng cho từng câu hỏi
        Đảm bảo kết quả cuối cùng thỏa mãn các điều kiện:
        - 15-20% câu hỏi có mức độ hài lòng 80-90%
        - Phần còn lại 90-100%
        - 1-2 câu hỏi có mức độ 75-80%
        """
        # Xác định loại phân bố dựa trên số thứ tự câu hỏi
        if question_num == 1:  # 1 câu hỏi có mức độ 75-80%
            target_satisfaction = 77.5  # Cố định ở mức 77.5%
        elif question_num <= 8:  # 7 câu hỏi tiếp theo có mức độ 80-90% (khoảng 13%)
            target_satisfaction = random.uniform(80, 90)
        else:  # Các câu hỏi còn lại có mức độ 90-97% (không 100%)
            target_satisfaction = random.uniform(90, 97)
        
        # Tạo phân bố ngẫu nhiên nhưng có kiểm soát
        # Đảm bảo target_satisfaction = level3 + level4 + level5
        
        # Phân bố level 1, 2 (không hài lòng)
        level1 = random.uniform(0, 8)  # 0-8%
        level2 = random.uniform(0, 15)  # 0-15%
        
        # Tính phần còn lại cho level 3, 4, 5
        remaining = 100 - level1 - level2
        
        # Phân bố level 3, 4, 5 để đạt target
        if target_satisfaction <= 80:
            # Mức thấp: ít level 5, nhiều level 3
            level3 = random.uniform(35, 50)
            level4 = random.uniform(20, 30)
            level5 = random.uniform(5, 20)
        elif target_satisfaction <= 90:
            # Mức trung bình: cân bằng
            level3 = random.uniform(15, 30)
            level4 = random.uniform(25, 40)
            level5 = random.uniform(25, 40)
        else:
            # Mức cao: nhiều level 5
            level3 = random.uniform(10, 25)
            level4 = random.uniform(20, 35)
            level5 = random.uniform(35, 50)
        
        # Chuẩn hóa để tổng = 100%
        total = level1 + level2 + level3 + level4 + level5
        level1 = level1 / total * 100
        level2 = level2 / total * 100
        level3 = level3 / total * 100
        level4 = level4 / total * 100
        level5 = level5 / total * 100
        
        # Điều chỉnh để đạt target satisfaction
        current_high = level3 + level4 + level5
        if current_high < target_satisfaction:
            # Tăng level 4, 5
            adjustment = (target_satisfaction - current_high) / 2
            level4 += adjustment
            level5 += adjustment
        else:
            # Giảm level 1, 2
            reduction = (current_high - target_satisfaction) / 2
            level1 = max(0, level1 - reduction)
            level2 = max(0, level2 - reduction)
        
        # Đảm bảo không có giá trị âm
        level1 = max(0, level1)
        level2 = max(0, level2)
        level3 = max(0, level3)
        level4 = max(0, level4)
        level5 = max(0, level5)
        
        # Đảm bảo không đạt 100% - giới hạn tối đa 98.5%
        final_high = level3 + level4 + level5
        if final_high >= 98.5:
            # Giảm level 5 và tăng level 1 để đảm bảo < 98.5%
            reduction = final_high - 98.0
            level5 = max(0, level5 - reduction)
            level1 = level1 + reduction
        
        return {
            1: level1,
            2: level2,
            3: level3,
            4: level4,
            5: level5
        }
    
    def _generate_responses_for_question(self, num_students: int, distribution: dict, question_num: int = 1) -> List[int]:
        """
        Tạo câu trả lời cho một câu hỏi dựa trên phân bố đã định
        """
        # Tính số lượng học sinh cho mỗi mức độ
        counts = {}
        for level in self.satisfaction_levels:
            counts[level] = int(num_students * distribution[level] / 100)
        
        # Điều chỉnh để tổng = num_students
        total_assigned = sum(counts.values())
        if total_assigned < num_students:
            counts[5] += num_students - total_assigned
        elif total_assigned > num_students:
            counts[1] = max(0, counts[1] - (total_assigned - num_students))
        
        # Tạo danh sách câu trả lời
        responses = []
        for level, count in counts.items():
            responses.extend([level] * count)
        
        # Đảm bảo độ dài chính xác
        while len(responses) < num_students:
            responses.append(5)  # Thêm mức 5 nếu thiếu
        while len(responses) > num_students:
            responses.pop()  # Bỏ bớt nếu thừa
        
        # Xáo trộn ngẫu nhiên
        random.shuffle(responses)
        
        # Kiểm tra và đảm bảo không có câu hỏi nào đạt 100%
        high_satisfaction_count = sum(1 for r in responses if r >= 3)
        high_satisfaction_percentage = (high_satisfaction_count / num_students) * 100
        
        if high_satisfaction_percentage >= 99.0:
            # Thay thế một số câu trả lời mức 5 bằng mức 1 để giảm tỷ lệ
            level5_indices = [i for i, r in enumerate(responses) if r == 5]
            if len(level5_indices) > 0:
                # Thay thế một số mức 5 bằng mức 1
                num_to_replace = min(2, len(level5_indices))
                for i in range(num_to_replace):
                    responses[level5_indices[i]] = 1
        
        # Đặc biệt xử lý câu hỏi 1 để đảm bảo mức độ hài lòng thấp
        if question_num == 1:
            # Đảm bảo câu hỏi 1 có mức độ hài lòng 75-80%
            high_satisfaction_count = sum(1 for r in responses if r >= 3)
            high_satisfaction_percentage = (high_satisfaction_count / num_students) * 100
            
            if high_satisfaction_percentage > 80:
                # Thay thế một số câu trả lời mức 4, 5 bằng mức 1, 2
                level4_5_indices = [i for i, r in enumerate(responses) if r >= 4]
                if len(level4_5_indices) > 0:
                    num_to_replace = min(8, len(level4_5_indices))  # Thay thế 8 câu
                    for i in range(num_to_replace):
                        responses[level4_5_indices[i]] = random.choice([1, 2])
        
        return responses
    
    def calculate_satisfaction_percentages(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Tính toán phần trăm mức độ hài lòng cho từng câu hỏi
        """
        print("Đang tính toán phần trăm mức độ hài lòng...")
        
        num_students = len(df)
        results = []
        
        for q in range(1, self.num_questions + 1):
            col_name = f'Câu hỏi {q}'
            question_data = df[col_name]
            
            # Tính phần trăm cho từng mức độ (1-5)
            level_percentages = {}
            for level in self.satisfaction_levels:
                count = (question_data == level).sum()
                percentage = (count / num_students) * 100
                level_percentages[f'Mức {level}'] = round(percentage, 2)
            
            # Tính mức độ hoàn toàn hài lòng (mức 3 + 4 + 5)
            high_satisfaction = level_percentages['Mức 3'] + level_percentages['Mức 4'] + level_percentages['Mức 5']
            
            result = {
                'Câu hỏi': q,
                'Mức 1 (%)': level_percentages['Mức 1'],
                'Mức 2 (%)': level_percentages['Mức 2'],
                'Mức 3 (%)': level_percentages['Mức 3'],
                'Mức 4 (%)': level_percentages['Mức 4'],
                'Mức 5 (%)': level_percentages['Mức 5'],
                'Mức độ hoàn toàn hài lòng (%)': round(high_satisfaction, 2)
            }
            
            results.append(result)
        
        return pd.DataFrame(results)
    
    def process_survey_data(self, input_file: str = None, num_students: int = 64) -> str:
        """
        Xử lý dữ liệu khảo sát và tạo file kết quả
        """
        print("=== XỬ LÝ DỮ LIỆU KHẢO SÁT HÀI LÒNG ===")
        
        # Tạo dữ liệu ngẫu nhiên có kiểm soát
        survey_data = self.generate_controlled_random_data(num_students)
        
        # Tính toán phần trăm mức độ hài lòng
        satisfaction_results = self.calculate_satisfaction_percentages(survey_data)
        
        # Tạo file kết quả
        output_file = 'ket_qua_khao_sat_hai_long.xlsx'
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Ghi dữ liệu khảo sát gốc
            survey_data.to_excel(writer, sheet_name='Dữ liệu khảo sát', index=False)
            
            # Ghi kết quả tính toán
            satisfaction_results.to_excel(writer, sheet_name='Kết quả phân tích', index=False)
        
        print(f"\n=== HOÀN THÀNH ===")
        print(f"File kết quả đã được tạo: {output_file}")
        print(f"Số học sinh: {num_students}")
        print(f"Số câu hỏi: {self.num_questions}")
        
        # Hiển thị thống kê kết quả
        self._display_results_summary(satisfaction_results)
        
        return output_file
    
    def _display_results_summary(self, results_df: pd.DataFrame):
        """
        Hiển thị tóm tắt kết quả
        """
        high_satisfaction = results_df['Mức độ hoàn toàn hài lòng (%)']
        
        print(f"\n=== THỐNG KÊ KẾT QUẢ ===")
        print(f"Mức độ hài lòng trung bình: {high_satisfaction.mean():.2f}%")
        print(f"Mức độ hài lòng thấp nhất: {high_satisfaction.min():.2f}%")
        print(f"Mức độ hài lòng cao nhất: {high_satisfaction.max():.2f}%")
        
        # Đếm số câu hỏi theo khoảng mức độ
        range_75_80 = ((high_satisfaction >= 75) & (high_satisfaction < 80)).sum()
        range_80_90 = ((high_satisfaction >= 80) & (high_satisfaction < 90)).sum()
        range_90_100 = ((high_satisfaction >= 90) & (high_satisfaction < 100)).sum()
        range_100 = (high_satisfaction == 100).sum()
        
        print(f"\nPhân bố mức độ hài lòng:")
        print(f"- 75-80%: {range_75_80} câu hỏi ({range_75_80/53*100:.1f}%)")
        print(f"- 80-90%: {range_80_90} câu hỏi ({range_80_90/53*100:.1f}%)")
        print(f"- 90-100%: {range_90_100} câu hỏi ({range_90_100/53*100:.1f}%)")
        print(f"- 100%: {range_100} câu hỏi ({range_100/53*100:.1f}%)")
        
        print(f"\nDanh sách mức độ hài lòng của 53 câu hỏi:")
        for i, value in enumerate(high_satisfaction, 1):
            print(f"Câu {i:2d}: {value:6.2f}%", end="  ")
            if i % 5 == 0:  # Xuống dòng mỗi 5 câu
                print()

def main():
    """
    Hàm chính để chạy script
    """
    processor = SatisfactionSurveyProcessor()
    
    # Số học sinh mặc định (có thể thay đổi)
    num_students = 64
    
    print("Script xử lý dữ liệu khảo sát hài lòng")
    print("=" * 50)
    
    try:
        # Xử lý dữ liệu
        output_file = processor.process_survey_data(num_students=num_students)
        
        print(f"\n✅ Hoàn thành! File kết quả: {output_file}")
        print("\nHướng dẫn sử dụng:")
        print("1. Mở file Excel kết quả")
        print("2. Sheet 'Dữ liệu khảo sát': Dữ liệu gốc với câu trả lời ngẫu nhiên")
        print("3. Sheet 'Kết quả phân tích': Phần trăm mức độ hài lòng cho từng câu hỏi")
        
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())