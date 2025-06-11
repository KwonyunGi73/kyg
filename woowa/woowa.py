from appium import webdriver
from appium.options.android import UiAutomator2Options
from time import sleep
from woowa_function import * # 혹은 필요한 함수만 명시적으로 import
# woowa_function.py에서 모든 함수들을 가져오기


# woowa_TC.py에서 구글 시트 관련 함수 가져오기
# (woowa_TC.py 파일이 동일 디렉토리에 있거나, PYTHONPATH에 설정되어 있어야 합니다)
try:
    from woowa_TC import connect_to_sheet, log_result
except ImportError:
    print("woowa_TC.py를 찾을 수 없습니다. 구글 시트 로깅이 비활성화됩니다.")
    # Fallback dummy functions if woowa_TC cannot be imported
    def connect_to_sheet(): return None
    def log_result(sheet, test_name, result):
        print(f"📋 [로컬 로깅] 테스트 결과: {test_name} - {result}")


def main():
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.device_name = 'pixel_7_pro' # 실제 테스트 환경에 맞게 수정
    options.platform_version = '13'     # 실제 테스트 환경에 맞게 수정
    options.automation_name = 'UiAutomator2'
    options.app_package = 'com.sampleapp' # 실제 '배달의 민족' 앱 패키지명으로 변경 필요 (예: com.woowahan.baemin)
    options.app_activity = 'com.baemin.presentation.ui.RouterActivity' # 실제 앱의 메인 액티비티로 변경 필요
    options.app_wait_activity = '*.*'
    options.no_reset = False # 테스트 환경에 따라 True 또는 False 설정

    driver = None # driver 변수 초기화
    sheet = None  # sheet 변수 초기화

    try:
        driver = webdriver.Remote("http://localhost:4723", options=options)
        driver.implicitly_wait(10) # 암시적 대기 시간 증가 (안정성 위함)
        print("✅ 배달의민족 앱 실행됨")

        # 구글 시트 연결 시도
        try:
            sheet = connect_to_sheet()
            if sheet:
                print("✅ Google Sheet에 성공적으로 연결되었습니다.")
            else: # connect_to_sheet 내부에서 오류 발생 시 None 반환 가능성 고려 (사용자 정의에 따라)
                 print("⚠️ Google Sheet 연결 객체를 받지 못했습니다. 로컬 로깅만 진행됩니다.")
        except Exception as e:
            print(f"❌ Google Sheet 연결 중 오류 발생: {e}. 로컬 로깅만 진행됩니다.")
            sheet = None # 연결 실패 시 sheet를 None으로 명시

        # 결과 기록용 헬퍼 함수
        def record_step_result(step_name, success_status):
            result_str = "PASS" if success_status else "FAIL"
            if sheet:
                log_result(sheet, step_name, result_str)
            else: # 시트 연결 실패 시 콘솔에만 출력
                print(f"📋 [시트 미연결] 테스트 결과: {step_name} - {result_str}")
            if not success_status:
                print(f"🛑 {step_name} 단계에서 실패하여 테스트를 중단할 수 있습니다. (현재는 계속 진행)")
                # 필요시 여기서 테스트 중단 로직 추가: raise Exception(f"{step_name} 실패")

        # --- 시나리오 실행 및 결과 기록 ---

        # 1. 권한 거부
        success = click_deny_permission(driver)
        record_step_result("TC_001_권한팝업_거부", success)
        # if not success: return # 첫 단계 실패 시 중단하려면 주석 해제

        # 2. 첫 팝업 처리
        success = handle_first_popup(driver)
        record_step_result("TC_002_첫_시작_팝업_처리", success)

        # 3. 팝업 버튼 클릭 (아마도 이전 팝업 후 추가적인 확인 버튼)
        success = click_popup_button_layout(driver)
        record_step_result("TC_003_팝업_내_버튼_클릭", success)
        
        # 4. 둘러보기 클릭
        success = click_look_around(driver)
        record_step_result("TC_004_둘러보기_클릭", success)
        sleep(1)

        # 5. 주소로 검색 클릭
        success = click_search_by_address(driver)
        record_step_result("TC_005_주소로_검색_화면_진입", success)
        sleep(1)

        # 6. 주소 입력창 클릭 (첫 번째 EditText)
        success = click_edit_text(driver) # 이 함수는 일반적인 EditText를 클릭하므로, 맥락에 맞는 TC 이름 사용
        record_step_result("TC_006_주소_검색_입력창_클릭", success)

        # 7. 주소 텍스트 입력
        success = input_text(driver, "광진구 화양동")
        record_step_result("TC_007_주소_입력_광진구화양동", success)

        # 8. 엔터 입력
        success = press_enter(driver)
        record_step_result("TC_008_주소_입력_후_엔터", success)
        sleep(1) # 검색 결과 로딩 대기

        # 9. 첫 번째 주소 검색 결과 클릭
        success = click_first_search_result(driver)
        record_step_result("TC_009_첫_번째_주소_검색_결과_선택", success)
        sleep(1) # 화면 전환 대기

        # 10. 상세주소 입력창 클릭 (ScrollView 내 첫 번째 EditText)
        success = click_first_edittext_in_scrollview(driver)
        record_step_result("TC_010_상세주소_입력창_클릭", success)

        # 11. 상세주소 텍스트 입력
        success = input_text(driver, "1111호") # input_text가 현재 화면의 EditText를 대상으로 하므로, 이전 단계에서 올바른 EditText가 활성화되어야 함
        record_step_result("TC_011_상세주소_입력_1111호", success)
        sleep(1)

        # 12. 상세주소 입력 후 확인 버튼 클릭
        success = click_confirm_button(driver)
        record_step_result("TC_012_상세주소_입력_확인", success)
        sleep(2) # 주소 설정 후 메인 화면 로딩 대기

        # 13. 음식 검색 버튼 클릭
        success = click_search_button(driver) # 메인 화면의 검색 버튼
        record_step_result("TC_013_음식_검색_버튼_클릭", success)

        # 14. 음식 검색어 입력
        success = input_text(driver, "국밥") # 검색 화면의 EditText에 입력
        record_step_result("TC_014_음식_검색어_입력_국밥", success)

        # 15. 엔터 입력 (음식 검색)
        success = press_enter(driver)
        record_step_result("TC_015_음식_검색어_입력_후_엔터", success)
        sleep(2) # 음식점 목록 로딩 대기

        # 16. 첫 번째 가게(RecyclerView 항목) 클릭
        success = click_first_recyclerview(driver)
        record_step_result("TC_016_첫_번째_가게_선택", success)
        sleep(2) # 가게 상세 화면 로딩 대기

        # 17. 첫 번째 '1인분' 옵션 클릭 (스크롤 포함)
        success = click_first_portion(driver)
        record_step_result("TC_017_메뉴_1인분_선택", success)
        sleep(1)

        # 18. 특정 좌표 탭 (장바구니 담기 버튼으로 추정)
        success = tap_at(driver, 1129, 2920) # 좌표는 기기/해상도에 따라 매우 민감함
        record_step_result("TC_018_장바구니_담기_버튼_탭", success)
        sleep(1) # 장바구니 담기 확인 팝업 또는 UI 변경 대기

        # 19. 장바구니 보기 클릭
        success = click_first_pocket(driver)
        record_step_result("TC_019_장바구니_보기_클릭", success)
        sleep(1) # 장바구니 화면 로딩 대기

        # 20. 알뜰배달 주문하기 클릭
        success = click_first_pocket_order(driver)
        record_step_result("TC_020_알뜰배달_주문하기_클릭", success)
        sleep(1) # 다음 화면(로그인/주문정보) 로딩 대기

        # 21. 회원 주문 팝업 닫기 (비회원 주문 시나리오로 추정)
        success = click_first_pocket_order_loginout(driver)
        record_step_result("TC_021_회원_주문_팝업_닫기", success)
        # 이 단계는 조건부로 실행될 수 있으므로, 실패 시 테스트 전체 실패로 간주할지 결정 필요

        # 22. 정보 동의 팝업 허용 (체크박스 등으로 추정)
        success = click_first_pocket_order_Information_consent(driver)
        record_step_result("TC_022_정보_제공_동의", success)
        sleep(3) # 동의 후 다음 단계 진행 대기

        # 23. 결제하기 버튼 클릭
        success = click_first_pocket_order_payment(driver)
        record_step_result("TC_023_결제하기_클릭", success)
        sleep(2) # 결제 화면 진입 대기

        print("✅ 모든 테스트 단계 실행 완료 (결과는 시트 또는 콘솔 확인)")
        print(f"최종 Contexts: {driver.contexts if driver else 'N/A'}")

    except Exception as e:
        print(f"🛑 테스트 실행 중 예기치 않은 오류 발생: {e}")
        # 예기치 않은 오류 발생 시에도 시트에 기록 (선택 사항)
        if sheet and driver: # driver가 초기화 된 후 오류 발생 시
             record_step_result("TC_ERROR_UNEXPECTED", False)
    finally:
        if driver:
            print("🌙 테스트 종료. 5초 후 드라이버 종료...")
            sleep(5)
            driver.quit()
            print("✅ 드라이버 종료됨.")

if __name__ == "__main__":
    main()

    # Test12
    