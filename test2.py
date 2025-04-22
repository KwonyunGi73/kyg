from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
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

    driver = webdriver.Remote("http://localhost:4723/wd/hub", options=options)
    driver.implicitly_wait(10)  # 요소가 뜰 때까지 최대 10초 대기

    try:
        # 클릭할 요소 찾기
        target_element = driver.find_element(AppiumBy.XPATH, "//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View[1]/android.view.View[3]")
        target_element.click()
        print("클릭 성공")

    except Exception as e:
        print("에러 발생:", e)

    #앱 종료
    #finally:
     #   driver.quit()

if __name__ == "__main__":
    main()
