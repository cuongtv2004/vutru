#!/usr/bin/env python3
"""
Sinh file audio đọc lời kể (tiếng Việt + Anh) cho từng thiên thể bằng gTTS.
Chạy lại khi đổi tên/fun fact trong index.html:

    python3 -m pip install --break-system-packages gTTS playwright
    python3 -m playwright install chromium
    python3 tools/gen-narration.py     # ghi vào assets/narration/<lang>/<id>.mp3

Lấy đúng chuỗi narration (name + fun fact) trực tiếp từ globals I18N/FUN của trang.
"""
import http.server, socketserver, threading, functools, os, time
from playwright.sync_api import sync_playwright
from gtts import gTTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
class R(socketserver.TCPServer): allow_reuse_address = True
h = R(("127.0.0.1", 0), functools.partial(Q, directory=ROOT)); threading.Thread(target=h.serve_forever, daemon=True).start()
port = h.server_address[1]

# Lấy đúng chuỗi narration từ globals của trang
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--use-gl=angle","--use-angle=swiftshader","--enable-unsafe-swiftshader"])
    pg = b.new_page(); pg.goto(f"http://127.0.0.1:{port}/index.html", wait_until="load"); pg.wait_for_timeout(1500)
    data = pg.evaluate("""() => {
      const out = {};
      for (const lang of ['vi','en']) {
        out[lang] = {};
        for (const id of Object.keys(I18N[lang].bodies)) {
          const name = I18N[lang].bodies[id].name;
          const fun = (FUN[lang] && FUN[lang][id]) || '';
          out[lang][id] = name + '. ' + fun;
        }
      }
      return out;
    }""")
    b.close()
h.shutdown()

total = 0; fail = []
for lang in ['vi','en']:
    d = os.path.join(ROOT, "assets/narration", lang); os.makedirs(d, exist_ok=True)
    for id, text in data[lang].items():
        path = os.path.join(d, id + ".mp3")
        for attempt in range(3):
            try:
                gTTS(text, lang=lang).save(path); total += 1
                print(f"  {lang}/{id}.mp3  ({os.path.getsize(path)}b)")
                break
            except Exception as e:
                if attempt == 2: fail.append(f"{lang}/{id}: {e}")
                else: time.sleep(1.5)
        time.sleep(0.3)
print(f"\nGenerated {total} files. Failures: {fail or 'none'}")
