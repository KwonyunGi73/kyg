from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def handle_optional_popup(driver, xpath, success_message, failure_message, timeout=1):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        ).click()
        print(f"✅ {success_message}")
    except TimeoutException:
        print(f"ℹ️ {failure_message} (시간 초과)")
    except Exception as e:
        print(f"⚠️ {failure_message} 중 오류: {e}")

# --- 수정된 '좋아요 목록' 확인 함수 ---
def verify_specific_item_in_liked_list(driver, product_name_to_verify):
    """
    '좋아요 목록' 페이지에서 ★정확한 상품명 텍스트★를 가진 요소가 있는지 확인합니다.
    """
    if not product_name_to_verify:
        print("❌ '좋아요 목록' 검증 실패: PDP에서 상품명을 가져오지 못했습니다 (product_name_to_verify is None).")
        return False

    specific_product_xpath = f"//android.widget.TextView[@text='{product_name_to_verify}']"
    
    try:
        print(f"🔍 '좋아요 목록'에서 '{product_name_to_verify}' 상품을 찾는 중(사용된 XPath: {specific_product_xpath})")
        sleep(1) # 페이지 요소가 로드될 시간을 잠시 줍니다. (필요에 따라 조절)
        
        WebDriverWait(driver, 5).until( # 존재 여부 확인이므로 짧게 기다립니다.
            EC.presence_of_element_located((AppiumBy.XPATH, specific_product_xpath))
        )
        print(f"✅ '{product_name_to_verify}' 상품을 '좋아요 목록'에서 찾았습니다.")
        return True # 요소를 찾으면 True 반환
    except TimeoutException:
        print(f"❌ '{product_name_to_verify}' 상품을 '좋아요 목록'에서 찾지 못했습니다 (시간 초과 또는 요소 없음).")
        return False # 시간 내에 요소를 찾지 못하면 False 반환
    except Exception as e:
        print(f"❌ '좋아요 목록'에서 특정 상품 확인 중 예기치 않은 시스템 오류 발생: {e}")
        return False

