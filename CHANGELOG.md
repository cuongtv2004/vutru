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

## Phase 5 — Deep-link & chia sẻ
- URL phản ánh trạng thái: `?body=earth&lang=vi&view=compare` (dùng `history.replaceState`, không reload).
- Mở link có sẵn tham số → tự chọn đúng thiên thể, ngôn ngữ, chế độ xem. Giáo viên gửi link tới đúng hành tinh.
- Nút **🔗 chép liên kết** (clipboard) + thông báo cho screen reader.

## Phase 7 — Accessibility
- **Điều khiển bằng bàn phím**: phím mũi tên xoay camera, `+`/`-` phóng to/thu nhỏ, `Esc` thoát tour/quiz/so-sánh.
- Tôn trọng **`prefers-reduced-motion`**: tắt confetti và tự-xoay (camera/hành tinh/vành đai) cho bé dễ say chuyển động.
- **Screen reader**: vùng `aria-live` đọc tên thiên thể, câu hỏi & kết quả quiz; canvas có `role`/`aria-label`.
- `aria-pressed` cho các nút bật/tắt (nhạc, so sánh, chạy/dừng, tạm dừng tour); `aria-current` cho thiên thể đang chọn; viền focus rõ ràng.

## Phase 8 — Khoảng cách thật
- Chế độ **🛰️ Khoảng cách thật**: Mặt Trời + 8 hành tinh xếp theo **đúng tỉ lệ khoảng cách (AU)** trên một trục.
- Nhãn hiện khoảng cách từng hành tinh (vd "Sao Mộc · 5,2 AU"); caption nhấn mạnh Sao Hải Vương xa 30 AU.
- Cho thấy các hành tinh trong dồn sát Mặt Trời còn nhóm ngoài cách rất xa. Loại trừ lẫn nhau với so-sánh/tour/quiz.

## Phase 9 — Polish hình ảnh
- **Hào quang Mặt Trời** nhiều lớp (additive blending) trông rực rỡ hơn.
- **Khí quyển Trái Đất**: viền sáng xanh quanh hành tinh.
- **Lớp sao sáng** thứ hai tạo chiều sâu cho nền vũ trụ.
- **Vòng sáng** đánh dấu thiên thể đang chọn (luôn hướng về camera).

## Âm thanh: nút tắt tiếng + đọc lời kể tiếng Việt chuẩn
- **Nút 🔊/🔇 tắt-bật tiếng (master)**: mặc định **TẮT khi mở** (hết cảnh nhạc tự phát khó chịu), nhớ lựa chọn (localStorage), tắt luôn nhạc nền + hiệu ứng + lời kể.
- **Đọc lời kể bằng file audio tiếng Việt sinh sẵn** (`assets/narration/<lang>/<id>.mp3`) → đọc giọng Việt chuẩn, **không phụ thuộc giọng của thiết bị**, chạy offline. Fallback Web Speech (chọn đúng giọng) nếu thiếu file.
- Bật "Đọc lời kể" → đọc luôn thiên thể đang chọn (không chỉ trong tour).
- *Audio sinh bằng gTTS (Google TTS) một lần rồi đóng gói vào repo.*

## Hạ tầng
- **Test harness** `tests/runtime.py` (Playwright + Chromium headless) + CI GitHub Actions:
  bắt lỗi JS và kiểm thử tour/quiz/so-sánh/i18n trên mỗi PR.

## Sửa lỗi
- Quiz: trả lời SAI câu "vệ tinh của Trái Đất" gây crash vì `byId` không đăng ký
  các mặt trăng → `selectBody(undefined)`. Đã đăng ký mặt trăng vào `byId`.
  (Lỗi do chính test harness mới phát hiện.)
