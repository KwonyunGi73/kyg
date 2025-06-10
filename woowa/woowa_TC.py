import gspread
from oauth2client.service_account import ServiceAccountCredentials
# 최신 라이브러리 사용 권장: from google.oauth2.service_account import Credentials
# from google.auth.transport.requests import Request

def connect_to_sheet():
    # ... (기존 연결 코드는 동일하게 유지)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "C:/Users/YG/Desktop/kyg test/kyg_key/kyg_key.json", scope) # 🚨 경로 확인!
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1hReunu8mNO4QZ4aXjrZ_z9vWUG8uhp2pHXGLcc1styY").sheet1
    return sheet
    

def log_result(sheet, test_name, result):
    try:
        # sheet.get_all_records() 대신 append_row 사용
        # append_row는 시트의 데이터가 있는 마지막 행 다음에 새 행으로 데이터를 추가합니다.
        # 헤더를 직접 파싱하지 않으므로, 헤더 관련 문제에서 좀 더 자유롭습니다.
        values_to_append = [test_name, result]  # A열에 test_name, B열에 result
        sheet.append_row(values_to_append)
        print(f"📋 테스트 결과 기록 완료 (새 행 추가): {test_name} - {result}")
    except Exception as e:
        print(f"❌ Google Sheet에 결과 기록 중 오류 발생: {e}")
        print(f"📋 [로컬 기록 대체] {test_name} - {result}")

# --- 아래는 woowa_TC.py를 직접 실행할 때 사용되는 예시 코드 ---
# (woowa.py에서 import하여 사용할 때는 호출되지 않음)
def test_onboarding_flow(): # 예시 함수
    test_name = "TC_01_온보딩_플로우"
    # 이 함수는 woowa.py에 통합되었으므로 여기서는 직접 사용하지 않음
    # 시트 연결은 main()에서 한 번만 하는 것이 효율적
    # sheet = connect_to_sheet() # 매번 연결 X
    try:
        print("온보딩 자동화 코드 실행 (가정)...")
        # Appium으로 온보딩 자동화 코드 작성 (가정)
        print("온보딩 성공")
        # log_result(sheet, test_name, "PASS") # main에서 처리
    except Exception as e:
        print("에러 발생:", e)
        # log_result(sheet, test_name, "FAIL") # main에서 처리

if __name__ == "__main__":
    # woowa_TC.py를 직접 실행하기 위한 테스트 코드 (선택 사항)
    print("woowa_TC.py 직접 실행 테스트 (실제 자동화는 woowa.py에서 실행)")
    # temp_sheet = connect_to_sheet()
    # if temp_sheet:
    #    log_result(temp_sheet, "TC_DUMMY_TEST_FROM_TC_PY", "PASS")
    # test_onboarding_flow()
    # Test