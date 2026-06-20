# Changelog

Lịch sử các phần đã làm cho Hệ Mặt Trời 3D (mục tiêu: cho các bé học tập).
Dựa trên ý tưởng từ [locphamnguyen/solar-system-3d](https://github.com/locphamnguyen/solar-system-3d).

## Phase 0 — Nền tảng & cải tiến kỹ thuật
- Gộp 2 file EN/VI thành **1 file** với i18n; nút đổi ngôn ngữ, mặc định tiếng Việt, nhớ lựa chọn (localStorage).
- **Offline-first**: self-host Three.js + texture trong `assets/`, tự fallback CDN; `download-assets.sh` để tải.
- **InstancedMesh** cho vành tiểu hành tinh (4 draw call thay vì 260).
- Loading screen, fallback khi không có WebGL, accessibility (danh sách thiên thể dạng `<button>`), SEO/meta.

## Phase 1 — Khám phá & nội dung cho trẻ
- **Guided tour**: camera tự bay qua 9 thiên thể, thanh điều khiển (trước/tạm dừng/tiếp/thoát).
- **Fun facts** ngôn ngữ đơn giản cho trẻ (VI/EN, 20 thiên thể).
- **Đọc lời kể** bằng Web Speech API (tùy chọn).

## Phase 2 — Quiz "học mà chơi"
- Nút **🎯 Đố vui**: bốc ngẫu nhiên 6 câu từ pool 12 câu (song ngữ).
- Trả lời bằng cách **bấm thiên thể** trong scene 3D hoặc sidebar.
- Đúng: +điểm, confetti, âm thanh (WebAudio); sai: phản hồi nhẹ + bay tới đáp án đúng.
- Màn kết quả chấm sao, nút chơi lại.

## Phase 3 — So sánh kích thước
- Nút **📏 So sánh kích thước**: xếp 8 hành tinh theo **tỉ lệ đường kính thật**.
- Camera tự căn khung, lưu/khôi phục góc nhìn; caption song ngữ giải thích tỉ lệ.
- (Khoảng cách giữ nguyên, không theo tỉ lệ — dải giá trị thật quá lớn để hiển thị cùng lúc.)

## Phase 4 — Quiz nâng cao
- Màn **chọn chủ đề & số câu** trước khi chơi: Tất cả / Hành tinh / Mặt trăng / Kích thước, chọn 6 hoặc 10 câu.
- Mở rộng pool lên **19 câu** (thêm câu về mặt trăng & kích thước), mỗi câu gắn `cat`.
- **Lưu điểm cao** (localStorage): hiện kỷ lục ở màn setup và màn kết quả, báo "🎉 Kỷ lục mới!" khi phá kỷ lục.

## Hạ tầng
- **Test harness** `tests/runtime.py` (Playwright + Chromium headless) + CI GitHub Actions:
  bắt lỗi JS và kiểm thử tour/quiz/so-sánh/i18n trên mỗi PR.

## Sửa lỗi
- Quiz: trả lời SAI câu "vệ tinh của Trái Đất" gây crash vì `byId` không đăng ký
  các mặt trăng → `selectBody(undefined)`. Đã đăng ký mặt trăng vào `byId`.
  (Lỗi do chính test harness mới phát hiện.)
