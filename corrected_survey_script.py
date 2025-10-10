import pandas as pd
import numpy as np
import os
from collections import Counter

# 1. Lấy tên file Excel đầu tiên trong thư mục hiện tại
folder_path = os.getcwd()  # Lấy thư mục làm việc hiện tại
excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

if not excel_files:
    print("Không tìm thấy file Excel nào trong thư mục!")
else:
    # Lấy file Excel đầu tiên
    file_in = excel_files[0]
    print(f"Đang xử lý file: {file_in}")

    # 2. Lấy danh sách các sheet trong file Excel
    xl = pd.ExcelFile(file_in)
    sheet_names = xl.sheet_names
    if not sheet_names:
        print("Không tìm thấy sheet nào trong file!")
    else:
        # Sử dụng sheet đầu tiên
        sheet = sheet_names[0]
        print(f"Đang xử lý sheet: {sheet}")

        # 3. Load data từ file
        df = pd.read_excel(file_in, sheet_name=sheet)

        # 4. Xác định cột đáp án (giả sử từ cột thứ 3 trở đi là đáp án 1–5)
        response_cols = df.columns[2:]
        n = 64  # Tổng số học sinh (cố định 64)
        num_questions = 51  # Số câu hỏi (cố định 51)

        print(f"Số học sinh: {n}")
        print(f"Số câu hỏi: {len(response_cols)}")

        # 5. Tạo số phiếu mức độ hài lòng dựa trên phân phối tỷ lệ mong muốn
        rng = np.random.default_rng()  # Loại bỏ seed để tạo ngẫu nhiên mỗi lần chạy
        new_counts = []
        
        # Tạo danh sách để theo dõi các tỷ lệ đã sử dụng để tránh lặp lại
        used_percentages = []
        
        for i, col in enumerate(response_cols):
            # Tạo một phân phối ngẫu nhiên cho các mức độ hài lòng 1-5
            # Điều chỉnh phân phối theo yêu cầu:
            # - 1-2 câu hỏi có tỷ lệ 75-80%
            # - 15-20% câu hỏi có tỷ lệ 80-90%
            # - Phần còn lại có tỷ lệ 90-<100% (không bao giờ đạt 100%)
            
            if i < 2 and rng.random() < 0.5:  # 1-2 câu hỏi đầu có thể có tỷ lệ 75-80%
                target_satisfaction = rng.uniform(75, 80)
            elif rng.random() < 0.18:  # 15-20% câu hỏi có tỷ lệ 80-90%
                target_satisfaction = rng.uniform(80, 90)
            else:  # Phần còn lại có tỷ lệ 90-<100%
                target_satisfaction = rng.uniform(90, 99.9)
            
            # Tạo phân phối để đạt được target_satisfaction
            # Mức độ hài lòng = mức 3 + mức 4 + mức 5
            satisfaction_count = int(n * target_satisfaction / 100)
            
            # Phân phối ngẫu nhiên cho mức 3, 4, 5
            remaining = satisfaction_count
            level3 = rng.integers(0, min(remaining, n//3) + 1)
            remaining -= level3
            level4 = rng.integers(0, min(remaining, n//2) + 1)
            remaining -= level4
            level5 = remaining
            
            # Phân phối cho mức 1, 2 (không hài lòng)
            remaining = n - satisfaction_count
            level1 = rng.integers(0, min(remaining, n//3) + 1)
            remaining -= level1
            level2 = remaining
            
            counts = [level1, level2, level3, level4, level5]
            
            # Kiểm tra và điều chỉnh nếu cần
            total = sum(counts)
            if total != n:
                diff = n - total
                if diff > 0:
                    counts[4] += diff  # Thêm vào mức 5
                else:
                    counts[0] = max(0, counts[0] + diff)  # Giảm từ mức 1
            
            new_counts.append(counts)
            
            # Tính tỷ lệ hài lòng thực tế để kiểm tra
            actual_satisfaction = (counts[2] + counts[3] + counts[4]) / n * 100
            used_percentages.append(round(actual_satisfaction, 2))

        # 6. Kiểm tra và điều chỉnh để tránh tỷ lệ giống nhau liên tiếp
        for i in range(1, len(used_percentages)):
            # Kiểm tra 3 câu liên tiếp
            if i >= 2:
                if (used_percentages[i] == used_percentages[i-1] == used_percentages[i-2]):
                    # Điều chỉnh câu hiện tại
                    new_target = rng.uniform(85, 95)
                    satisfaction_count = int(n * new_target / 100)
                    remaining = satisfaction_count
                    level3 = rng.integers(0, min(remaining, n//3) + 1)
                    remaining -= level3
                    level4 = rng.integers(0, min(remaining, n//2) + 1)
                    remaining -= level4
                    level5 = remaining
                    remaining = n - satisfaction_count
                    level1 = rng.integers(0, min(remaining, n//3) + 1)
                    remaining -= level1
                    level2 = remaining
                    counts = [level1, level2, level3, level4, level5]
                    total = sum(counts)
                    if total != n:
                        diff = n - total
                        if diff > 0:
                            counts[4] += diff
                        else:
                            counts[0] = max(0, counts[0] + diff)
                    new_counts[i] = counts
                    used_percentages[i] = round((counts[2] + counts[3] + counts[4]) / n * 100, 2)
            
            # Kiểm tra 2 câu liên tiếp
            elif used_percentages[i] == used_percentages[i-1]:
                # Điều chỉnh câu hiện tại
                new_target = rng.uniform(85, 95)
                satisfaction_count = int(n * new_target / 100)
                remaining = satisfaction_count
                level3 = rng.integers(0, min(remaining, n//3) + 1)
                remaining -= level3
                level4 = rng.integers(0, min(remaining, n//2) + 1)
                remaining -= level4
                level5 = remaining
                remaining = n - satisfaction_count
                level1 = rng.integers(0, min(remaining, n//3) + 1)
                remaining -= level1
                level2 = remaining
                counts = [level1, level2, level3, level4, level5]
                total = sum(counts)
                if total != n:
                    diff = n - total
                    if diff > 0:
                        counts[4] += diff
                    else:
                        counts[0] = max(0, counts[0] + diff)
                new_counts[i] = counts
                used_percentages[i] = round((counts[2] + counts[3] + counts[4]) / n * 100, 2)

        # 7. Kiểm tra tỷ lệ bị lặp quá nhiều, điều chỉnh nếu cần
        c = Counter(used_percentages)
        for val, freq in c.items():
            if freq > 3:
                idxs = [i for i, x in enumerate(used_percentages) if x == val]
                for j in idxs[3:]:
                    new_target = rng.uniform(85, 95)
                    satisfaction_count = int(n * new_target / 100)
                    remaining = satisfaction_count
                    level3 = rng.integers(0, min(remaining, n//3) + 1)
                    remaining -= level3
                    level4 = rng.integers(0, min(remaining, n//2) + 1)
                    remaining -= level4
                    level5 = remaining
                    remaining = n - satisfaction_count
                    level1 = rng.integers(0, min(remaining, n//3) + 1)
                    remaining -= level1
                    level2 = remaining
                    counts = [level1, level2, level3, level4, level5]
                    total = sum(counts)
                    if total != n:
                        diff = n - total
                        if diff > 0:
                            counts[4] += diff
                        else:
                            counts[0] = max(0, counts[0] + diff)
                    new_counts[j] = counts
                    used_percentages[j] = round((counts[2] + counts[3] + counts[4]) / n * 100, 2)

        # In kết quả MỨC ĐỘ HOÀN TOÀN HÀI LÒNG TỔNG CỘNG
        print("MỨC ĐỘ HOÀN TOÀN HÀI LÒNG TỔNG CỘNG (%) cho từng câu hỏi:")
        for i, perc in enumerate(used_percentages):
            print(f"Câu {i+1}: {perc:.2f}%")

        # 8. Điều chỉnh raw data để áp dụng số phiếu mới
        df2 = df.copy()
        for idx, col in enumerate(response_cols):
            # Lấy phân phối số phiếu cho mức độ hài lòng 1-5 từ new_counts
            counts = new_counts[idx]
            # Tạo một list mới với số phiếu cho mỗi mức độ hài lòng
            new_values = [1]*counts[0] + [2]*counts[1] + [3]*counts[2] + [4]*counts[3] + [5]*counts[4]
            rng.shuffle(new_values)  # Shuffle để đảm bảo phân phối ngẫu nhiên
            df2[col] = new_values

        # 9. Ghi file mới
        out_file = f"adjusted_{file_in}"  # Tên file mới sẽ là 'adjusted_tên_file.xlsx'
        df2.to_excel(out_file, index=False)
        print(f"Hoàn thành! File đã được lưu: {out_file}")
        print(f"Tổng số học sinh: {n}")
        print(f"Tổng số câu hỏi: {len(response_cols)}")
        
        # Kiểm tra phân phối cuối cùng
        print("\nPhân phối tỷ lệ hài lòng:")
        print(f"- Tỷ lệ 75-80%: {sum(1 for p in used_percentages if 75 <= p < 80)} câu")
        print(f"- Tỷ lệ 80-90%: {sum(1 for p in used_percentages if 80 <= p < 90)} câu")
        print(f"- Tỷ lệ 90-<100%: {sum(1 for p in used_percentages if 90 <= p < 100)} câu")
        print(f"- Tỷ lệ 100%: {sum(1 for p in used_percentages if p >= 100)} câu")