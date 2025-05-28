# 1. 구글 시트 연결 및 결과 기록 함수 (파일 맨 위)
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "C:/Users/YG/Desktop/kyg test/kyg_key/kyg_key.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1hReunu8mNO4QZ4aXjrZ_z9vWUG8uhp2pHXGLcc1styY").sheet1
    return sheet

def log_result(sheet, test_name, result):
    all_records = sheet.get_all_records()
    row = len(all_records) + 2
    sheet.update(f'A{row}', [[test_name, result]])
    print(f"📋 테스트 결과 기록 완료: {test_name} - {result}")

# 2. 테스트 실행용 시트 연결 (공통 변수)
sheet = connect_to_sheet()

# 3. 테스트 함수 예시
def test_onboarding_flow():
    test_name = "TC_01_온보딩_플로우"
    try:
        # Appium으로 온보딩 자동화 코드 작성
        print("온보딩 성공")
        log_result(sheet, test_name, "PASS")
    except Exception as e:
        print("에러 발생:", e)
        log_result(sheet, test_name, "FAIL")

# 4. 테스트 함수 호출
if __name__ == "__main__":
    test_onboarding_flow()