# --- 핵심 로직 함수 (verify_item_in_liked_list 호출 부분을 수정) ---
def perform_search_and_like_sequence(driver, search_term, max_retries=1):
    targeted_product_name_from_pdp = None
    
    for attempt in range(max_retries + 1):
        print(f"\n--- 시도 {attempt + 1}/{max_retries + 1} ---")
        is_current_attempt_successful = False

        if attempt > 0:
            print("   홈으로 이동 후 검색부터 다시 시작합니다.")
            try:
                home_button_xpath = '//android.view.ViewGroup[@resource-id="com.musinsa.store:id/item_home"]'
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, home_button_xpath))
                ).click()
                print("   ✅ 홈으로 이동 성공.")
                sleep(2)
            except Exception as e:
                print(f"   ❌ 홈으로 이동 중 오류 발생: {e}. 이번 재시도를 중단합니다.")
                continue 

        try:
            print("--- 검색 및 상품 처리 시작 ---")
            # 1. 검색창으로 진입 (이하 XPath들은 실제 값으로 채워져 있다고 가정)
            search_trigger_xpath = "//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View[1]/android.view.View[3]"
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((AppiumBy.XPATH, search_trigger_xpath))).click()
            print("✅ 검색창 진입 성공")
            sleep(1)

            # 2. 검색어 입력
            search_input_xpath = '//android.widget.EditText'
            search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((AppiumBy.XPATH, search_input_xpath)))
            search_input.click()
            search_input.clear()
            search_input.send_keys(search_term) # search_term은 PDP에서 가져올 이름과 일치하거나, PDP 이름을 가져오는 XPath가 정확해야 함
            print(f"✅ '{search_term}' 입력 완료")

            # 3. 검색 실행 (엔터)
            driver.press_keycode(66)
            print("✅ 검색 완료")
            sleep(2)

            # 4. (PLP) '좋아요' 버튼 클릭
            like_button_on_plp_xpath = '(//android.widget.Button[@text="좋아요 버튼"])[1]' # !!! PLP의 특정 상품 좋아요 버튼 XPath로 개선 필요 !!!
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((AppiumBy.XPATH, like_button_on_plp_xpath))).click()
            print("✅ 좋아요 버튼 클릭 성공")
            sleep(1)

            # 5. (PLP) PDP로 이동
            pdp_link_on_plp_xpath = '(//android.view.View[@content-desc="상품 상세로 이동"])[1]' # !!! PLP의 특정 상품 PDP 링크 XPath로 개선 필요 !!!
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((AppiumBy.XPATH, pdp_link_on_plp_xpath))).click()
            print("✅ 상품 상세 페이지 이동 완료")
            sleep(5)

            product_name_pdp_xpath_stable = '//android.widget.TextView[@text="유틸리티 와이드 파라슈트 나일론 팬츠 _ 4COLOR"]'

            # print(f"✅상품명 가져오기 시도 (XPath: {product_name_pdp_xpath_stable})...")
            print(f"✅ 상품명 가져오기 시도 (유틸리티 와이드 파라슈트 나일론 팬츠 _ 4COLOR) ")
            sleep(5)
            product_name_element_pdp = WebDriverWait(driver, 10).until(EC.presence_of_element_located((AppiumBy.XPATH, product_name_pdp_xpath_stable)))
            targeted_product_name_from_pdp = product_name_element_pdp.text
            print(f"✅ 상품명 확인/저장: '{targeted_product_name_from_pdp}'")
            
            # 7. '좋아요 목록' 페이지로 이동
            # print("✅ '좋아요 목록' 페이지로 이동 시도...")
            driver.back() 
            sleep(1)
            navigate_to_liked_page_xpath = '(//android.widget.ImageView[@resource-id="com.musinsa.store:id/image_view"])[4]' # 사용자 제공
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((AppiumBy.XPATH, navigate_to_liked_page_xpath))).click()
            print("✅ '좋아요 목록' 페이지로 이동")
            sleep(2)

            # 8. '좋아요 목록'에서 ★수정된 함수★를 사용하여 상품명 최종 확인
            print("✅ '좋아요 목록'에서 상품명 최종 확인")
            if verify_specific_item_in_liked_list(driver, targeted_product_name_from_pdp): # 수정된 함수 호출
                print(f"🎉 시도 {attempt + 1} 성공: '{targeted_product_name_from_pdp}' 상품이 '좋아요 목록'에 있습니다.")
                return True # 전체 함수 성공 종료
            else:
                print(f"⚠️ 시도 {attempt + 1} 실패: '{targeted_product_name_from_pdp}' 상품을 '좋아요 목록'에서 찾지 못했습니다.")
        
        except TimeoutException as te:
            print(f"❌ 시도 {attempt + 1} 중 시간 초과 오류: {te}")
        except Exception as e:
            print(f"❌ 시도 {attempt + 1} 중 예기치 않은 오류: {e}")
        
        if attempt < max_retries: # 현재 시도 실패했고, 재시도 횟수 남았으면
            print(f"   다음 재시도를 준비합니다...")
            sleep(1)
        elif attempt >= max_retries: # 모든 시도 후에도 성공 못함
            print(f"--- 모든 시도({attempt + 1}) 후에도 상품을 '좋아요 목록'에서 찾지 못했습니다. ---")
            return False

    print(f"--- 모든 재시도({max_retries + 1}) 후 최종 실패 ---") # 루프가 정상적으로 끝났지만 성공 못한 경우
    return False


def main():
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.device_name = 'emulator-5554'
    options.platform_version = '13'
    options.automation_name = 'UiAutomator2'
    options.app_package = 'com.musinsa.store'
    options.app_activity = 'com.musinsa.store.scenes.deeplink.DeepLinkActivity'
    options.app_wait_activity = '*.*'
    options.no_reset = True 

    driver = webdriver.Remote("http://localhost:4723", options=options)
    driver.implicitly_wait(10)

    try:
        handle_optional_popup(driver, '//android.widget.TextView[@text="취소"]', "권한 관련 '취소' 팝업 닫기 완료", "권한 관련 '취소' 팝업 없음")
        handle_optional_popup(driver, '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_deny_button"]', "시스템 알림 '거부' 팝업 닫기 완료", "시스템 알림 '거부' 팝업 없음")
        handle_optional_popup(driver, '//android.widget.TextView[@text="닫기"]', "일반 '닫기' 팝업 닫기 완료", "일반 '닫기' 팝업 없음", timeout=1)
        
        search_term_for_test = "유틸리티 와이드 파라슈트 나일론 팬츠" # PDP에서 실제로 가져올 상품명과 일치하거나, PDP 상품명 가져오는 XPath가 정확해야 함

        if perform_search_and_like_sequence(driver, search_term_for_test, max_retries=1):
            print("\n🎉 전체 테스트 시나리오 성공!")
        else:
            print("\n💔 전체 테스트 시나리오 실패.")

    except Exception as e:
        print(f"💥 메인 스크립트 실행 중 최상위 예외 발생: {e}")
    finally:
        print("\n(테스트가 종료되었습니다. 필요시 driver.quit() 활성화)")
        # sleep(5)
        # driver.quit()

if __name__ == "__main__":
    main()