from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from appium.webdriver.webdriver import WebDriver
from time import sleep

def click_deny_permission(driver):
    try:
        deny_btn = driver.find_element("xpath", '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_deny_button"]')
        deny_btn.click()
        print("알림팝업 -> 허용안함 클릭")
        return True
    except Exception as e:
        print(f"알림팝업 미노출 또는 오류: {e}")
        return False

def handle_first_popup(driver):
    try:
        location_checkbox = driver.find_element(
            AppiumBy.XPATH, '//android.view.ViewGroup[@resource-id="com.sampleapp:id/tutorialLocationCheckBox"]'
        )
        location_checkbox.click()
        print("첫 시작 팝업창 노출: 위치 권한 체크박스 클릭 완료")

        start_button = driver.find_element(
            AppiumBy.XPATH, '//androidx.compose.ui.platform.ComposeView[@resource-id="com.sampleapp:id/tutorialStartButton"]'
        )
        start_button.click()
        print("시작하기 버튼 클릭 완료")
        sleep(1)
        return True
    except NoSuchElementException:
        print("첫 시작 팝업창 미노출")
        return False
    except Exception as e:
        print(f"handle_first_popup 오류: {e}")
        return False

def click_popup_button_layout(driver):
    try:
        button = driver.find_element(AppiumBy.XPATH, '//android.view.ViewGroup[@resource-id="com.sampleapp:id/popupButtonLayout"]')
        button.click()
        print("확인인 클릭 완료")
        sleep(1) # 클릭 후 UI 안정화 시간
        return True
    except NoSuchElementException:
        print("확인 버튼 미노출")
        return False
    except Exception as e:
        print(f"click_popup_button_layout 오류: {e}")
        return False

def click_look_around(driver):
    try:
        look_around_btn = driver.find_element(
            AppiumBy.XPATH, '//android.widget.ScrollView/android.view.View[8]/android.widget.Button'
        )
        look_around_btn.click()
        print('"둘러보기" 버튼 클릭 완료')
        return True
    except NoSuchElementException:
        print('"둘러보기" 버튼 미노출, 다음 흐름 진행')
        return False # 미노출도 실패로 간주하거나, 시나리오에 따라 True로 할 수도 있습니다. 여기서는 False로 처리합니다.
    except Exception as e:
        print(f"click_look_around 오류: {e}")
        return False

def click_search_by_address(driver):
    try:
        btn = driver.find_element(AppiumBy.XPATH, '//android.widget.Button[@content-desc="지번, 도로명, 건물명으로 검색"]')
        btn.click()
        print("주소 검색 버튼 클릭 완료")
        return True
    except NoSuchElementException:
        print("주소 검색 버튼을 찾을 수 없습니다.")
        return False
    except Exception as e:
        print(f"click_search_by_address 오류: {e}")
        return False

def click_edit_text(driver):
    try:
        edit_text = driver.find_element(AppiumBy.XPATH, '//android.widget.EditText') # 첫 번째 EditText를 대상으로 함
        edit_text.click()
        print("EditText 클릭 완료")
        return True
    except NoSuchElementException:
        print("EditText 요소를 찾을 수 없습니다.")
        return False
    except Exception as e:
        print(f"click_edit_text 오류: {e}")
        return False

def input_text(driver, text_to_input):
    try:
        # 현재 활성화된 또는 첫 번째 EditText를 대상으로 함.
        # 더 안정적인 방법은 특정 EditText를 식별하는 XPath를 사용하는 것입니다.
        edit_text = driver.find_element(AppiumBy.XPATH, '//android.widget.EditText')
        edit_text.click() # 클릭하여 활성화 보장
        edit_text.clear()
        edit_text.send_keys(text_to_input)
        print(f'"{text_to_input}" 입력 완료')
        return True
    except NoSuchElementException:
        print("EditText 요소를 찾을 수 없습니다.")
        return False
    except Exception as e:
        print(f'"{text_to_input}" 입력 중 오류: {e}')
        return False

def press_enter(driver):
    try:
        driver.press_keycode(66) # 66은 KEYCODE_ENTER 입니다.
        print("엔터 키 입력 완료")
        return True
    except Exception as e:
        print(f"엔터 키 입력 중 오류: {e}")
        return False

def click_first_search_result(driver):
    try:
        first_result = driver.find_element(AppiumBy.XPATH, '//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[3]/android.view.View[1]')
        first_result.click()
        print("첫 번째 검색 결과 클릭 완료")
        return True
    except NoSuchElementException:
        print("첫 번째 검색 결과를 찾을 수 없습니다.")
        return False
    except Exception as e:
        print(f"click_first_search_result 오류: {e}")
        return False

