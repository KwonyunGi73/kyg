from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options # type: ignore
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import numpy as np  # ← 추가
from time import sleep


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
    driver.implicitly_wait(5)


    try:
        # 1. 조건부 팝업 닫기
        try:
            close_btn = driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="닫기"]')
            close_btn.click()
            print("팝업 닫기 완료")
        except NoSuchElementException:
            print("팝업 없음")

        # 2. 검색창으로 진입
        search_trigger = driver.find_element(AppiumBy.XPATH, "//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View[1]/android.view.View[3]")
        search_trigger.click()
        print("검색창 진입 성공")

        sleep(1)

        # 3. 텍스트 입력 필드 찾기 (EditText)
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText'))
        )
        search_input.click()  # 먼저 클릭 후 텍스트 입력
        search_input.clear()  # 기존 텍스트가 있을 경우 지우기
        search_input.send_keys("무탠다드")
        print("검색어 입력 완료")

        # 4. 엔터 키로 검색 실행
        driver.press_keycode(66)  # KEYCODE_ENTER
        print("검색 실행 완료")

        # 5. 상품 상세로 이동 버튼 클릭
        product_detail_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.view.View[@content-desc="상품 상세로 이동"])[1]'))
        )
        product_detail_button.click()
        print("상품 상세 페이지로 이동 완료")

        # 6. 좋아요 버튼 위치 저장 (처음 눌렀을 때)
        like_button = driver.find_element(AppiumBy.XPATH, '//android.widget.Button[contains(@text, "좋아요 버튼")]')
        location = like_button.location
        size = like_button.size
        x, y = location['x'], location['y']
        width, height = size['width'], size['height']
        print(f"좋아요 버튼 위치 저장: x={x}, y={y}, width={width}, height={height}")

        # 7. 전체 화면 스크린샷 찍기
        driver.save_screenshot('screenshot.png')

        # 8. 스크린샷에서 좋아요 버튼 영역 크롭
        img = Image.open('screenshot.png')
        cropped_img = img.crop((x, y, x + width, y + height))

        # 9. 좋아요 상태 이미지 비교
        like_on_img = Image.open("musinsa/musinsalikeon.png")
        like_off_img = Image.open("musinsa/musinsalikeoff.png")

        # 이미지 비교 함수 (단순 픽셀 차이로 비교)
        def compare_images(img1, img2):
            return np.array_equal(np.array(img1), np.array(img2))

        # 10. 좋아요 상태 판단
        if compare_images(cropped_img, like_on_img):
            print("좋아요가 이미 눌렸습니다.")
            # 좋아요 취소 코드 작성
            # 예: like_button.click()  # 좋아요 취소
        else:
            print("좋아요가 눌려 있지 않습니다.")
            # 좋아요 클릭 코드 작성
            # 예: like_button.click()  # 좋아요 클릭

        # 10. 좋아요 상태 판단 및 처리
        if compare_images(cropped_img, like_on_img):
            print("좋아요가 눌려져 있습니다. → 먼저 취소 후 다시 눌러야 합니다.")
            
            like_button.click()  # 먼저 좋아요 취소

            # 버튼 다시 로드될 때까지 기다림
            sleep(1)  # UI 반응 안정 시간 확보 (옵션)
            
            # 다시 좋아요 버튼을 찾음
            like_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.Button[contains(@text, "좋아요 버튼")]'))
            )
            
            # 좋아요 버튼 클릭 (좋아요 다시 눌리게)
            like_button.click()
            print("좋아요를 다시 눌렀습니다.")
        else:
            print("좋아요가 눌려 있지 않습니다. → 좋아요 누르기")
            like_button.click()  # 좋아요 눌러서 상태 변경
            print("좋아요를 눌렀습니다.")

    except Exception as e:
        print(f"오류 발생: {e}")
    # 앱 종료 안 함 (디버깅용)
    # finally:
    #     driver.quit()

if __name__ == "__main__":
    main()
