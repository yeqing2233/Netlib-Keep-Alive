import os
import time
from playwright.sync_api import sync_playwright

# 从环境变量解析多个账号
accounts_env = os.environ.get("SITE_ACCOUNTS", "")
accounts = []

for item in accounts_env.split(";"):
    if item.strip():
        try:
            username, password = item.split(",", 1)
            accounts.append({"username": username.strip(), "password": password.strip()})
        except ValueError:
            print(f"⚠️ 忽略格式错误的账号项: {item}")

fail_msgs = [
    "Invalid credentials.",
    "Not connected to server.",
    "Error with the login: login size should be between 2 and 50 (currently: 1)"
]

def login_account(playwright, USER, PWD):
    print(f"🚀 开始登录账号: {USER}")
    try:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.netlib.re/")
        time.sleep(5)

        page.get_by_text("Login").click()
        time.sleep(2)
        page.get_by_role("textbox", name="Username").fill(USER)
        time.sleep(2)
        page.get_by_role("textbox", name="Password").fill(PWD)
        time.sleep(2)
        page.get_by_role("button", name="Validate").click()
        page.wait_for_load_state("networkidle")
        time.sleep(2)

        success_text = "You are the exclusive owner of the following domains."
        if page.query_selector(f"text={success_text}"):
            print(f"✅ 账号 {USER} 登录成功")
            time.sleep(5)
        else:
            failed_msg = None
            for msg in fail_msgs:
                if page.query_selector(f"text={msg}"):
                    failed_msg = msg
                    break
            if failed_msg:
                print(f"❌ 账号 {USER} 登录失败: {failed_msg}")
            else:
                print(f"❌ 账号 {USER} 登录失败: 未知错误")

        context.close()
        browser.close()

    except Exception as e:
        print(f"❌ 账号 {USER} 登录异常: {e}")

def run():
    with sync_playwright() as playwright:
        for acc in accounts:
            login_account(playwright, acc["username"], acc["password"])
            time.sleep(2)

if __name__ == "__main__":
    run()
