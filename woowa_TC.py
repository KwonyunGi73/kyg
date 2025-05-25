import gspread
from oauth2client.service_account import ServiceAccountCredentials

def test_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/YG/Desktop/kyg test/kyg_key/kyg_key.json", scope)
    client = gspread.authorize(creds)

    # 시트 열기 - 아래의 key는 해당 Google Sheet URL 중간에 있는 부분입니다.
    # 예: https://docs.google.com/spreadsheets/d/이부분이-key/edit
    sheet = client.open_by_key("1hReunu8mNO4QZ4aXjrZ_z9vWUG8uhp2pHXGLcc1styY").sheet1

    # A1 셀에 '테스트 완료' 라는 텍스트 입력
    sheet.update('A1', [['테스트 완료!']])
    print("A1 셀 업데이트 완료")

test_google_sheet()
