# 🪐 Hệ Mặt Trời 3D — Handoff & Kế hoạch tiếp tục

Tài liệu bàn giao để **session mới** tiếp tục phát triển. Đọc file này trước khi làm.

> Mục tiêu sản phẩm: web mô phỏng hệ mặt trời 3D **cho các bé học tập**. Ưu tiên: chạy offline, song ngữ Việt/Anh (mặc định tiếng Việt), thân thiện trẻ em, dùng được trên máy tính bảng trường học.

---

## 1. Trạng thái hiện tại

- **Repo:** `cuongtv2004/vutru` (remote SSH). Deploy bằng **GitHub Pages** (branch `main`, thư mục gốc) → `https://cuongtv2004.github.io/vutru/`.
- **Đã merge vào `main`:** Phase 0–11 (xem mục 3), hạ tầng test + CI, các bản sửa lỗi & cải thiện âm thanh.
- **PR đang chờ merge:** `phase-11-dwarf` (thêm 5 hành tinh lùn) — *kiểm tra lại đã merge chưa; nếu rồi thì bỏ qua.*
- **Branch hiện tại của tài liệu này:** `docs/handoff`.

---

## 2. Kiến trúc & quy ước (QUAN TRỌNG — đọc kỹ)

### Cấu trúc file
```
index.html                 # TOÀN BỘ app trong 1 file (data + i18n + CSS + Three.js). ~1300 dòng.
download-assets.sh         # tải Three.js + texture về assets/ (chạy 1 lần, cần mạng)
tools/gen-narration.py     # sinh lại file audio đọc lời kể (gTTS) khi đổi tên/fun fact
tests/runtime.py           # smoke test runtime (Playwright headless) — 39 checks
.github/workflows/runtime-test.yml   # CI chạy test trên mỗi PR
CHANGELOG.md               # nhật ký từng phase
assets/
  ├─ audio.mp3             # nhạc nền
  ├─ vendor/three.min.js   # Three.js r128 (tải bằng download-assets.sh, đã commit)
  ├─ textures/*.jpg        # texture hành tinh (đã commit, cho GitHub Pages)
  └─ narration/<vi|en>/<id>.mp3   # 52 file đọc lời kể (sinh bằng gTTS, đã commit)
```

### `index.html` — tổ chức bên trong
- **Script data (global, đầu file):** `DATA` (mảng thiên thể), `I18N` (vi/en: ui + bodies{name,desc,stats}), `FUN` (fun fact vi/en theo id), `QUIZ` (câu hỏi có `cat`), `GRAV` (trọng lực bề mặt).
  - Thêm thiên thể = thêm 1 phần tử `DATA` + bản dịch trong `I18N.vi.bodies`/`I18N.en.bodies` + `FUN.vi`/`FUN.en`. **Bắt buộc đủ cả 2 ngôn ngữ** (test sẽ kiểm).
- **Three.js init + `boot()`:** tất cả logic trong `boot()`. Body data → `makeBody()` → mảng `bodies` + map `byId` (cả mặt trăng đều có trong `byId`).
- **Các chế độ loại trừ lẫn nhau:** Guided tour, Quiz, So sánh kích thước (`compareMode`), Khoảng cách thật (`distanceMode`). Khi bật cái này phải tắt cái kia (xem `setCompare`/`setDistance`/`startTour`/`openQuizSetup`).
- **i18n:** mọi chuỗi UI nằm trong `I18N[lang].ui`; hàm `applyLang()` gán lại text khi đổi ngôn ngữ. Thêm chuỗi mới → thêm vào cả `vi.ui` và `en.ui` + gán trong `applyLang()`.
- **Âm thanh:** nút `🔊/🔇` (`setSound`) là **master mute**, **mặc định TẮT**, nhớ `localStorage('ssSound')`, tắt cả nhạc + hiệu ứng quiz (`blip`) + lời kể.
- **Đọc lời kể:** `playNarration(id, text)` ưu tiên phát `assets/narration/<lang>/<id>.mp3`; lỗi/thiếu file mới fallback Web Speech (`speakWeb`). Lý do dùng file: **nhiều thiết bị không có giọng TTS tiếng Việt** → Web Speech đọc giọng Anh.
- **Deep-link:** `updateURL()` ghi `?body=&lang=&view=` (replaceState); đọc lại lúc load (`urlParams`).

### Quy ước làm việc (BẮT BUỘC)
1. **Mỗi phase = 1 branch riêng → mở PR vào `main`.** User tự merge (mình KHÔNG merge). `gh` CLI không cài → đưa link `https://github.com/cuongtv2004/vutru/pull/new/<branch>` cho user.
2. **KHÔNG thêm dòng `Co-Authored-By` vào commit message** (mọi commit, mọi dự án — yêu cầu của user).
3. **Luôn chạy `python3 tests/runtime.py` trước khi báo xong** một thay đổi `index.html`. Thêm checks mới cho tính năng mới. Mục tiêu: tất cả PASS, 0 lỗi JS.
4. Khi không truy cập được tài nguyên (mạng/headless), **báo user ngay**, đừng đoán mò.
5. Sau khi user merge → `git checkout main && git pull` rồi branch tiếp.

---

## 3. Đã hoàn thành (Phase 0–11)

