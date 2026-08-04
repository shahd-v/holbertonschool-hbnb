from app.models.user import User
try:
    u = User('John', 'Doe', 'not-an-email', 'password')
    print("Success: No error raised")
except Exception as e:
    print(f"Caught expected exception: {type(e).__name__}: {e}")
