import tkinter as tk
from tkinter import messagebox
import database

class ProductApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng nhập")
        self.conn = None
        self.create_login_window()

    def create_login_window(self):
        # Xóa các widget hiện tại
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Đăng nhập", command=self.login).pack(pady=10)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập cả username và password.")
            return

        self.conn = database.connect_db(username, password)
        if self.conn:
            messagebox.showinfo("Thành công", "Đăng nhập thành công!")
            self.create_main_window()
        else:
            messagebox.showerror("Thất bại", "Đăng nhập thất bại. Vui lòng thử lại.")

    def create_main_window(self):
        # Xóa các widget hiện tại
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Quản lý Sản phẩm")

        # Menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        account_menu = tk.Menu(menubar, tearoff=0)
        account_menu.add_command(label="Đăng xuất", command=self.logout)
        account_menu.add_command(label="Thoát", command=self.root.quit)
        menubar.add_cascade(label="Tài khoản", menu=account_menu)

        # Frame thêm sản phẩm
        add_frame = tk.LabelFrame(self.root, text="Thêm Sản phẩm", padx=10, pady=10)
        add_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(add_frame, text="Tên sản phẩm:").grid(row=0, column=0, sticky="e", pady=2)
        self.new_name_entry = tk.Entry(add_frame)
        self.new_name_entry.grid(row=0, column=1, pady=2, sticky="w")

        tk.Label(add_frame, text="Mô tả sản phẩm:").grid(row=1, column=0, sticky="e", pady=2)
        self.new_description_entry = tk.Entry(add_frame)
        self.new_description_entry.grid(row=1, column=1, pady=2, sticky="w")

        tk.Label(add_frame, text="Giá sản phẩm:").grid(row=2, column=0, sticky="e", pady=2)
        self.new_price_entry = tk.Entry(add_frame)
        self.new_price_entry.grid(row=2, column=1, pady=2, sticky="w")

        tk.Button(add_frame, text="Thêm sản phẩm", command=self.add_product).grid(row=3, column=0, columnspan=2, pady=5)

        # Frame hiển thị sản phẩm
        view_frame = tk.LabelFrame(self.root, text="Danh sách Sản phẩm", padx=10, pady=10)
        view_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.result_text = tk.Text(view_frame, height=10, width=70)
        self.result_text.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(view_frame, command=self.result_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.result_text.config(yscrollcommand=scrollbar.set)

        tk.Button(self.root, text="Xem sản phẩm", command=self.view_products).pack(pady=5)

        # Frame cập nhật sản phẩm
        update_frame = tk.LabelFrame(self.root, text="Cập nhật Sản phẩm", padx=10, pady=10)
        update_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(update_frame, text="ID sản phẩm:").grid(row=0, column=0, sticky="e", pady=2)
        self.update_id_entry = tk.Entry(update_frame)
        self.update_id_entry.grid(row=0, column=1, pady=2, sticky="w")

        tk.Label(update_frame, text="Tên mới:").grid(row=1, column=0, sticky="e", pady=2)
        self.update_name_entry = tk.Entry(update_frame)
        self.update_name_entry.grid(row=1, column=1, pady=2, sticky="w")

        tk.Label(update_frame, text="Mô tả mới:").grid(row=2, column=0, sticky="e", pady=2)
        self.update_description_entry = tk.Entry(update_frame)
        self.update_description_entry.grid(row=2, column=1, pady=2, sticky="w")

        tk.Label(update_frame, text="Giá mới:").grid(row=3, column=0, sticky="e", pady=2)
        self.update_price_entry = tk.Entry(update_frame)
        self.update_price_entry.grid(row=3, column=1, pady=2, sticky="w")

        tk.Button(update_frame, text="Cập nhật sản phẩm", command=self.update_product).grid(row=4, column=0, columnspan=2, pady=5)

        # Frame xóa sản phẩm
        delete_frame = tk.LabelFrame(self.root, text="Xóa Sản phẩm", padx=10, pady=10)
        delete_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(delete_frame, text="ID sản phẩm:").grid(row=0, column=0, sticky="e", pady=2)
        self.delete_id_entry = tk.Entry(delete_frame)
        self.delete_id_entry.grid(row=0, column=1, pady=2, sticky="w")

        tk.Button(delete_frame, text="Xóa sản phẩm", command=self.delete_product).grid(row=1, column=0, columnspan=2, pady=5)

    def logout(self):
        if self.conn:
            self.conn.close()
            self.conn = None
        messagebox.showinfo("Đăng xuất", "Bạn đã đăng xuất thành công!")
        self.root.title("Đăng nhập")
        self.create_login_window()

    def add_product(self):
        name = self.new_name_entry.get().strip()
        description = self.new_description_entry.get().strip()
        price = self.new_price_entry.get().strip()

        if not name or not price:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đủ tên và giá sản phẩm.")
            return

        try:
            price = float(price)
            if price < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Lỗi", "Giá sản phẩm phải là số dương.")
            return

        try:
            database.add_product(self.conn, name, description, price)
            messagebox.showinfo("Thành công", "Thêm sản phẩm thành công!")
            self.view_products()
            self.new_name_entry.delete(0, tk.END)
            self.new_description_entry.delete(0, tk.END)
            self.new_price_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Thêm sản phẩm thất bại: {e}")

    def view_products(self):
        try:
            products = database.get_all_products(self.conn)
            self.result_text.delete(1.0, tk.END)
            if not products:
                self.result_text.insert(tk.END, "Không có sản phẩm nào.\n")
                return
            for product in products:
                self.result_text.insert(tk.END, f"ID: {product[0]}, Tên: {product[1]}, Mô tả: {product[2]}, Giá: {product[3]}\n")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lấy danh sách sản phẩm thất bại: {e}")

    def update_product(self):
        product_id = self.update_id_entry.get().strip()
        name = self.update_name_entry.get().strip()
        description = self.update_description_entry.get().strip()
        price = self.update_price_entry.get().strip()

        if not product_id or not name or not price:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ ID, tên và giá mới của sản phẩm.")
            return

        try:
            product_id = int(product_id)
            if product_id <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Lỗi", "ID sản phẩm phải là số nguyên dương.")
            return

        try:
            price = float(price)
            if price < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Lỗi", "Giá sản phẩm phải là số dương.")
            return

        try:
            database.update_product(self.conn, product_id, name, description, price)
            messagebox.showinfo("Thành công", "Cập nhật sản phẩm thành công!")
            self.view_products()
            self.update_id_entry.delete(0, tk.END)
            self.update_name_entry.delete(0, tk.END)
            self.update_description_entry.delete(0, tk.END)
            self.update_price_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Cập nhật sản phẩm thất bại: {e}")

    def delete_product(self):
        product_id = self.delete_id_entry.get().strip()

        if not product_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập ID sản phẩm.")
            return

        try:
            product_id = int(product_id)
            if product_id <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Lỗi", "ID sản phẩm phải là số nguyên dương.")
            return

        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa sản phẩm ID {product_id} không?")
        if not confirm:
            return

        try:
            database.delete_product(self.conn, product_id)
            messagebox.showinfo("Thành công", "Xóa sản phẩm thành công!")
            self.view_products()
            self.delete_id_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Xóa sản phẩm thất bại: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductApp(root)
    root.mainloop()
