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

# Cảnh báo nhiễu của WebGL phần mềm trong môi trường headless — bỏ qua.
NOISE = ("SwiftShader", "Automatic fallback", "GroupMarkerNotSet",
         "fallback to software", "deprecated", "Failed to load resource")


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):  # im lặng để output CI sạch
        pass


class ReuseServer(socketserver.TCPServer):
    allow_reuse_address = True  # phải là class attr để có hiệu lực trước khi bind


def serve():
    handler = functools.partial(QuietHandler, directory=ROOT)
    httpd = ReuseServer(("127.0.0.1", 0), handler)  # port 0 = OS chọn cổng trống
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


def main():
    httpd, port = serve()
    url = f"http://127.0.0.1:{port}/index.html"
    time.sleep(0.5)
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
        page.goto(url, wait_until="load", timeout=30000)
        page.wait_for_timeout(2500)

        check("WebGL renders (no fallback)",
              page.eval_on_selector("#nowebgl", "e=>getComputedStyle(e).display") == "none")
        check("loading screen hidden", "hide" in (page.get_attribute("#loader", "class") or ""))
        check("default body = Sun", (page.text_content("#ipName") or "").strip() in ("Mặt Trời", "Sun"))
        check("fun fact shown", page.eval_on_selector("#ipFun", "e=>e.textContent.length>0"))
        nrows = page.eval_on_selector_all("#bodyList .body-row", "els=>els.length")
        check("dwarf planets added (>=26 bodies)", nrows >= 26, f"{nrows} rows")

        # Compare mode
        page.click("#compareBtn"); page.wait_for_timeout(900)
        check("compare caption on", "on" in (page.get_attribute("#compareCap", "class") or ""))
        check("compare button active", "active" in (page.get_attribute("#compareBtn", "class") or ""))
        check("compare aria-pressed true", page.get_attribute("#compareBtn", "aria-pressed") == "true")
        page.click("#compareBtn"); page.wait_for_timeout(500)
        check("compare exits cleanly", "on" not in (page.get_attribute("#compareCap", "class") or ""))
        check("compare aria-pressed false", page.get_attribute("#compareBtn", "aria-pressed") == "false")

        # Real-distance mode
        page.click("#distanceBtn"); page.wait_for_timeout(900)
        check("distance caption on", "on" in (page.get_attribute("#distanceCap", "class") or ""))
        check("distance aria-pressed true", page.get_attribute("#distanceBtn", "aria-pressed") == "true")
        # switching to compare must turn distance off (mutually exclusive)
        page.click("#compareBtn"); page.wait_for_timeout(600)
        check("compare turns distance off", "on" not in (page.get_attribute("#distanceCap", "class") or "")
              and "on" in (page.get_attribute("#compareCap", "class") or ""))
        page.click("#compareBtn"); page.wait_for_timeout(400)

        # Tour
        page.click("#tourStartBtn"); page.wait_for_timeout(800)
        check("tour bar visible",
              page.eval_on_selector("#tourBar", "e=>getComputedStyle(e).display") != "none")
        p0 = page.text_content("#tourPos")
        check("tour includes dwarf planets (14 stops)", (p0 or "").endswith("/14"), p0)
        page.click("#tourNext"); page.wait_for_timeout(400)
        check("tour advances", page.text_content("#tourPos") != p0, f"{p0} -> {page.text_content('#tourPos')}")
        page.click("#tourExit"); page.wait_for_timeout(300)

        # Quiz: setup screen -> begin -> play through -> result + high score
        page.click("#quizStartBtn"); page.wait_for_timeout(400)
        check("quiz setup overlay shown", "on" in (page.get_attribute("#quizSetup", "class") or ""))
        page.click('#topicChips .chip[data-topic="dwarf"]'); page.wait_for_timeout(150)
        check("dwarf topic chip activates",
              "active" in (page.get_attribute('#topicChips .chip[data-topic="dwarf"]', "class") or ""))
        page.click('#topicChips .chip[data-topic="size"]'); page.wait_for_timeout(150)
        check("topic chip activates",
              "active" in (page.get_attribute('#topicChips .chip[data-topic="size"]', "class") or ""))
        page.click("#quizBegin"); page.wait_for_timeout(500)
        check("quiz bar visible",
              page.eval_on_selector("#quizBar", "e=>getComputedStyle(e).display") != "none")
        check("quiz has question", len((page.text_content("#quizQ") or "").strip()) > 0)
        page.eval_on_selector_all("#bodyList .body-row", "els=>els[2] && els[2].click()")
        page.wait_for_timeout(700)
        check("quiz gives feedback", len((page.text_content("#quizFb") or "").strip()) > 0)
        # play to completion (answer each question by clicking a body)
        for _ in range(12):
            if "on" in (page.get_attribute("#quizResult", "class") or ""):
                break
            page.eval_on_selector_all("#bodyList .body-row", "els=>els[2] && els[2].click()")
            page.wait_for_timeout(2200)
        check("quiz reaches result", "on" in (page.get_attribute("#quizResult", "class") or ""))
        check("high score line shown", len((page.text_content("#quizRecord") or "").strip()) > 0)
        page.click("#quizClose"); page.wait_for_timeout(300)

        # Accessibility
        check("canvas is focusable application", page.get_attribute("#space", "role") == "application"
              and page.get_attribute("#space", "tabindex") == "0")
        check("live region announces", len((page.text_content("#srLive") or "").strip()) > 0)
        page.click("#quizStartBtn"); page.wait_for_timeout(300)
        page.keyboard.press("Escape"); page.wait_for_timeout(300)
        check("Escape closes overlay", "on" not in (page.get_attribute("#quizSetup", "class") or ""))

        # i18n toggle
        before = page.text_content("#uiTitle")
        page.click("#langBtn"); page.wait_for_timeout(400)
        after = page.text_content("#uiTitle")
        check("language toggles", before != after, f"{before} -> {after}")

        # Sound: default MUTED on open (the user's fix), toggle works
        check("default muted on open", page.get_attribute("#musicBtn", "aria-pressed") == "false")
        page.click("#musicBtn"); page.wait_for_timeout(200)
        check("sound toggles on", page.get_attribute("#musicBtn", "aria-pressed") == "true")
        # Narration via pre-generated audio file (device-independent Vietnamese)
        page.check("#cbNarrate"); page.wait_for_timeout(200)
        page.eval_on_selector_all("#bodyList .body-row", "els=>els[3] && els[3].click()")
        page.wait_for_timeout(500)
        check("narration toggle works without crash", len((page.text_content("#ipName") or "").strip()) > 0)
        r = page.request.get(f"http://127.0.0.1:{port}/assets/narration/vi/earth.mp3")
        check("vi narration audio file served", r.status == 200, f"status {r.status}")
        page.uncheck("#cbNarrate"); page.click("#musicBtn"); page.wait_for_timeout(150)

        # Weight-on-planets calculator
        page.click("#weightBtn"); page.wait_for_timeout(300)
        check("weight panel opens", "on" in (page.get_attribute("#weightPanel", "class") or ""))
        page.fill("#weightInput", "100"); page.wait_for_timeout(200)
        rows = page.eval_on_selector_all("#weightList .wrow", "els=>els.length")
        check("weight list populated (incl. dwarf planets)", rows >= 15, f"{rows} rows")
        wtxt = page.text_content("#weightList") or ""
        check("weight computed (100kg -> Sun 2700)", "2700" in wtxt, wtxt[:60])
        check("weight includes a dwarf planet (Ceres)", ("Ceres" in wtxt), wtxt[:80])
        page.click("#weightClose"); page.wait_for_timeout(150)

        # Deep-link: state reflected in URL + loadable from URL
        check("URL has deep-link params", "body=" in page.url and "lang=" in page.url, page.url)
        page2 = browser.new_page(viewport={"width": 1100, "height": 700})
        page2.on("pageerror", lambda e: errors.append("page2: " + str(e)))
        page2.goto(f"http://127.0.0.1:{port}/index.html?body=mars&lang=en", wait_until="load", timeout=30000)
        page2.wait_for_timeout(2000)
        check("deep-link selects body", (page2.text_content("#ipName") or "").strip() == "Mars",
              page2.text_content("#ipName"))
        check("deep-link sets language", (page2.text_content("#uiTitle") or "").strip() == "SOLAR SYSTEM")
        page2.goto(f"http://127.0.0.1:{port}/index.html?body=pluto&lang=vi", wait_until="load", timeout=30000)
        page2.wait_for_timeout(2000)
        check("dwarf planet selectable (Pluto)", (page2.text_content("#ipName") or "").strip() == "Sao Diêm Vương",
              page2.text_content("#ipName"))
        page2.close()

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
