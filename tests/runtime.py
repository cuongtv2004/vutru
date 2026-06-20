#!/usr/bin/env python3
"""
Runtime smoke test cho Hệ Mặt Trời 3D — chạy trang thật trong Chromium headless,
bắt lỗi JS, và kiểm tra các tính năng chính (tour, quiz, so sánh kích thước, i18n).

Cách chạy local (cần Python + Playwright):
    python3 -m pip install --break-system-packages playwright
    python3 -m playwright install --with-deps chromium
    bash download-assets.sh            # đảm bảo assets/ đầy đủ
    python3 tests/runtime.py

Thoát mã 0 = đạt, khác 0 = có lỗi (dùng cho CI).
"""
import http.server, socketserver, threading, functools, os, sys, time
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 8222
URL = f"http://127.0.0.1:{PORT}/index.html"

# Cảnh báo nhiễu của WebGL phần mềm trong môi trường headless — bỏ qua.
NOISE = ("SwiftShader", "Automatic fallback", "GroupMarkerNotSet",
         "fallback to software", "deprecated", "Failed to load resource")


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):  # im lặng để output CI sạch
        pass


def serve():
    handler = functools.partial(QuietHandler, directory=ROOT)
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    httpd.allow_reuse_address = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def main():
    httpd = serve()
    time.sleep(0.8)
    errors, console_err, checks = [], [], []

    def check(name, cond, detail=""):
        checks.append((name, bool(cond), detail))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=[
            "--use-gl=angle", "--use-angle=swiftshader",
            "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: console_err.append(m.text) if m.type == "error" else None)
        page.goto(URL, wait_until="load", timeout=30000)
        page.wait_for_timeout(2500)

        check("WebGL renders (no fallback)",
              page.eval_on_selector("#nowebgl", "e=>getComputedStyle(e).display") == "none")
        check("loading screen hidden", "hide" in (page.get_attribute("#loader", "class") or ""))
        check("default body = Sun", (page.text_content("#ipName") or "").strip() in ("Mặt Trời", "Sun"))
        check("fun fact shown", page.eval_on_selector("#ipFun", "e=>e.textContent.length>0"))

        # Compare mode
        page.click("#compareBtn"); page.wait_for_timeout(900)
        check("compare caption on", "on" in (page.get_attribute("#compareCap", "class") or ""))
        check("compare button active", "active" in (page.get_attribute("#compareBtn", "class") or ""))
        page.click("#compareBtn"); page.wait_for_timeout(500)
        check("compare exits cleanly", "on" not in (page.get_attribute("#compareCap", "class") or ""))

        # Tour
        page.click("#tourStartBtn"); page.wait_for_timeout(800)
        check("tour bar visible",
              page.eval_on_selector("#tourBar", "e=>getComputedStyle(e).display") != "none")
        p0 = page.text_content("#tourPos")
        page.click("#tourNext"); page.wait_for_timeout(400)
        check("tour advances", page.text_content("#tourPos") != p0, f"{p0} -> {page.text_content('#tourPos')}")
        page.click("#tourExit"); page.wait_for_timeout(300)

        # Quiz
        page.click("#quizStartBtn"); page.wait_for_timeout(600)
        check("quiz bar visible",
              page.eval_on_selector("#quizBar", "e=>getComputedStyle(e).display") != "none")
        check("quiz has question", len((page.text_content("#quizQ") or "").strip()) > 0)
        page.eval_on_selector_all("#bodyList .body-row", "els=>els[1] && els[1].click()")
        page.wait_for_timeout(700)
        check("quiz gives feedback", len((page.text_content("#quizFb") or "").strip()) > 0)
        page.click("#quizExit"); page.wait_for_timeout(300)

        # i18n toggle
        before = page.text_content("#uiTitle")
        page.click("#langBtn"); page.wait_for_timeout(400)
        after = page.text_content("#uiTitle")
        check("language toggles", before != after, f"{before} -> {after}")

        browser.close()

    httpd.shutdown()

    filt = [c for c in console_err if not any(n in c for n in NOISE)]
    check("no uncaught JS errors", not errors, "; ".join(errors))
    check("no console errors", not filt, "; ".join(filt))

    print("=== RUNTIME TEST ===")
    failed = 0
    for name, ok, detail in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))
        if not ok:
            failed += 1
    print(f"\n{len(checks)-failed}/{len(checks)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
