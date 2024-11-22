import psycopg2
from psycopg2 import sql

def connect_db(username, password):
    try:
        conn = psycopg2.connect(
            host="localhost",  # Địa chỉ server
            database="product_db",  # Tên database bạn vừa tạo
            user="postgres",  # User PostgreSQL (ví dụ: postgres)
            password="27112002"  # Password PostgreSQL
        )
        return conn
    except psycopg2.Error as e:
        print(f"Kết nối thất bại: {e}")
        return None


# Hàm lấy tất cả sản phẩm
def get_all_products(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM product ORDER BY id ASC")
            products = cur.fetchall()
        return products
    except psycopg2.Error as e:
        print(f"Lỗi khi lấy sản phẩm: {e}")
        raise

# Hàm thêm sản phẩm mới
def add_product(conn, name, description, price):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO product (name, description, price) VALUES (%s, %s, %s)",
                (name, description, price)
            )
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Lỗi khi thêm sản phẩm: {e}")
        raise

# Hàm cập nhật sản phẩm
def update_product(conn, product_id, name, description, price):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE product SET name = %s, description = %s, price = %s WHERE id = %s",
                (name, description, price, product_id)
            )
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Lỗi khi cập nhật sản phẩm: {e}")
        raise

# Hàm xóa sản phẩm
def delete_product(conn, product_id):
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM product WHERE id = %s", (product_id,))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Lỗi khi xóa sản phẩm: {e}")
        raise
