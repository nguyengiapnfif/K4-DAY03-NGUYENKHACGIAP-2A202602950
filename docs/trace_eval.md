# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** [Điền Họ và Tên]  
> **Mã Sinh Viên / Mã Học viên:** 2A202602950  
> **Chủ đề Lựa chọn:** Đề tài Mở — Trợ lý Học vụ Khóa AI20K (tra cứu tiến độ học viên & đặt lịch Mentor 1:1)  

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 4 / 5 | Yêu cầu kiểu "xem Mentor của tôi là ai rồi đặt lịch" buộc Agent chia 2 bước nối tiếp: tra cứu hồ sơ → đặt lịch với Mentor vừa tìm được (TC04). Chưa đạt 5 vì chuỗi suy luận tối đa ~2–3 bước. |
| **2. Tool Interaction** | 5 / 5 | Tiến độ lab, điểm, chuyên cần, Mentor phụ trách là dữ liệu động theo từng học viên, không thể trả lời từ System Prompt; đặt lịch là hành động ghi dữ liệu. Cả hai đều bắt buộc gọi Tool qua MCP Server. |
| **3. Dynamic Decision** | 4 / 5 | Bước sau phụ thuộc Observation bước trước: tham số `mentor_name` của `book_mentor_session` lấy từ kết quả `learner_progress_query` (TC04); nếu nhận `NOT_FOUND` thì Agent dừng và báo lỗi thay vì đặt lịch (TC05). Câu hỏi chung (TC01) thì trả lời trực tiếp, không gọi Tool. |
| **4. Long Horizon Goal** | 3 / 5 | Agent giữ mục tiêu gốc (đặt lịch) xuyên suốt nhiều vòng ReAct trong 1 yêu cầu, nhưng chưa cần duy trì mục tiêu qua nhiều phiên hội thoại hay lập kế hoạch dài hạn. |
| **TỔNG ĐIỂM AGENTIC FIT** | **16 / 20** | *Tổng điểm > 12/20: Bài toán phù hợp triển khai Agentic System.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

**Cấu hình chạy:** `LLM_PROVIDER=gemini`, `LLM_MODEL=gemini-3.8-flash`. Toàn bộ 10/10 sự kiện trong `docs/trace_waterfall.json` có `"llm_source": "gemini:gemini-3.8-flash"` (không có bước nào fallback về Mock).

Trích xuất tiêu biểu — **TC04 (multi_step_reasoning)**: Agent tra cứu Mentor trước, dùng Observation làm tham số cho lần gọi Tool thứ hai, rồi mới trả lời:

```json
[
  {
    "step": 1,
    "action_type": "TOOL_EXECUTION",
    "llm_source": "gemini:gemini-3.8-flash",
    "tool_name": "learner_progress_query",
    "arguments": { "learner_id": "AI20K-K4A-001" },
    "observation": {
      "status": "SUCCESS",
      "learner_id": "AI20K-K4A-001",
      "data": {
        "full_name": "Lê Hoàng Nam",
        "cohort": "K4A (Lớp Sáng)",
        "mentor": "Mentor Trần Minh Khoa"
      }
    },
    "latency_ms": 2045.19
  },
  {
    "step": 2,
    "action_type": "TOOL_EXECUTION",
    "llm_source": "gemini:gemini-3.8-flash",
    "tool_name": "book_mentor_session",
    "arguments": {
      "learner_id": "AI20K-K4A-001",
      "datetime_str": "20:00 16/09/2026",
      "mentor_name": "Mentor Trần Minh Khoa",
      "topic": "Hỏi về ReAct loop"
    },
    "observation": {
      "status": "SUCCESS",
      "booking_id": "MS-AI20K-K4A-001-01",
      "mentor": "Mentor Trần Minh Khoa",
      "datetime": "20:00 16/09/2026"
    },
    "latency_ms": 3626.96
  },
  {
    "step": 3,
    "action_type": "FINAL_ANSWER",
    "llm_source": "gemini:gemini-3.8-flash",
    "output": "Chào bạn Lê Hoàng Nam (AI20K-K4A-001), ... Mentor phụ trách: Mentor Trần Minh Khoa ... Mã lịch hẹn: MS-AI20K-K4A-001-01, 20:00 ngày 16/09/2026, chủ đề: Hỏi về ReAct loop.",
    "latency_ms": 2423.29
  }
]
```

**Kết quả từng Test Case (Gemini API thật):**

| TC | Loại | Chuỗi thực thi | Kết quả |
| :---: | :--- | :--- | :---: |
| TC01 | direct_query | FINAL_ANSWER (không gọi Tool) | ✅ |
| TC02 | single_tool_query | `learner_progress_query` → FINAL_ANSWER | ✅ |
| TC03 | appointment_booking | `book_mentor_session` → FINAL_ANSWER | ✅ |
| TC04 | multi_step_reasoning | `learner_progress_query` → `book_mentor_session` → FINAL_ANSWER | ✅ |
| TC05 | edge_case_handling | `learner_progress_query` (NOT_FOUND) → FINAL_ANSWER lịch sự, không bịa dữ liệu | ✅ |

**Quan sát & ghi chú:**
- TC03: LLM trích `mentor_name` là `"Phạm Thu Hà"` (bỏ tiền tố "Mentor") — lịch vẫn đặt đúng người; có thể siết lại bằng cách validate `mentor_name` với danh sách Mentor trong Tool.
- TC02: `latency_ms` bước 1 = 24.677 ms do Gemini trả `503 UNAVAILABLE` (quá tải), Provider tự chờ 15s rồi retry thành công.
- Free tier `gemini-3.8-flash` giới hạn 5 request/phút → test runner nghỉ 60s giữa các test case (`TEST_CASE_DELAY_SECONDS`) và tự retry khi gặp `429`/`503`.

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 5 lượt (TC02: 1, TC03: 1, TC04: 2, TC05: 1).
- **Kết quả đẩy Repo nộp bài:** [ ] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
