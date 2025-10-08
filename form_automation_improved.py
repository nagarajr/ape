import pandas as pd
import random
import time
from playwright.sync_api import sync_playwright
import pyperclip

def fill_form_improved_submit(student_name):
    """Điền form với phương pháp gửi form cải tiến"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 1200, 'height': 1000},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        
        try:
            print(f"Đang xử lý: {student_name}")
            
            # Mở form với timeout dài hơn
            page.goto('https://forms.gle/DuV8MWtUL5SubSNK7', wait_until='networkidle', timeout=30000)
            page.wait_for_timeout(5000)  # Tăng thời gian chờ
            
            # Đảm bảo page đang active
            page.bring_to_front()
            
            # Điền tên với cải tiến
            print("Đang điền tên...")
            name_input = page.locator('input[type="text"]').first
            name_input.click()
            page.wait_for_timeout(1500)
            
            # Xóa nội dung cũ nếu có
            page.keyboard.press('Control+A')
            page.wait_for_timeout(500)
            
            # Nhập tên với typing tự nhiên hơn
            pyperclip.copy(student_name)
            page.keyboard.press('Control+V')
            page.wait_for_timeout(1500)
            
            # Trigger change event
            name_input.evaluate('element => element.dispatchEvent(new Event("change", { bubbles: true }))')
            page.wait_for_timeout(1000)
            print("✓ Đã điền tên")
            
            # Xử lý dropdown lớp với cải tiến
            print("Đang xử lý dropdown lớp...")
            dropdown = page.locator('div[role="listbox"]').first
            dropdown.click()
            page.wait_for_timeout(2000)
            
            # Chọn option K5C
            option = page.locator('div[role="option"]:has-text("K5C Giáo dục Mầm non")')
            option.click()
            print("✓ Đã chọn lớp K5C")
            page.wait_for_timeout(2000)
            
            # ĐIỀN CÂU HỎI với cải tiến
            print("Đang điền phần khảo sát...")
            
            # Cuộn và thu thập tất cả câu hỏi
            all_radio_groups = []
            
            # Cuộn toàn bộ trang với cải tiến
            for scroll_pass in range(3):
                print(f"Đang cuộn trang (lần {scroll_pass + 1}/3)...")
                
                page.evaluate("window.scrollTo(0, 0)")
                page.wait_for_timeout(1000)
                
                page_height = page.evaluate("document.body.scrollHeight")
                scroll_step = 300
                current_position = 0
                
                while current_position < page_height:
                    page.evaluate(f"window.scrollTo(0, {current_position})")
                    page.wait_for_timeout(300)
                    
                    current_groups = page.locator('div[role="radiogroup"]').all()
                    for group in current_groups:
                        if group not in all_radio_groups:
                            all_radio_groups.append(group)
                    
                    current_position += scroll_step
                
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(1000)
            
            print(f"Tìm thấy {len(all_radio_groups)} nhóm câu hỏi")
            
            # Điền câu hỏi với cải tiến
            filled_count = 0
            required_questions = 53
            
            for i, group in enumerate(all_radio_groups[:required_questions]):
                try:
                    group.scroll_into_view_if_needed()
                    page.wait_for_timeout(500)  # Tăng thời gian chờ
                    
                    checked_radios = group.locator('div[role="radio"][aria-checked="true"]')
                    if checked_radios.count() == 0:
                        choice = 5 if random.random() < 0.7 else 4
                        radios = group.locator('div[role="radio"]').all()
                        
                        if len(radios) >= choice:
                            # Click với force để đảm bảo
                            radios[choice-1].click(force=True)
                            page.wait_for_timeout(300)
                            
                            # Trigger change event
                            radios[choice-1].evaluate('element => element.dispatchEvent(new Event("change", { bubbles: true }))')
                            page.wait_for_timeout(200)
                            
                            if radios[choice-1].get_attribute('aria-checked') == 'true':
                                filled_count += 1
                    else:
                        filled_count += 1
                except:
                    continue
            
            # Kiểm tra final
            final_count = 0
            for i, group in enumerate(all_radio_groups[:required_questions]):
                checked_radios = group.locator('div[role="radio"][aria-checked="true"]')
                if checked_radios.count() > 0:
                    final_count += 1
            
            print(f"🎯 KẾT QUẢ CUỐI: {final_count}/{required_questions} câu đã được điền")
            
            if final_count < required_questions:
                print("❌ Không thể điền đủ câu hỏi")
                return False
            
            # === GỬI FORM VỚI CẢI TIẾN ===
            print("Đang chuẩn bị gửi form...")
            
            # Cuộn xuống cuối trang
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(3000)
            
            # Đợi form validation hoàn tất
            print("Đang đợi form validation...")
            page.wait_for_timeout(5000)
            
            # Thử nhiều phương pháp tìm và click nút Gửi
            submit_success = False
            
            # Phương pháp 1: Tìm nút submit chính
            try:
                print("Thử phương pháp 1: Tìm nút submit chính...")
                submit_selectors = [
                    'div[role="button"]:has-text("Gửi")',
                    'span:has-text("Gửi")',
                    'button:has-text("Gửi")',
                    'div[jsname="M2UYVd"]',  # Selector cụ thể của Google Forms
                    'div[data-value="Gửi"]',
                    'div[aria-label*="Gửi"]'
                ]
                
                for selector in submit_selectors:
                    submit_button = page.locator(selector).first
                    if submit_button.count() > 0 and submit_button.is_visible():
                        print(f"✓ Tìm thấy nút Gửi với selector: {selector}")
                        submit_button.scroll_into_view_if_needed()
                        page.wait_for_timeout(2000)
                        
                        # Hover trước khi click để kích hoạt
                        submit_button.hover()
                        page.wait_for_timeout(1000)
                        
                        # Click với nhiều phương pháp
                        try:
                            submit_button.click(force=True)
                        except:
                            submit_button.click()
                        
                        page.wait_for_timeout(3000)
                        
                        # Kiểm tra xem có dialog xác nhận không
                        try:
                            confirm_button = page.locator('div[role="button"]:has-text("Gửi")').first
                            if confirm_button.count() > 0 and confirm_button.is_visible():
                                print("Tìm thấy dialog xác nhận, đang click...")
                                confirm_button.click()
                                page.wait_for_timeout(3000)
                        except:
                            pass
                        
                        submit_success = True
                        break
                        
            except Exception as e:
                print(f"Lỗi phương pháp 1: {e}")
            
            # Phương pháp 2: Tìm bằng JavaScript
            if not submit_success:
                try:
                    print("Thử phương pháp 2: Tìm bằng JavaScript...")
                    submit_button = page.evaluate("""
                        () => {
                            const buttons = Array.from(document.querySelectorAll('div[role="button"], button, span'));
                            return buttons.find(btn => 
                                btn.textContent.includes('Gửi') && 
                                btn.offsetParent !== null
                            );
                        }
                    """)
                    
                    if submit_button:
                        print("✓ Tìm thấy nút Gửi bằng JavaScript")
                        page.evaluate("arguments[0].click()", submit_button)
                        page.wait_for_timeout(3000)
                        submit_success = True
                        
                except Exception as e:
                    print(f"Lỗi phương pháp 2: {e}")
            
            # Phương pháp 3: Submit form trực tiếp
            if not submit_success:
                try:
                    print("Thử phương pháp 3: Submit form trực tiếp...")
                    page.evaluate("""
                        () => {
                            const forms = document.querySelectorAll('form');
                            if (forms.length > 0) {
                                forms[0].submit();
                                return true;
                            }
                            return false;
                        }
                    """)
                    page.wait_for_timeout(3000)
                    submit_success = True
                    
                except Exception as e:
                    print(f"Lỗi phương pháp 3: {e}")
            
            # Kiểm tra kết quả gửi
            if submit_success:
                print("Đang kiểm tra kết quả gửi...")
                page.wait_for_timeout(5000)
                
                # Kiểm tra nhiều indicator thành công
                page_content = page.content()
                success_indicators = [
                    "Câu trả lời của bạn đã được ghi lại",
                    "Gửi ý kiến phản hồi khác",
                    "Cảm ơn bạn đã gửi phản hồi",
                    "Phản hồi của bạn đã được ghi lại",
                    "Thank you for your response",
                    "Your response has been recorded"
                ]
                
                if any(indicator in page_content for indicator in success_indicators):
                    print("✅ Form đã được gửi thành công!")
                    return True
                else:
                    # Kiểm tra URL có thay đổi không
                    current_url = page.url
                    if "formResponse" in current_url or "thanks" in current_url.lower():
                        print("✅ Form đã được gửi thành công (dựa trên URL)!")
                        return True
                    else:
                        print("⚠️ Không xác định được trạng thái gửi form")
                        return False
            else:
                print("❌ Không thể gửi form tự động")
                return False
                
        except Exception as e:
            print(f"✗ Lỗi: {e}")
            return False
            
        finally:
            browser.close()

# Đọc danh sách học sinh
try:
    df = pd.read_excel('danh_sach.xlsx')
    student_names = df['Họ và tên'].tolist()
    print(f"Đọc được {len(student_names)} học sinh")
except Exception as e:
    print(f"Lỗi đọc file Excel: {e}")
    exit()

# Xử lý từng học sinh
success_count = 0
for i, student_name in enumerate(student_names):
    print(f"\n{'='*60}")
    print(f"=== HỌC SINH {i+1}/{len(student_names)}: {student_name} ===")
    print(f"{'='*60}")
    
    try:
        success = fill_form_improved_submit(student_name)
        
        if success:
            success_count += 1
            print(f"✅ THÀNH CÔNG: {student_name}")
        else:
            print(f"❌ THẤT BẠI: {student_name}")
    
    except Exception as e:
        print(f"❌ LỖI NGHIÊM TRỌG: {e}")
    
    # Delay giữa các học sinh (trừ học sinh cuối)
    if i < len(student_names) - 1:
        delay = random.uniform(8, 12)  # Tăng thời gian delay
        print(f"⏳ Chờ {delay:.1f} giây trước khi tiếp tục...")
        time.sleep(delay)

print(f"\n{'='*60}")
print(f"🎉 HOÀN THÀNH! Đã xử lý {success_count}/{len(student_names)} học sinh")
print(f"{'='*60}")