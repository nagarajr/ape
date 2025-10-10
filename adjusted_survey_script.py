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

        for i, col in enumerate(response_cols):
            # Tạo một phân phối ngẫu nhiên cho các mức độ hài lòng 1-5
            # Điều chỉnh phân phối để phù hợp với 64 học sinh
            if rng.random() < 0.05:
                # Khoảng 5% sẽ có tỷ lệ dưới 75%
                counts = [int(rng.uniform(3, 6)) for _ in range(5)]
            elif rng.random() < 0.2:
                # Khoảng 15-20% sẽ có tỷ lệ từ 80% đến dưới 90%
                counts = [int(rng.uniform(6, 10)) for _ in range(5)]
            else:
                # Khoảng 75-80% sẽ có tỷ lệ từ 90% đến dưới 100%, nhưng không bao giờ đạt 100%
                counts = [int(rng.uniform(8, 16)) for _ in range(5)]

            new_counts.append(counts)

        # Kiểm tra và điều chỉnh số phiếu sao cho tổng bằng n (64 học sinh)
        for i, counts in enumerate(new_counts):
            total_counts = sum(counts)
            if total_counts != n:  # Nếu số phiếu không bằng tổng số học sinh, chỉnh lại
                diff = n - total_counts  # Số thiếu hoặc thừa
                if diff > 0:
                    # Nếu thiếu, thêm vào mức độ 4 và 5 (hài lòng cao)
                    counts[3] += diff // 2
                    counts[4] += diff - (diff // 2)
                else:
                    # Nếu thừa, giảm từ mức độ 1 và 2 (không hài lòng)
                    diff = abs(diff)
                    counts[0] = max(0, counts[0] - diff // 2)
                    counts[1] = max(0, counts[1] - (diff - diff // 2))
            new_counts[i] = counts

        # Tính tỷ lệ % dựa trên số phiếu
        new_percentages = []
        for counts in new_counts:
            total = sum(counts)
            percentages = [round(count / total * 100, 2) for count in counts]
            new_percentages.append(tuple(percentages))  # Chuyển list thành tuple

        # Kiểm tra và điều chỉnh các tỷ lệ sao cho không giống nhau liên tiếp
        for i in range(1, len(new_percentages)):
            if new_percentages[i] == new_percentages[i-1]:
                # Điều chỉnh nếu tỷ lệ giống nhau liên tiếp
                new_percentages[i] = tuple([round(rng.uniform(90, 99.99), 2) for _ in range(5)])
                # Đảm bảo không giống tỷ lệ câu trước
                if new_percentages[i] == new_percentages[i-1]:
                    new_percentages[i] = tuple([round(rng.uniform(90, 99.99), 2) for _ in range(5)])

        # In kết quả mới sinh ra để kiểm tra
        print("Tỷ lệ MỨC ĐỘ HÀI LÒNG (%) mới:")
        for i, perc in enumerate(new_percentages):
            print(f"Câu {i+1}: {perc}")

        # 6. Kiểm tra tỷ lệ bị lặp quá nhiều, điều chỉnh nếu cần
        c = Counter(new_percentages)
        for val, freq in c.items():
            if freq > 3:
                idxs = [i for i, x in enumerate(new_percentages) if x == val]
                for j in idxs[3:]:
                    new_percentages[j] = tuple([round(max(0, min(99.99, x + rng.uniform(-2, 2))), 2) for x in new_percentages[j]])

        # 7. Điều chỉnh raw data để áp dụng số phiếu mới
        df2 = df.copy()
        for idx, col in enumerate(response_cols):
            # Lấy phân phối số phiếu cho mức độ hài lòng 1-5 từ new_counts
            counts = new_counts[idx]
            # Tạo một list mới với số phiếu cho mỗi mức độ hài lòng
            new_values = [1]*counts[0] + [2]*counts[1] + [3]*counts[2] + [4]*counts[3] + [5]*counts[4]
            rng.shuffle(new_values)  # Shuffle để đảm bảo phân phối ngẫu nhiên
            df2[col] = new_values

        # 8. Ghi file mới
        out_file = f"adjusted_{file_in}"  # Tên file mới sẽ là 'adjusted_tên_file.xlsx'
        df2.to_excel(out_file, index=False)
        print(f"Hoàn thành! File đã được lưu: {out_file}")
        print(f"Tổng số học sinh: {n}")
        print(f"Tổng số câu hỏi: {len(response_cols)}")