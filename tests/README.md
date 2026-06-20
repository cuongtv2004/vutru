# Test

## `runtime.py` — smoke test runtime

Chạy trang thật trong Chromium headless, bắt lỗi JS và kiểm tra các tính năng chính
(loading, info panel, **tour**, **quiz**, **so sánh kích thước**, đổi ngôn ngữ).

### Chạy local
```bash
python3 -m pip install --break-system-packages playwright
python3 -m playwright install --with-deps chromium
bash download-assets.sh          # đảm bảo assets/ đầy đủ
python3 tests/runtime.py
```

Thoát mã `0` = đạt, khác `0` = có lỗi. Tự khởi HTTP server nội bộ, không cần bước riêng.

### CI
[`.github/workflows/runtime-test.yml`](../.github/workflows/runtime-test.yml) chạy test này
trên mỗi PR và push vào `main`.
