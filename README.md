# 🪐 Hệ Mặt Trời 3D — phiên bản cho các bé học tập

Mô phỏng hệ mặt trời 3D tương tác, chạy thẳng trên trình duyệt. Dựa trên ý tưởng từ
[locphamnguyen/solar-system-3d](https://github.com/locphamnguyen/solar-system-3d), được làm lại để:

- **Chạy offline 100%** — phù hợp lớp học, máy tính trường, máy tính bảng không có mạng.
- **Một file duy nhất, song ngữ** — tiếng Việt (mặc định) + English, đổi bằng nút `EN/VI`, không còn 2 file trùng lặp.
- **Mượt hơn trên máy yếu** — vành đai tiểu hành tinh dùng `InstancedMesh` (4 draw call thay vì 260).
- **Thân thiện hơn** — màn hình tải, fallback khi máy không hỗ trợ WebGL, danh sách thiên thể bấm được bằng bàn phím.

## ✨ Tính năng

**Khám phá vũ trụ**
- 🌌 Hệ mặt trời 3D: Mặt Trời, 8 hành tinh, các mặt trăng chính, vành đai tiểu hành tinh và **5 hành tinh lùn** (Ceres, Sao Diêm Vương + Charon, Haumea, Makemake, Eris).
- 📖 Mỗi thiên thể có mô tả + **fun fact** song ngữ, **đọc lời kể bằng giọng tiếng Việt** (file audio sẵn, không cần mạng).
- 🚀 **Khám phá có hướng dẫn** — camera tự bay qua 14 chặng kèm lời kể.
- 🔍 **Tìm kiếm thiên thể** — lọc nhanh danh sách theo tên, bỏ dấu, khớp cả tiếng Việt lẫn tiếng Anh.

**Học mà chơi**
- 🎯 **Quiz** — chọn chủ đề (hành tinh / mặt trăng / kích thước / hành tinh lùn) và số câu; trả lời bằng cách bấm thiên thể; có confetti, âm thanh và lưu kỷ lục.
- ⏱️ **Quiz tính giờ** — chế độ đếm ngược mỗi câu, kỷ lục riêng.

**Các chế độ trực quan**
- 📏 **So sánh kích thước** — xếp các thiên thể theo tỉ lệ đường kính thật.
- 🛰️ **Khoảng cách thật** — xếp theo đúng tỉ lệ khoảng cách (AU), thấy rõ nhóm ngoài xa thế nào.
- ⚖️ **Cân nặng của em** — nhập cân nặng, xem mình nặng bao nhiêu trên mỗi thiên thể (theo trọng lực bề mặt thật).
- 🌗 **Pha Mặt Trăng & nhật/nguyệt thực** — mô phỏng Mặt Trời–Trái Đất–Mặt Trăng, 8 pha + nhật/nguyệt thực khi thẳng hàng.
- 🌍 **Ngày/đêm & mùa** — Trái Đất nghiêng trục 23,5° quay quanh Mặt Trời, minh hoạ các mùa và ranh giới ngày/đêm.
- ✨ **Chòm sao** — vẽ 6 chòm sao quen thuộc (Lạp Hộ, Bắc Đẩu, Tiên Hậu, Bọ Cạp, Sư Tử, Thiên Nga) với đường nối và tên song ngữ.

**Tiện ích**
- 🌐 Song ngữ Việt/Anh (mặc định tiếng Việt), nhớ lựa chọn.
- 🔇 Nút tắt/bật tiếng (mặc định **tắt**), tắt cả nhạc nền + hiệu ứng + lời kể.
- 🔗 Chia sẻ trạng thái qua liên kết (`?body=&lang=&view=`).
- ♿ Điều khiển bằng bàn phím, tôn trọng `prefers-reduced-motion`, có nhãn aria.

## 🚀 Bắt đầu

```bash
# 1) Tải asset về để chạy offline (chạy 1 lần, CẦN mạng lần này)
bash download-assets.sh

# 2) Mở app — nên chạy qua server tĩnh để tránh chặn CORS khi load texture
python3 -m http.server 8000
```

Rồi mở trình duyệt vào `http://localhost:8000`.

> Không có Python? Vẫn mở trực tiếp `index.html` bằng trình duyệt được — nhưng một số trình duyệt
> chặn texture local qua `file://`; khi đó app tự lấy texture từ CDN (cần mạng). Chạy qua server tĩnh
> là cách offline ổn định nhất. Không cần Node.js/npm.

> Nếu chưa chạy `download-assets.sh`, app vẫn hoạt động khi **có mạng** (tự tải Three.js + texture từ CDN). Sau khi tải về local thì chạy offline hoàn toàn.

## 🎮 Điều khiển

| Thao tác | Hiệu ứng |
|---|---|
| Kéo chuột / 1 ngón | Xoay camera |
| Lăn chuột / chụm 2 ngón | Phóng to / thu nhỏ |
| Bấm thiên thể (3D hoặc danh sách) | Bay tới và bám theo |
| Tab + Enter | Chọn thiên thể bằng bàn phím |
| Phím mũi tên | Xoay camera |
| `+` / `-` | Phóng to / thu nhỏ |
| `Esc` | Thoát chế độ / đóng cửa sổ đang mở |

## 📁 Cấu trúc

```
vutru/
├── index.html              # toàn bộ app (data + i18n + CSS + Three.js logic)
├── download-assets.sh      # tải Three.js + texture về local
├── tools/gen-narration.py  # sinh file audio đọc lời kể (gTTS)
├── tests/runtime.py        # smoke test runtime (Playwright headless)
├── CHANGELOG.md            # nhật ký từng phase
└── assets/
    ├── audio.mp3           # nhạc nền (đã có sẵn)
    ├── vendor/three.min.js # tải bởi script
    ├── textures/*.jpg      # tải bởi script
    └── narration/<vi|en>/  # file audio đọc lời kể (đã commit)
```

## 🗺️ Lộ trình

Toàn bộ lộ trình giáo dục đã hoàn thành — xem chi tiết từng phase trong [CHANGELOG.md](CHANGELOG.md).
Mọi tính năng ở mục [✨ Tính năng](#-tính-năng) đều đã có trong bản hiện tại.

## 📜 Giấy phép & nguồn

- Ý tưởng & texture gốc: [KyleGough/solar-system](https://github.com/KyleGough/solar-system), [locphamnguyen/solar-system-3d](https://github.com/locphamnguyen/solar-system-3d).
