# -----------------------------------------------
# 무신사 앱 Appium 자동화 세팅 여정 (2025.04 기준)
# -----------------------------------------------
# ✅ 목적: Appium으로 무신사 앱 자동화 테스트 수행
# ✅ 기기 환경: Android Emulator (API 33, Android 13)
# ✅ 주요 이슈와 해결 과정 요약:

# 1. 앱 실행 실패 문제:
#    - 초기엔 잘못된 appActivity 입력으로 인해 자동 실행 실패
#    - 해결: logcat에서 실행 가능한 Activity 추적하여 정확한 진입점 파악

# 2. logcat 활용:
#    - adb logcat 실행 후 무신사 앱 수동 실행
#    - "cmp=com.musinsa.store/..." 로그를 통해 진입점 확인
#    - `DeepLinkActivity`가 실제 LAUNCHER 액티비티임을 발견

# 3. Appium Desired Capabilities 세팅:
#    - 올바른 appPackage 및 appActivity를 설정해야 함
#    - appActivity는 반드시 전체 패키지 경로 사용 (com.musinsa.store.XXX)

# 4. Activity Not Exported 에러:
#    - 내부 Activity로 직접 진입 시 보안 제한 걸림
#    - 해결: AndroidManifest에서 exported=true 확인된 액티비티 사용

# 5. adb 명령어 사용 팁:
#    - adb shell dumpsys window windows | grep mCurrentFocus → 현재 포커스된 액티비티 확인
#    - adb shell monkey -p com.musinsa.store -c android.intent.category.LAUNCHER 1 → 앱 강제 실행
#    - adb logcat | grep START → Activity 전환 로그 확인

# ✅ 최종 적용값:
# "appPackage": "com.musinsa.store"
# "appActivity": "com.musinsa.store.scenes.deeplink.DeepLinkActivity"
# "platformVersion": "13"
# "deviceName": "emulator-5554"
# "automationName": "UiAutomator2"
# "noReset": true

# -----------------------------------------------
# 💡 이 경험을 통해 앱 자동화에서 정확한 진입점 설정의 중요성,
#    로그 분석 및 ADB 도구 숙련도를 키울 수 있었음
# -----------------------------------------------
