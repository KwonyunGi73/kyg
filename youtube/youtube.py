from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By # By를 사용하시므로 유지
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from appium.webdriver.common.appiumby import AppiumBy # AppiumBy도 사용하시므로 유지
from selenium.common.exceptions import NoSuchElementException
import time # time.sleep()을 위해 import
import re


options = UiAutomator2Options()
options.platform_name = 'Android'
options.device_name = 'emulator-4723' 
options.platform_version = '13.0'    
options.automation_name = 'uiautomator2'
options.app_package = 'com.google.android.youtube'
options.app_activity = 'com.google.android.youtube.HomeActivity' 
options.no_reset = False 

driver = webdriver.Remote('http://localhost:4723', options=options)
driver.implicitly_wait(5) 

# === 2. 공통 함수: 요소 클릭 === (그대로 사용)
def click_if_element_exists(by, value, timeout=5):
    """요소가 있으면 클릭, 없으면 무시"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        element.click()
        print(f"[클릭 완료] {value}")
        return True
    except TimeoutException:
        print(f"[요소 없음] {value}")
        return False

# === 3. 권한 팝업 처리 === (그대로 사용)
def handle_permission_popup():
    """권한 팝업이 있으면 첫 번째 버튼 클릭"""
    try:
        buttons = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.Button"))
        )
        if buttons:
            buttons[0].click()
            print("[권한 팝업 처리 완료] 첫 번째 버튼 클릭")
            return True
    except TimeoutException:
        print("[권한 팝업 없음] 진행 계속")
    return False


print("▶ YouTube 자동화 시작") # 스크립트 시작 알림
handle_permission_popup() # 권한 팝업 처리 시도

# 1) 검색 버튼 클릭 (XPath 사용)
try:
    search_button_xpath = '//android.widget.ImageView[@content-desc="검색"]'
    search_button = WebDriverWait(driver, 10).until( # 검색 버튼은 중요하므로 대기시간을 좀 더 줄 수 있습니다.
        EC.element_to_be_clickable((AppiumBy.XPATH, search_button_xpath))
    )
    search_button.click()
    print("✅ [검색 버튼 클릭 완료] XPath로 클릭됨")
except TimeoutException:
    print("❌ [오류] 검색 버튼을 찾을 수 없음 (XPath)")
    driver.quit() # 검색 버튼 못찾으면 진행 불가
    exit()


# 2) 검색어 입력창(EditText) 찾아서 입력
try:
    search_input_xpath = '//android.widget.EditText' # 만약 여러 EditText가 있다면 더 구체적인 XPath 필요
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.XPATH, search_input_xpath)) # By.CLASS_NAME 대신 AppiumBy.XPATH 사용
    )
    search_input.send_keys("고재영") # 검색어
    print("[검색어 입력 완료] 고재영")

    # 3) 키보드에서 Enter 키 입력 (검색 실행)
    driver.press_keycode(66)  # KEYCODE_ENTER
    print("[Enter 입력 완료] 검색 실행됨")
    time.sleep(2) # 검색 결과 로딩 대기
except TimeoutException:
    print("[검색 입력창 없음] 검색 실패")
    driver.quit()
    exit()

# --- "View Channel" 버튼을 찾거나 스크롤하며 찾는 로직 ---
view_channel_accessibility_id = '채널 보기'
max_scroll_attempts = 3  # 최대 스크롤 시도 횟수
view_channel_found_and_clicked = False

print(f"▶ '{view_channel_accessibility_id}' 버튼을 찾기 시작합니다 (최대 스크롤 {max_scroll_attempts}회 시도).")

for attempt in range(max_scroll_attempts):
    try:
        print(f"시도 {attempt + 1}/{max_scroll_attempts}: 영상상 찾기")
        view_channel_button = WebDriverWait(driver, 3).until( # 각 시도마다 대기 시간 짧게
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, view_channel_accessibility_id))
        )
        view_channel_button.click()
        print(f"✅ [채널 클릭 완료] {view_channel_accessibility_id}")
        view_channel_found_and_clicked = True
        break  # 버튼을 찾아 클릭했으므로 반복 종료
    except TimeoutException:
        print(f"ℹ️ 현재 화면에서 '{view_channel_accessibility_id}' 버튼을 찾지 못했습니다 (시도 {attempt + 1}).")
        if attempt < max_scroll_attempts - 1:
            print("   아래로 스크롤합니다...")
            try:
                size = driver.get_window_size()
                start_x = size['width'] // 2
                start_y = int(size['height'] * 0.5)
                end_y = int(size['height'] * 0.3)
                driver.swipe(start_x, start_y, start_x, end_y, 300)
                time.sleep(1.5) # 스크롤 후 UI 안정화 시간
            except Exception as scroll_e:
                print(f"   ⚠️ 스크롤 중 오류 발생: {scroll_e}")
                break 


if not view_channel_found_and_clicked:
    print(f"❌ [오류] 최대 {max_scroll_attempts}번 스크롤 후에도 '{view_channel_accessibility_id}' 요소를 찾거나 클릭할 수 없었습니다.")


if view_channel_found_and_clicked: 
    try:
        channel_name_check_xpath = "//android.view.ViewGroup[contains(@content-desc, '고재영') or contains(@text, '고재영') or descendant::android.widget.TextView[contains(@text, '고재영')]]"
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((AppiumBy.XPATH, channel_name_check_xpath))
        )
        print("✅ [1차 확인] 고재영 관련 채널 정보가 화면에 있습니다.")

        # 1차 확인이 성공하면 2차 확인 진행
        try:
            # === [2차 확인] 채널 확인 (Verified 배지) ===
            verified_badge_xpath = "//android.widget.ImageView[contains(@content-desc, 'Verified') or contains(@content-desc, '인증됨')]" # 다국어 고려
            verified_badge = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((AppiumBy.XPATH, verified_badge_xpath))
            )
            print("✅ [2차 확인] 채널이 확인됨(Verified).")
        
        except TimeoutException:
            print("ℹ️ [2차 확인 정보] 채널이 확인되지 않음(Not Verified).") # 오류가 아니라 정보일 수 있음

    except TimeoutException:
        print("❌ [1차 확인 실패] 고재영 관련 채널 정보를 찾을 수 없습니다.")



if view_channel_found_and_clicked: # 채널에 성공적으로 진입했을 때만 영상 클릭 시도
    try:
        first_video_xpath = "(//android.view.ViewGroup[contains(@content-desc, '동영상') or contains(@content-desc, 'Video')])[1]" # 예시
        first_video = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, first_video_xpath))
        )
        first_video.click()
        print("✅ [클릭 완료] 첫 번째 영상 클릭됨")
        time.sleep(3) # 영상 로드 및 광고 가능성 대기

        driver.back()
        driver.back()
        print("✅ 뒤로 가기 완료. 채널 페이지")
            
        print("▶ 두 번째 영상 클릭 시도 (스크롤 기능 포함)...")
        second_video_xpath = "(//android.view.ViewGroup[contains(@content-desc, '동영상') or contains(@content-desc, 'Video')])[2]"
        max_video_scroll_attempts = 3  # 예: 최대 3번 스크롤하며 두 번째 영상 찾기
        second_video_clicked_successfully = False

        for attempt_num in range(max_video_scroll_attempts):
            try:
                print(f"시도 {attempt_num + 1}/{max_video_scroll_attempts}찾기")

                second_video = WebDriverWait(driver, 3).until( 
                    EC.element_to_be_clickable((AppiumBy.XPATH, second_video_xpath))
                )
                second_video.click()
                print("✅ [클릭 완료] 두 번째 영상 클릭됨")
                second_video_clicked_successfully = True
                time.sleep(1) # 영상 로드 및 광고 등장 가능성 대기 (필요시 조절)
                break  # 성공했으므로 루프 탈출
            except TimeoutException:
                print(f"   ℹ️ 현재 화면에서 두 번째 영상을 찾지 못했습니다 (시도 {attempt_num + 1}).")
                if attempt_num < max_video_scroll_attempts - 1:  # 마지막 시도가 아니라면 스크롤
                    print("      아래로 스크롤합니다...")
                    try:
                        size = driver.get_window_size()
                        start_x = size['width'] // 2

                        start_y = int(size['height'] * 0.7) 
                        end_y = int(size['height'] * 0.3)
                        driver.swipe(start_x, start_y, start_x, end_y, 800) # 스와이프 시간 0.8초
                        time.sleep(1.5) # 스크롤 후 UI 안정화 및 새 요소 로드 대기
                    except Exception as scroll_e:
                        print(f"      ⚠️ 스크롤 중 오류 발생: {scroll_e}")
                        break # 스크롤 중 오류 발생 시 더 이상 시도 의미 없을 수 있음
                else: # 마지막 시도에서도 못 찾음
                    print(f"❌ [오류] 두 번째 영상({second_video_xpath})을 최대 스크롤 시도 후에도 찾거나 클릭할 수 없었습니다.")
            except Exception as e_video2: # TimeoutException 외의 다른 예외 (클릭 중 발생 등)
                print(f"❌ [오류] 두 번째 영상 클릭/처리 중 예기치 않은 오류 발생 (시도 {attempt_num + 1}): {e_video2}")
                break # 다른 중요한 예외 발생 시 루프 탈출

        if not second_video_clicked_successfully:

            print(f"--- 최종적으로 두 번째 영상({second_video_xpath}) 클릭에 실패했습니다. ---")

        video_like_button_xpath = '//android.view.ViewGroup[contains(@content-desc, "좋아함")]/android.widget.ImageView' # 더 포괄적으로
        
        # 좋아요 버튼이 토글 방식임을 고려하여, 현재 상태를 알 수 없으므로 일단 한 번 클릭합니다.
        # (정확한 상태 확인은 더 복잡한 로직이 필요하며, 현재는 '일단 누른다'에 집중)
        try:
            like_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, video_like_button_xpath))
            )
            like_button.click()
            print("✅ 영상 '좋아요' 버튼 클릭 시도 완료")
        except TimeoutException:
            print("❌ 영상 재생 화면에서 '좋아요' 버튼을 찾을 수 없습니다.")

    except TimeoutException:
        print("❌ [오류] 첫 번째 영상을 찾거나 클릭할 수 없습니다.")
    time.sleep(2)
    driver.back()#뒤로가기기
else:
    print("ℹ️ 'View Channel' 버튼을 클릭하지 못했으므로 영상 재생 및 좋아요를 시도하지 않습니다.")
target_element_xpath = '//android.support.v7.widget.RecyclerView[@resource-id="com.google.android.youtube:id/watch_list"]/android.view.ViewGroup[4]/android.view.ViewGroup/android.view.ViewGroup[1]'

try:
    
    element_to_click = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((AppiumBy.XPATH, target_element_xpath))
    )
    
    
    element_to_click.click()
    print(f"✅ 댓글창 클릭 성공")

    time.sleep(5)
    driver.back()

except TimeoutException:
    print(f"❌ 시간 초과: 요소를 찾거나 클릭 가능한 상태가 아닙니다. XPath: {target_element_xpath}")
except Exception as e: # 다른 예기치 않은 오류도 처리
    print(f"❌ 요소 클릭 중 예기치 않은 오류 발생: {e}, XPath: {target_element_xpath}")
    
    time.sleep(5)
share_button_xpath = '//android.view.ViewGroup[@content-desc="공유"]'

locator_strategy = AppiumBy.XPATH
locator_value = share_button_xpath

try:

        share_button_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((locator_strategy, locator_value))
        )
        
        share_button_element.click()
        print("✅ '공유' 버튼 클릭 성공.")
        

        time.sleep(3)

except TimeoutException:
        print(f"❌ 시간 초과: '공유' 버튼을 찾거나 클릭할 수 없습니다. (선택자: {locator_value})")
except Exception as e: 
        print(f"❌ '공유' 버튼 클릭 중 예기치 않은 오류 발생: {e}")
    
add_sharebutton_xpath = '//android.support.v7.widget.RecyclerView[@resource-id="com.google.android.youtube:id/bottom_sheet_list"]/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup[2]/android.widget.ImageView'

try:
    
    comment_input_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((AppiumBy.XPATH, add_sharebutton_xpath))
    )
    
    comment_input_field.click()
    print("✅ 링크복사 클릭 성공")

except TimeoutException:
    print(f"❌ 시간 초과: '링크복사' 입력창을 찾거나 클릭할 수 없습니다.")
except Exception as e:
    print(f"❌ '링크복사' 입력창 클릭 중 예기치 않은 오류 발생: {e}")

    driver.back()

print("▶ YouTube 자동화 종료")
# driver.quit() # 실제 자동화 완료 후에는 주석 해제하여 드라이버 종료
# Test12344533d23sddssdsd