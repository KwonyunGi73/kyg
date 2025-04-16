from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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

# === 4. 실행 ===
handle_permission_popup()

#  여기에 추가 자동화 로직 작성 
# 예시:
# click_if_element_exists(By.ID, "com.google.android.youtube:id/some_button")

print("▶ YouTube 자동화 시작")
