# Changelog

Lịch sử các phần đã làm cho Hệ Mặt Trời 3D (mục tiêu: cho các bé học tập), **mới nhất ở trên**.
Dựa trên ý tưởng từ [locphamnguyen/solar-system-3d](https://github.com/locphamnguyen/solar-system-3d).

> **Về cách đánh số:** mỗi phase tương ứng một nhánh/PR khi phát triển nên số có vài khoảng trống —
> **Phase 6** (PWA) đã **bỏ** vì chỉ cần chạy GitHub Pages; **không có Phase 13**.
> Các mục không đánh số (Âm thanh, Hạ tầng, Sửa lỗi) là cải tiến xen giữa các phase.

## Phase 16 — Tìm kiếm, quiz tính giờ & ngày/đêm-mùa
*(Bỏ "Chế độ giáo viên" P12 vì app dùng cục bộ ở nhà, không dùng trên lớp.)*
- **🔍 Ô tìm kiếm thiên thể**: lọc nhanh danh sách bên sidebar theo tên, **bỏ dấu** và khớp **cả tiếng Việt lẫn tiếng Anh** (vd "sao hoa" → Sao Hỏa). Báo khi không có kết quả.
- **⏱️ Quiz tính giờ**: chip chọn chế độ "Thường / Tính giờ" trong màn cài đặt quiz; mỗi câu đếm ngược 12 giây (hết giờ = sai, hiện đáp án), kỷ lục lưu **riêng** cho chế độ tính giờ.
- **🌍 Ngày/đêm & mùa**: mini-scene riêng — Trái Đất nghiêng trục 23,5° (cố định hướng) quay quanh Mặt Trời; kéo thanh trượt đổi thời điểm trong năm → đổi mùa (Bắc bán cầu, kèm chú thích Nam bán cầu ngược lại); Trái Đất tự quay tạo ranh giới ngày/đêm. Vật lý solstice đã kiểm: cực nghiêng về Mặt Trời = mùa hè.
- Tất cả song ngữ, tôn trọng reduced-motion, deep-link `?view=seasons`. Kiểm thử: +12 checks (65 tổng).

## Phase 15 — Chòm sao
- Nút **✨ Chòm sao**: chế độ vẽ **6 chòm sao quen thuộc** lên nền sao (Lạp Hộ/Orion, Gấu Lớn/Bắc Đẩu, Tiên Hậu/Cassiopeia, Bọ Cạp/Scorpius, Sư Tử/Leo, Thiên Nga/Cygnus).
- Mỗi chòm gồm các **ngôi sao** (sao sáng nổi bật to & vàng hơn) + **đường nối** mô tả hình vẽ + **tên song ngữ**. Bố trí dạng "bản đồ sao" nhìn thẳng, tự canh khung theo tỉ lệ màn hình (hợp cả ngang/dọc).
- Dùng đúng pattern "chế độ" như So sánh/Khoảng cách: ẩn hệ mặt trời, giữ nền sao, loại trừ lẫn nhau với các chế độ khác; thoát bằng nút hoặc Esc; deep-link `?view=constellations`.
- Kiểm thử: +5 checks (53 tổng).

## Phase 14 — Pha Mặt Trăng & Nhật/Nguyệt thực
- Nút **🌗 Pha & Nhật/Nguyệt thực**: mở một **mini-scene riêng** (Three.js, renderer độc lập) mô phỏng Mặt Trời – Trái Đất – Mặt Trăng.
- Kéo **thanh trượt** (hoặc bấm ▶ để tự chạy) để Mặt Trăng đi quanh Trái Đất; phần được Mặt Trời chiếu sáng đổi dần → hiển thị **8 pha** (Trăng non → Trăng tròn → khuyết) kèm emoji 🌑🌒🌓🌔🌕🌖🌗🌘 và tên song ngữ.
- **Nhật thực** khi Trăng non thẳng hàng (bóng Mặt Trăng chấm lên Trái Đất); **nguyệt thực** khi Trăng tròn thẳng hàng (Mặt Trăng nhuốm đỏ đồng). Có lời giải thích vì sao thực không xảy ra mỗi tháng (quỹ đạo nghiêng).
- Trái Đất có ranh giới ngày/đêm thật nhờ ánh sáng định hướng từ Mặt Trời; loại trừ lẫn nhau với tour/quiz/so-sánh/khoảng-cách; tôn trọng `prefers-reduced-motion` (mặc định tạm dừng); thoát bằng ✕ hoặc Esc; có deep-link `?view=phase`.
- Kiểm thử: +5 checks (48 tổng).

## Phase 12 — Tích hợp 5 hành tinh lùn vào mọi chế độ
- **Guided tour**: thêm Ceres, Sao Diêm Vương, Haumea, Makemake, Eris vào cuối hành trình (9 → 14 chặng), đọc lời kể bằng file audio sẵn có.
- **So sánh kích thước (📏)**: thêm 5 hành tinh lùn ở cuối hàng — bé thấy chúng tí xíu so với 8 hành tinh.
- **Khoảng cách thật (🛰️)**: tách danh sách riêng cho chế độ khoảng cách; xếp hành tinh lùn theo đúng AU (Ceres trong vành đai; Sao Diêm Vương → Eris vượt xa Sao Hải Vương, trục kéo dài tới Eris ở 68 AU).
- **Cân nặng của em (⚖️)**: thêm 5 hành tinh lùn (trọng lực bề mặt thật) — đứng đầu danh sách "nhẹ nhất" vì bé gần như không cân nặng gì trên chúng.
- **Đố vui (🎯)**: thêm chủ đề **Hành tinh lùn** (5 câu hỏi song ngữ) + chip chọn chủ đề.
- Cập nhật chú thích chế độ so sánh/khoảng cách; bổ sung kiểm thử (39 → 42 checks).

## Phase 11 — Hành tinh lùn
- Thêm **5 hành tinh lùn**: Ceres (trong vành đai), Sao Diêm Vương (+ mặt trăng Charon), Haumea (hình quả trứng), Makemake, Eris (quỹ đạo ngoài Sao Hải Vương).
- Đầy đủ tên/mô tả/thông số + fun fact song ngữ + **file audio đọc lời kể** tiếng Việt & Anh.
- Bấm chọn được như mọi thiên thể, hỗ trợ deep-link (`?body=pluto`).

## Phase 10 — Cân nặng trên các thiên thể
- Nút **⚖️ Cân nặng của em**: bé nhập cân nặng → xem mình nặng bao nhiêu trên Mặt Trăng, các hành tinh và Mặt Trời (theo trọng lực bề mặt thật).
- Danh sách xếp tăng dần theo trọng lực (nhẹ nhất → nặng nhất), cập nhật trực tiếp khi nhập, song ngữ.

## Âm thanh: nút tắt tiếng + đọc lời kể tiếng Việt chuẩn
- **Nút 🔊/🔇 tắt-bật tiếng (master)**: mặc định **TẮT khi mở** (hết cảnh nhạc tự phát khó chịu), nhớ lựa chọn (localStorage), tắt luôn nhạc nền + hiệu ứng + lời kể.
- **Đọc lời kể bằng file audio tiếng Việt sinh sẵn** (`assets/narration/<lang>/<id>.mp3`) → đọc giọng Việt chuẩn, **không phụ thuộc giọng của thiết bị**, chạy offline. Fallback Web Speech (chọn đúng giọng) nếu thiếu file.
- Bật "Đọc lời kể" → đọc luôn thiên thể đang chọn (không chỉ trong tour).
- *Audio sinh bằng gTTS (Google TTS) một lần rồi đóng gói vào repo.*

## Phase 9 — Polish hình ảnh
- **Hào quang Mặt Trời** nhiều lớp (additive blending) trông rực rỡ hơn.
- **Khí quyển Trái Đất**: viền sáng xanh quanh hành tinh.
- **Lớp sao sáng** thứ hai tạo chiều sâu cho nền vũ trụ.
- **Vòng sáng** đánh dấu thiên thể đang chọn (luôn hướng về camera).

## Phase 8 — Khoảng cách thật
- Chế độ **🛰️ Khoảng cách thật**: Mặt Trời + 8 hành tinh xếp theo **đúng tỉ lệ khoảng cách (AU)** trên một trục.
- Nhãn hiện khoảng cách từng hành tinh (vd "Sao Mộc · 5,2 AU"); caption nhấn mạnh Sao Hải Vương xa 30 AU.
- Cho thấy các hành tinh trong dồn sát Mặt Trời còn nhóm ngoài cách rất xa. Loại trừ lẫn nhau với so-sánh/tour/quiz.

## Phase 7 — Accessibility
- **Điều khiển bằng bàn phím**: phím mũi tên xoay camera, `+`/`-` phóng to/thu nhỏ, `Esc` thoát tour/quiz/so-sánh.
- Tôn trọng **`prefers-reduced-motion`**: tắt confetti và tự-xoay (camera/hành tinh/vành đai) cho bé dễ say chuyển động.
- **Screen reader**: vùng `aria-live` đọc tên thiên thể, câu hỏi & kết quả quiz; canvas có `role`/`aria-label`.
- `aria-pressed` cho các nút bật/tắt (nhạc, so sánh, chạy/dừng, tạm dừng tour); `aria-current` cho thiên thể đang chọn; viền focus rõ ràng.

## Phase 5 — Deep-link & chia sẻ
- URL phản ánh trạng thái: `?body=earth&lang=vi&view=compare` (dùng `history.replaceState`, không reload).
- Mở link có sẵn tham số → tự chọn đúng thiên thể, ngôn ngữ, chế độ xem. Giáo viên gửi link tới đúng hành tinh.
- Nút **🔗 chép liên kết** (clipboard) + thông báo cho screen reader.

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

## Phase 3 — So sánh kích thước
- Nút **📏 So sánh kích thước**: xếp 8 hành tinh theo **tỉ lệ đường kính thật**.
- Camera tự căn khung, lưu/khôi phục góc nhìn; caption song ngữ giải thích tỉ lệ.
- (Khoảng cách giữ nguyên, không theo tỉ lệ — dải giá trị thật quá lớn để hiển thị cùng lúc.)

## Phase 2 — Quiz "học mà chơi"
- Nút **🎯 Đố vui**: bốc ngẫu nhiên 6 câu từ pool 12 câu (song ngữ).
- Trả lời bằng cách **bấm thiên thể** trong scene 3D hoặc sidebar.
- Đúng: +điểm, confetti, âm thanh (WebAudio); sai: phản hồi nhẹ + bay tới đáp án đúng.
- Màn kết quả chấm sao, nút chơi lại.

## Phase 1 — Khám phá & nội dung cho trẻ
- **Guided tour**: camera tự bay qua 9 thiên thể, thanh điều khiển (trước/tạm dừng/tiếp/thoát).
- **Fun facts** ngôn ngữ đơn giản cho trẻ (VI/EN, 20 thiên thể).
- **Đọc lời kể** bằng Web Speech API (tùy chọn).

## Phase 0 — Nền tảng & cải tiến kỹ thuật
- Gộp 2 file EN/VI thành **1 file** với i18n; nút đổi ngôn ngữ, mặc định tiếng Việt, nhớ lựa chọn (localStorage).
- **Offline-first**: self-host Three.js + texture trong `assets/`, tự fallback CDN; `download-assets.sh` để tải.
- **InstancedMesh** cho vành tiểu hành tinh (4 draw call thay vì 260).
- Loading screen, fallback khi không có WebGL, accessibility (danh sách thiên thể dạng `<button>`), SEO/meta.
