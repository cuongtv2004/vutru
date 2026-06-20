# 🪐 Hệ Mặt Trời 3D — phiên bản cho các bé học tập

Mô phỏng hệ mặt trời 3D tương tác, chạy thẳng trên trình duyệt. Dựa trên ý tưởng từ
[locphamnguyen/solar-system-3d](https://github.com/locphamnguyen/solar-system-3d), được làm lại để:

- **Chạy offline 100%** — phù hợp lớp học, máy tính trường, máy tính bảng không có mạng.
- **Một file duy nhất, song ngữ** — tiếng Việt (mặc định) + English, đổi bằng nút `EN/VI`, không còn 2 file trùng lặp.
- **Mượt hơn trên máy yếu** — vành đai tiểu hành tinh dùng `InstancedMesh` (4 draw call thay vì 260).
- **Thân thiện hơn** — màn hình tải, fallback khi máy không hỗ trợ WebGL, danh sách thiên thể bấm được bằng bàn phím.

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

## 📁 Cấu trúc

```
solar-system/
├── index.html              # toàn bộ app (data + i18n + Three.js logic)
├── download-assets.sh      # tải Three.js + texture về local
└── assets/
    ├── audio.mp3           # nhạc nền (đã có sẵn)
    ├── vendor/three.min.js # tải bởi script
    └── textures/*.jpg      # tải bởi script
```

## 🗺️ Lộ trình tiếp theo (cho mục tiêu giáo dục)

- [x] **Phase 1** — Chế độ "Khám phá có hướng dẫn" (camera tự bay + lời kể), fun facts đơn giản cho trẻ.
- [x] **Phase 2** — Quiz học mà chơi ("Hành tinh nào nóng nhất?" → bấm chọn), hiệu ứng thưởng (confetti + âm thanh).
- [ ] **Phase 3** — Toggle "Kích thước thật vs Dễ nhìn" để dạy về tỉ lệ vũ trụ.

## 📜 Giấy phép & nguồn

- Ý tưởng & texture gốc: [KyleGough/solar-system](https://github.com/KyleGough/solar-system), [locphamnguyen/solar-system-3d](https://github.com/locphamnguyen/solar-system-3d).
