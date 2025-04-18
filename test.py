from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import re

# === 1. Appium 설정 ===
options = UiAutomator2Options()
options.platform_name = 'Android'
options.device_name = 'emulator-5554'
options.platform_version = '15.0'
options.automation_name = 'uiautomator2'
options.app_package = 'com.google.android.youtube'
options.app_activity = 'com.google.android.youtube.HomeActivity'

driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)

# === 2. 공통 함수: 요소 클릭 ===
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

# === 3. 권한 팝업 처리 ===
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

# === (추가) accessibility id로 클릭하는 함수 ===
def click_if_accessibility_id_exists(accessibility_id, timeout=3):
    """accessibility id로 요소 찾고 클릭"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(('accessibility id', accessibility_id))
        )
        element.click()
        print(f"[클릭 완료] '{accessibility_id}'")
        return True
    except TimeoutException:
        print(f"[요소 없음] '{accessibility_id}'")
        return False

# === 4. 실행 ===
handle_permission_popup()

# 1) 검색 버튼 (Search YouTube) 클릭
click_if_accessibility_id_exists("Search YouTube")

# 2) 검색어 입력창(EditText) 찾아서 입력
try:
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "android.widget.EditText"))
    )
    search_input.send_keys("고재영")
    print("[검색어 입력 완료] 고재영")

    # 3) 키보드에서 Enter 키 입력 (검색 실행)
    driver.press_keycode(66)  # KEYCODE_ENTER
    print("[Enter 입력 완료] 검색 실행됨")
except TimeoutException:
    print("[검색 입력창 없음] 검색 실패")

try:
    # "View Channel" 버튼을 기다렸다가 클릭
    view_channel = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(('accessibility id', 'View Channel'))
    )
    view_channel.click()
    print("[채널 클릭 완료] View Channel")
except TimeoutException:
    print("[오류] 'View Channel' 요소를 찾을 수 없음")


try:
    # === [1차 확인] "고재영"이 포함된 채널 확인 ===
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//android.view.ViewGroup[contains(@content-desc, '고재영')]"))
    )
    print("✅ [1차 확인] 고재영 관련 채널로 진입했습니다.")

    # 1차 확인이 성공하면 2차 확인 진행
    try:
        # === [2차 확인] 채널 확인 ===
        # 여기서는 Verified 포함된 요소를 확인
        verified_badge = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//android.widget.ImageView[contains(@content-desc, 'Verified')]"))
        )
        print("✅ [2차 확인] 고재영 채널의 확인됨.")
    
    except TimeoutException:
        # 2차 확인 실패 시, 코드 실행은 되지만 메시지를 출력
        print("❌ [2차 확인 실패] 고재영 채널의 확인할 수 없습니다.")

except TimeoutException:
    # 1차 확인 실패 시, 이후 2차 확인을 진행하지 않고 바로 종료
    print("❌ [오류] 고재영 채널에 진입하지 못했습니다.")


try:
    # 첫 번째 영상 클릭 (영상 리스트 중 첫 번째 ViewGroup)
    first_video = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "(//android.view.ViewGroup[contains(@content-desc, 'Go to channel')])[1]"))
    )
    first_video.click()
    print("✅ [클릭 완료] 첫 번째 영상 클릭됨")
except TimeoutException:
    print("❌ [오류] 첫 번째 영상을 찾을 수 없습니다.")
    
try:
    close_ad = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//android.widget.ImageView[@content-desc='Close ad panel']"))
    )
    close_ad.click()
    print("✅ [광고 닫기 완료] 광고가 감지되어 닫았습니다.")
except TimeoutException:
    print("ℹ️ [광고 없음] 광고가 감지되지 않았습니다.")


print("▶ YouTube 자동화 시작")
