"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
Đề tài: Trợ lý Học vụ Khóa AI20K (tra cứu tiến độ học viên & đặt lịch Mentor 1:1).
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Tra cứu thông tin (Query Tool)
    {
        "name": "learner_progress_query",
        "description": (
            "Tra cứu hồ sơ và tiến độ học tập của học viên khóa AI20K bằng mã học viên: "
            "lớp (K4A/K4B), số lab đã nộp, điểm trung bình lab, tỷ lệ chuyên cần và Mentor phụ trách."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "learner_id": {
                    "type": "string",
                    "description": "Mã học viên AI20K cần tra cứu (ví dụ: 'AI20K-K4A-001')"
                }
            },
            "required": ["learner_id"]
        }
    },

    # Tool 2: Hành động đặt lịch (Action Tool)
    {
        "name": "book_mentor_session",
        "description": (
            "Đặt lịch buổi hỗ trợ 1:1 giữa học viên khóa AI20K và Mentor. "
            "Nếu người dùng không nêu tên Mentor, hãy dùng learner_progress_query để tìm Mentor phụ trách trước."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "learner_id": {
                    "type": "string",
                    "description": "Mã học viên AI20K cần đặt lịch (ví dụ: 'AI20K-K4A-001')"
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Thời gian hẹn theo định dạng 'HH:MM DD/MM/YYYY' (ví dụ: '20:00 16/09/2026')"
                },
                "mentor_name": {
                    "type": "string",
                    "description": "Tên Mentor phụ trách buổi 1:1 (ví dụ: 'Mentor Trần Minh Khoa')"
                },
                "topic": {
                    "type": "string",
                    "description": "Nội dung cần hỗ trợ trong buổi 1:1 (ví dụ: 'Debug ReAct loop Lab 3')"
                }
            },
            "required": ["learner_id", "datetime_str", "mentor_name"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

# Dữ liệu giả lập (fictional) phục vụ bài Lab
MOCK_DATABASE = {
    "AI20K-K4A-001": {
        "full_name": "Lê Hoàng Nam",
        "cohort": "K4A (Lớp Sáng)",
        "labs_submitted": 2,
        "labs_total": 3,
        "avg_lab_score": 8.5,
        "attendance_rate": "95%",
        "status": "Đang học",
        "mentor": "Mentor Trần Minh Khoa"
    },
    "AI20K-K4B-002": {
        "full_name": "Phạm Ngọc Mai",
        "cohort": "K4B (Lớp Chiều)",
        "labs_submitted": 3,
        "labs_total": 3,
        "avg_lab_score": 9.0,
        "attendance_rate": "100%",
        "status": "Đang học",
        "mentor": "Mentor Phạm Thu Hà"
    }
}


def execute_learner_progress_query(learner_id: str) -> str:
    """Thực thi tra cứu tiến độ học viên theo mã học viên"""
    learner = MOCK_DATABASE.get(learner_id.strip().upper())
    if learner:
        return json.dumps({
            "status": "SUCCESS",
            "learner_id": learner_id,
            "data": learner
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy học viên AI20K có mã '{learner_id}'"
        }, ensure_ascii=False)


def execute_book_mentor_session(learner_id: str, datetime_str: str, mentor_name: str, topic: str = "Hỗ trợ học tập chung") -> str:
    """Thực thi đặt lịch buổi Mentor 1:1"""
    if learner_id.strip().upper() not in MOCK_DATABASE:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không thể đặt lịch: không tìm thấy học viên AI20K có mã '{learner_id}'"
        }, ensure_ascii=False)
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"MS-{learner_id.strip().upper()}-01",
        "learner_id": learner_id,
        "datetime": datetime_str,
        "mentor": mentor_name,
        "topic": topic,
        "message": f"Đặt lịch Mentor 1:1 thành công cho học viên {learner_id} với {mentor_name} vào lúc {datetime_str} (chủ đề: {topic})."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "learner_progress_query": execute_learner_progress_query,
    "book_mentor_session": execute_book_mentor_session
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
