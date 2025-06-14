# error_handler.py
# from exceptions import InvalidUserIDError, UserNotFoundError, DatabaseConnectionError
import sys

def format_http_response(status_code: int, message: str) -> dict:
    """پاسخ را به یک فرمت استاندارد JSON تبدیل می‌کند."""
    return {"status": status_code, "error_message": message}

# === دیکشنری نگاشت خطا ===
EXCEPTION_TO_HTTP_MAP = {
    InvalidUserIDError: format_http_response(400, "Bad Request: شناسه کاربر نامعتبر است."),
    UserNotFoundError: format_http_response(404, "Not Found: کاربر مورد نظر یافت نشد."),
    DatabaseConnectionError: format_http_response(503, "Service Unavailable: سرویس دیتابیس در دسترس نیست."),
}

def central_error_handler(exc: Exception) -> dict:
    """
    مدیر مرکزی خطاها.
    یک استثناء (exception) دریافت کرده و آن را به یک پاسخ HTTP استاندارد نگاشت می‌کند.
    """
    # ابتدا در دیکشنری نگاشت جستجو کن
    response = EXCEPTION_TO_HTTP_MAP.get(type(exc))

    if response:
        # اگر خطای شناخته‌شده بود، پاسخ نگاشت‌شده را برگردان
        print(f"--- خطای شناخته‌شده مدیریت شد: {type(exc).__name__} ---", file=sys.stderr)
        return response
    else:
        # اگر خطا ناشناخته بود، یک پاسخ عمومی 500 برگردان
        print(f"--- خطای پیش‌بینی نشده مدیریت شد: {exc} ---", file=sys.stderr)
        return format_http_response(500, "Internal Server Error: یک خطای داخلی رخ داده است.")



# main_api.py
# from user_service import find_user_by_id
# from error_handler import central_error_handler

def get_user_endpoint(user_id_input: str):
    """
    این تابع نقش اندپوینت API ما را بازی می‌کند.
    منطق برنامه بسیار تمیز و متمرکز بر روی حالت موفقیت است.
    """
    print(f"\n>>>>> درخواست برای کاربر با شناسه: '{user_id_input}'")
    try:
        # 1. اجرای منطق اصلی
        user_data = find_user_by_id(user_id_input)
        
        # 2. در صورت موفقیت، پاسخ 200 OK برگردان
        response = {"status": 200, "data": user_data}

    except Exception as e:
        # 3. در صورت بروز هر نوع خطایی، آن را به مدیر مرکزی بسپار
        response = central_error_handler(e)

    # پاسخ نهایی را چاپ کن
    print(f"<<<<< پاسخ نهایی: {response}")
    return response

# --- اجرای سناریوهای مختلف ---
if __name__ == "__main__":
    # ۱. حالت موفقیت‌آمیز
    get_user_endpoint("2")

    # ۲. شناسه نامعتبر (حروف) -> باید خطای 400 بدهد
    get_user_endpoint("abc")

    # ۳. کاربر پیدا نشد -> باید خطای 404 بدهد
    get_user_endpoint("99")
    
    # ۴. خطای اتصال به دیتابیس -> باید خطای 503 بدهد
    get_user_endpoint("5")

    # ۵. یک خطای پیش‌بینی نشده (برای تست مدیر مرکزی)
    try:
        result = 1 / 0
    except Exception as e:
        final_response = central_error_handler(e)
        print(f"\n>>>>> تست خطای پیش‌بینی نشده")
        print(f"<<<<< پاسخ نهایی: {final_response}")