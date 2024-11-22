import tkinter as tk
from tkinter import messagebox

# Tạo cửa sổ ứng dụng
root = tk.Tk()
root.title("Basic Caculator")
root.geometry("400x600")
root.configure(bg="#f0f0f0")

# Biến lưu trữ biểu thức toán học
expression = ""

# Hàm cập nhật biểu thức
def update_expression(value):
    global expression
    expression += str(value)
    equation.set(expression)

# Hàm xóa toàn bộ biểu thức
def clear_all():
    global expression
    expression = ""
    equation.set(expression)

# Hàm xóa ký tự cuối cùng trong biểu thức
def delete_last():
    global expression
    expression = expression[:-1]
    equation.set(expression)

# Hàm tính toán kết quả
def calculate():
    global expression
    try:
        result = eval(expression)  # Tính toán biểu thức
        equation.set(result)
        expression = str(result)   # Lưu kết quả để tiếp tục tính toán
    except Exception:
        messagebox.showerror("Lỗi", "Biểu thức không hợp lệ")
        expression = ""
        equation.set("")

# Giao diện hiển thị biểu thức và kết quả
equation = tk.StringVar()
display = tk.Entry(root, textvariable=equation, font=("Arial", 24), bd=10, insertwidth=2, width=14, borderwidth=4, justify='right')
display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Tạo các nút cho máy tính
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+',
    'C', 'CE'
]

row = 1
col = 0
for button in buttons:
    if button == '=':
        btn = tk.Button(root, text=button, padx=20, pady=20, font=("Arial", 16), bg="#4CAF50", fg="white",
                        command=calculate)
    elif button == 'C':
        btn = tk.Button(root, text=button, padx=20, pady=20, font=("Arial", 16), bg="#f44336", fg="white",
                        command=clear_all)
    elif button == 'CE':
        btn = tk.Button(root, text=button, padx=20, pady=20, font=("Arial", 16), bg="#ff9800", fg="white",
                        command=delete_last)
    else:
        btn = tk.Button(root, text=button, padx=20, pady=20, font=("Arial", 16), bg="#2196F3", fg="white",
                        command=lambda t=button: update_expression(t))

    btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')  # Căn giữa và mở rộng

    col += 1
    if col > 3:  # Đặt lại cột sau khi đạt tới cột cuối cùng
        col = 0
        row += 1

# Sắp xếp nút "C" và "CE" ở dòng cuối cùng
tk.Button(root, text='C', padx=20, pady=20, font=("Arial", 16), bg="#f44336", fg="white",
          command=clear_all).grid(row=row, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')  # "C" chiếm 2 cột
tk.Button(root, text='CE', padx=20, pady=20, font=("Arial", 16), bg="#ff9800", fg="white",
          command=delete_last).grid(row=row, column=2, columnspan=2, padx=5, pady=5, sticky='nsew')  # "CE" chiếm 2 cột

# Cải thiện layout để tự động mở rộng các cột
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

root.mainloop()