def click_first_edittext_in_scrollview(driver):
    try:
        edit_text = driver.find_element(AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.EditText[1]')
        edit_text.click()
        print("ScrollView 내 첫 번째 EditText 클릭 완료")
        sleep(1) # 클릭 후 UI 안정화
        return True
    except NoSuchElementException:
        print("ScrollView 내 첫 번째 EditText를 찾을 수 없습니다.")
        return False
    except Exception as e:
        print(f"click_first_edittext_in_scrollview 오류: {e}")
        return False

def click_confirm_button(driver):
    try:
        button = driver.find_element(AppiumBy.XPATH, '//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[1]/android.widget.Button')
        button.click()
        print("확인 버튼 클릭 완료")
        return True
    except NoSuchElementException:
        print("확인 버튼을 찾을 수 없습니다.")
        return False
    except Exception as e:
        print(f"click_confirm_button 오류: {e}")
        return False

def click_search_button(driver):
    try:
        search_button = driver.find_element(
            by=AppiumBy.XPATH,
            value='//android.view.View[contains(@content-desc, "검색 버튼")]'
        )
        search_button.click()
        print("✅ 음식 검색 버튼 클릭 성공")
        return True
    except Exception as e:
        print(f"❌ 음식 검색 버튼 클릭 실패: {e}")
        return False

def click_first_recyclerview(driver):
    try:
        store_views = driver.find_elements(AppiumBy.XPATH, '//androidx.recyclerview.widget.RecyclerView//android.view.View[@content-desc]')
        if store_views:
            store_views[0].click()
            print("첫 번째 가게 항목 클릭 완료")
            return True
        else:
            print("가게 항목을 찾지 못했습니다.")
            return False
    except Exception as e:
        print(f"예외 발생: RecyclerView 내 가게 항목을 찾는 중 오류 발생: {e}")
        return False

def click_first_portion(driver: WebDriver):
    try:
        max_scrolls = 5
        for i in range(max_scrolls):
            elements = driver.find_elements(
                AppiumBy.XPATH,
                '//android.view.View[contains(@content-desc, "1인분")]'
            )
            if elements:
                elements[0].click()
                print("✅ 1인분 포함된 요소 중 첫 번째 클릭 성공")
                return True
            else:
                print(f"🔍 1인분 요소 못 찾음 → {i+1}번째 스크롤 시도")
                driver.swipe(start_x=500, start_y=900, end_x=500, end_y=750, duration=500)
                sleep(1)
        print("❌ 1인분 포함된 요소를 찾지 못했습니다.")
        return False
    except Exception as e:
        print(f"❌ 1인분 요소 클릭 실패: {e}")
        return False

def tap_at(driver, x, y, duration_ms=100):
    try:
        driver.tap([(x, y)], duration=duration_ms)
        print(f"({x}, {y}) 탭 성공(장바구니 담기기)")
        return True
    except Exception as e:
        print(f"❌ tap_at 오류 발생: {e}")
        return False

def click_first_pocket(driver):
    try:
        first_result = driver.find_element(AppiumBy.XPATH, '//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View[2]/android.view.View[4]/android.widget.Button')
        first_result.click()
        print("장바구니 보기 클릭완료")
        return True
    except NoSuchElementException:
        print("장바구니 보기 클릭실패")
        return False
    except Exception as e:
        print(f"click_first_pocket 오류: {e}")
        return False

def click_first_pocket_order(driver):
    try:
        first_result = driver.find_element(AppiumBy.XPATH, '//android.widget.Button[@text="알뜰배달 주문하기"]')
        first_result.click()
        print("알뜰배달 주문하기 클릭성공")
        return True
    except NoSuchElementException:
        print("알뜰배달 주문하기 클릭실패")
        return False
    except Exception as e:
        print(f"click_first_pocket_order 오류: {e}")
        return False

def click_first_pocket_order_loginout(driver):
    try:
        first_result = driver.find_element(AppiumBy.XPATH, '//android.widget.Button[@text="닫기"]')
        first_result.click()
        print("회원 주문 팝업 닫기")
        return True
    except NoSuchElementException:
        print("회원 주문 팝업 닫기 실패") # '실패패' 오타 수정
        return False
    except Exception as e:
        print(f"click_first_pocket_order_loginout 오류: {e}")
        return False

def click_first_pocket_order_Information_consent(driver):
    try:
        first_result = driver.find_element(AppiumBy.XPATH, '//android.view.View[@resource-id="root"]/android.view.View[6]/android.view.View[3]/android.widget.Image')
        first_result.click()
        print("내용 동의 팝업 허용")
        return True
    except NoSuchElementException:
        print("내용 동의 팝업 허용실패")
        return False
    except Exception as e:
        print(f"click_first_pocket_order_Information_consent 오류: {e}")
        return False
        
def click_first_pocket_order_payment(driver):
    try:
        first_result = driver.find_element(AppiumBy.XPATH, '//android.widget.Button[@resource-id="pay-cta-button"]')
        first_result.click()
        print("결제하기 클릭성공")
        return True
    except NoSuchElementException:
        print("결제하기 클릭실패")
        return False
    except Exception as e:
        print(f"click_first_pocket_order_payment 오류: {e}")
        return False