| Phase | Nội dung |
|---|---|
| 0 | Gộp i18n 1 file, offline-first (self-host Three.js+texture), InstancedMesh vành đai, loading screen, WebGL fallback, a11y cơ bản |
| 1 | Guided tour (camera tự bay 9 thiên thể) + fun facts + đọc lời kể |
| 2 | Quiz "học mà chơi" (bấm thiên thể trả lời) + confetti + âm thanh |
| 3 | So sánh kích thước thật (📏) |
| 4 | Quiz nâng cao: chọn chủ đề/số câu, 19 câu, lưu điểm cao |
| 5 | Deep-link & chia sẻ (`?body=&lang=&view=`) + nút 🔗 |
| 7 | Accessibility: bàn phím, prefers-reduced-motion, aria-live/pressed |
| 8 | Khoảng cách thật theo AU (🛰️) |
| 9 | Polish: hào quang Mặt Trời, khí quyển Trái Đất, lớp sao, vòng chọn |
| 10 | Cân nặng của bé trên các thiên thể (⚖️) |
| 11 | 5 hành tinh lùn (Ceres, Sao Diêm Vương + Charon, Haumea, Makemake, Eris) — *PR có thể đang chờ merge* |
| + | Hạ tầng test+CI; nút tắt tiếng (mặc định tắt); đọc lời kể bằng file audio tiếng Việt |

*(Phase 6 — PWA — đã BỎ vì chỉ cần chạy GitHub Pages.)*

---

## 4. Phần còn dở / chưa làm

- **Chưa có gì lỗi nghiêm trọng đang treo.** Tất cả phase đã merge đều xanh test.
- **Cần để ý sau khi thêm thiên thể/đổi nội dung:** chạy lại `python3 tools/gen-narration.py` để cập nhật file audio đọc lời kể, rồi commit. (Cần `pip install gTTS playwright` + mạng.)
- **Giọng đọc:** đang dùng gTTS (Google). Nếu cần giấy phép sạch hoặc chất lượng cao hơn → cân nhắc giọng khác (eSpeak-ng offline / dịch vụ TTS có bản quyền).
- **Các fixed-list chưa bao gồm hành tinh lùn:** tour (`tourOrder`), so sánh (`compareOrder`), khoảng cách (`distanceItems`), cân nặng (`weightBody`), quiz. Có thể bổ sung nếu muốn (cân nhắc tỉ lệ/độ phức tạp).

---

## 5. Roadmap các phase tiếp theo (gợi ý, ưu tiên cho trẻ)

### P12 — Chế độ giáo viên / Bài giảng
- Một "kịch bản" gồm các bước (slide): mỗi bước = chọn 1 thiên thể + 1 đoạn dẫn + (tuỳ chọn) 1 câu hỏi thảo luận hiện trên màn.
- UI: thanh điều hướng bước (◀ ▶) + ô hiển thị nội dung; có thể tái dùng cơ chế guided tour.
- Dữ liệu kịch bản đặt trong 1 mảng `LESSON` (song ngữ). Cho phép "in" (window.print với CSS @media print) ra phiếu.
- Test: mở chế độ, next/prev bước, nội dung đổi.

### P14 — Nhật/Nguyệt thực & pha Mặt Trăng
- Cảnh cận: Mặt Trời – Trái Đất – Mặt Trăng, minh hoạ pha Mặt Trăng (góc chiếu sáng) và khi thẳng hàng → nhật/nguyệt thực (bóng).
- Có thể làm như 1 "mini-scene" riêng (nút mở overlay canvas nhỏ) hoặc 1 chế độ camera đặc biệt.
- Lưu ý: cần ánh sáng định hướng từ Mặt Trời để thấy pha; tôn trọng reduced-motion.

### P15 — Chòm sao / So sánh sao
- Chế độ vẽ vài chòm sao quen thuộc lên starfield (đường nối + tên), hoặc so sánh kích thước Mặt Trời với các sao khác (Sirius, Betelgeuse...).
- Tái dùng pattern "chế độ" như compare/distance (group riêng + caption + loại trừ lẫn nhau).

### Ý tưởng khác
- Thêm hành tinh lùn vào quiz/tour/cân nặng.
- Chế độ "ngày/đêm trên Trái Đất", mùa.
- Tìm kiếm thiên thể (ô search lọc sidebar).
- Chế độ thử thách quiz tính giờ; bảng xếp hạng cục bộ.

---

## 6. Cách phát triển & test nhanh

```bash
# Chạy app local (không cần Node):
python3 -m http.server 8000        # mở http://localhost:8000

# Chạy test runtime (cần Playwright + Chromium):
python3 -m pip install --break-system-packages playwright gTTS
python3 -m playwright install --with-deps chromium
python3 tests/runtime.py           # exit 0 = đạt; in <n>/<n> passed

# Sinh lại audio đọc lời kể (sau khi đổi tên/fun fact):
python3 tools/gen-narration.py     # ghi assets/narration/<lang>/<id>.mp3
```

### Mẹo verify bằng screenshot (headless) — không cần mắt người cho phần DOM:
Dùng Playwright chụp `page.screenshot(...)` với cờ `--use-angle=swiftshader --enable-unsafe-swiftshader` để WebGL chạy phần mềm. **Hạn chế:** headless KHÔNG có giọng TTS và KHÔNG nghe được audio → phần âm thanh chỉ verify được "không crash" + "file phục vụ 200"; chất lượng nghe phải thử trên máy thật.

---

## 7. Lưu ý / gotchas
- Three.js bản **r128** (cũ) — nhiều API mới không có; giữ nguyên để khỏi vỡ.
- `byId` chứa cả mặt trăng (đừng bỏ — từng gây crash quiz khi thiếu).
- CSS overlay dùng chung class `.quiz-card`; nút trong card style bằng `.quiz-card > button` (child selector) để không đè style chip.
- Khi thêm `getElementById('x')` nhớ có `id="x"` trong HTML (test kiểm tra điều này).
- Network trong môi trường dev có thể bị chặn lúc đầu phiên rồi mở sau — thử lại trước khi kết luận.
