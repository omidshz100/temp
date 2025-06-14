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