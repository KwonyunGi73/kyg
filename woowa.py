from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from selenium.common.exceptions import NoSuchElementException
from time import sleep

def click_deny_permission(driver):
    try:
        deny_btn = driver.find_element("xpath", '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_deny_button"]')
        deny_btn.click()
        print("알림팝업 -> 허용안함 클릭")
    except Exception as e:
        print("알림팝업 미노출", e)

def handle_first_popup(driver):
    try:
        # 위치 권한 팝업 체크박스
        location_checkbox = driver.find_element(
            AppiumBy.XPATH, '//android.view.ViewGroup[@resource-id="com.sampleapp:id/tutorialLocationCheckBox"]'
        )
        location_checkbox.click()
        print("첫 시작 팝업창 노출: 위치 권한 체크박스 클릭 완료")

        # 시작하기 버튼 클릭
        start_button = driver.find_element(
            AppiumBy.XPATH, '//androidx.compose.ui.platform.ComposeView[@resource-id="com.sampleapp:id/tutorialStartButton"]'
        )
        start_button.click()
        print("시작하기 버튼 클릭 완료")

        sleep(1)  # UI 안정화용 (필요하면 조정)

    except NoSuchElementException:
        print("첫 시작 팝업창 미노출")

def click_popup_button_layout(driver):
    try:
        button = driver.find_element(AppiumBy.XPATH, '//android.view.ViewGroup[@resource-id="com.sampleapp:id/popupButtonLayout"]')
        button.click()
        print("확인인 클릭 완료")
    except NoSuchElementException:
        print("확인 버튼 미노출")

        sleep(1)

def click_look_around(driver):
    try:
        look_around_btn = driver.find_element(
            AppiumBy.XPATH, '//android.widget.ScrollView/android.view.View[8]/android.widget.Button'
        )
        look_around_btn.click()
        print('"둘러보기" 버튼 클릭 완료')
    except NoSuchElementException:
        print('"둘러보기" 버튼 미노출, 다음 흐름 진행')

"""
def click_button(driver):
    try:
        btn = driver.find_element(AppiumBy.XPATH, '//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[2]/android.widget.Button')
        btn.click()
        print("버튼 클릭 완료")
    except NoSuchElementException:
        print("버튼을 찾을 수 없습니다.")

        sleep(10)
"""
def click_search_by_address(driver):
    try:
        btn = driver.find_element(AppiumBy.XPATH, '//android.widget.Button[@content-desc="지번, 도로명, 건물명으로 검색"]')
        btn.click()
        print("주소 검색 버튼 클릭 완료")
    except NoSuchElementException:
        print("주소 검색 버튼을 찾을 수 없습니다.")



def click_edit_text(driver):
    try:
        edit_text = driver.find_element(AppiumBy.XPATH, '//android.widget.EditText')
        edit_text.click()
        print("EditText 클릭 완료")
    except NoSuchElementException:
        print("EditText 요소를 찾을 수 없습니다.")



def input_text(driver, text):
    try:
        edit_text = driver.find_element(AppiumBy.XPATH, '//android.widget.EditText')
        edit_text.click()
        edit_text.clear()  # 기존 텍스트 지우기
        edit_text.send_keys(text)
        print(f'"{text}" 입력 완료')
    except NoSuchElementException:
        print("EditText 요소를 찾을 수 없습니다.")

def press_enter(driver):
    driver.press_keycode(66)
    print("엔터 키 입력 완료")



def click_first_search_result(driver):
    try:
        first_result = driver.find_element(AppiumBy.XPATH, '//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[3]/android.view.View[1]')
        first_result.click()
        print("첫 번째 검색 결과 클릭 완료")
    except NoSuchElementException:
        print("첫 번째 검색 결과를 찾을 수 없습니다.")


def click_first_edittext_in_scrollview(driver):
    try:
        edit_text = driver.find_element(AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.EditText[1]')
        edit_text.click()
        print("ScrollView 내 첫 번째 EditText 클릭 완료")
    except NoSuchElementException:
        print("ScrollView 내 첫 번째 EditText를 찾을 수 없습니다.")

        sleep(1)

def click_confirm_button(driver):
    try:
        button = driver.find_element(AppiumBy.XPATH, '//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[1]/android.widget.Button')
        button.click()
        print("확인 버튼 클릭 완료")
    except NoSuchElementException:
        print("확인 버튼을 찾을 수 없습니다.")


def main():
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.device_name = 'pixel_7_pro'
    options.platform_version = '13'  # API 33
    options.automation_name = 'UiAutomator2'
    options.app_package = 'com.sampleapp'
    options.app_activity = 'com.baemin.presentation.ui.RouterActivity'
    options.app_wait_activity = '*.*'
    options.no_reset = False

    driver = webdriver.Remote("http://localhost:4723", options=options)
    driver.implicitly_wait(5)

    print("✅ 배달의민족 앱 실행됨")



    #함수 시작할 코드
    click_deny_permission(driver)
    handle_first_popup(driver)
    click_popup_button_layout(driver)
    click_look_around(driver)
    sleep(10)
    #click_button(driver) 주소 입력완료까지 했지만 > 검색을 찾지못함함
    click_search_by_address(driver)
    click_edit_text(driver)
    input_text(driver, "광진구 화양동")
    press_enter(driver)
    click_first_search_result(driver)
    click_first_edittext_in_scrollview(driver)
    input_text(driver, "1111호")
    click_confirm_button(driver)
    # 여기까지 초기 사용자의 시뮬레이션

if __name__ == "__main__":
    main()