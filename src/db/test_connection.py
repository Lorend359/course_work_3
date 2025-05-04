from src.db.connection import get_connection

def test_db_connection():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SHOW server_encoding;")
                encoding = cur.fetchone()[0]
                print(f"✅ Кодировка сервера: {encoding}")

    except Exception as e:
        print("❌ Ошибка подключения к базе данных:", e)

if __name__ == "__main__":
    test_db_connection()
