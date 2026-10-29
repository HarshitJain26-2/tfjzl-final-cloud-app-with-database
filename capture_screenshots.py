import os
import sys
import time
import subprocess
from playwright.sync_api import sync_playwright

def main():
    proj_dir = os.path.abspath(r"C:\Users\Harshit\Desktop\Coursera\tfjzl-final-cloud-app-with-database")
    shots_dir = os.path.join(proj_dir, "screenshots")
    os.makedirs(shots_dir, exist_ok=True)

    print("Starting Django development server on port 8000...")
    server = subprocess.Popen(
        [sys.executable, "manage.py", "runserver", "127.0.0.1:8000", "--noreload"],
        cwd=proj_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        time.sleep(3)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={'width': 1280, 'height': 800})
            page = context.new_page()

            # Task 3: Admin Site Screenshot
            print("Navigating to admin login...")
            page.goto("http://127.0.0.1:8000/admin/login/?next=/admin/")
            page.fill("input[name='username']", "admin")
            page.fill("input[name='password']", "admin12345")
            page.click("input[type='submit']")

            page.wait_for_selector("#content")
            time.sleep(1)

            admin_shot_path = os.path.join(shots_dir, "03-admin-site.png")
            page.screenshot(path=admin_shot_path, full_page=True)
            print(f"Captured admin screenshot: {admin_shot_path}")

            # Task 7: Mock Exam & Final Screenshot
            print("Logging into online course application as student...")
            page.goto("http://127.0.0.1:8000/onlinecourse/login/")
            page.fill("input[name='username']", "student")
            page.fill("input[name='psw']", "student12345")
            page.click("button[type='submit']")
            time.sleep(1)

            print("Navigating to Course Details...")
            page.goto("http://127.0.0.1:8000/onlinecourse/1/")
            time.sleep(1)

            # Open collapse exam
            print("Expanding exam section...")
            page.click("button:has-text('Start Exam')")
            time.sleep(1)

            # Select correct answers:
            # Q1: print("Hello World")
            # Q2: tuple
            # Q3: def
            checkboxes = page.query_selector_all("input[type='checkbox']")
            for cb in checkboxes:
                cb_id = cb.get_attribute("id")
                label_handle = page.query_selector(f"label[for='{cb_id}']")
                label_text = label_handle.inner_text().strip() if label_handle else ""
                if label_text in ['print("Hello World")', 'tuple', 'def']:
                    cb.check()
                    print(f"Checked correct choice: {label_text}")

            print("Submitting exam...")
            page.click("button:has-text('Submit Exam')")

            page.wait_for_selector(".alert-success")
            time.sleep(1)

            final_shot_path = os.path.join(shots_dir, "07-final.png")
            page.screenshot(path=final_shot_path, full_page=True)
            print(f"Captured final exam result screenshot: {final_shot_path}")

            browser.close()
            print("Automation completed successfully!")
    finally:
        print("Stopping Django server...")
        server.terminate()
        server.wait()

if __name__ == "__main__":
    main()

