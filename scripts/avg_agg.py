import sys

def average_over_500(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            # Đọc dữ liệu, tách các giá trị (cách nhau bởi khoảng trắng hoặc xuống dòng)
            data = f.read().split()
            
            # Chuyển thành số và lọc giá trị > 500
            numbers = []
            for x in data:
                try:
                    num = float(x)
                    numbers.append(num)
                except ValueError:
                    continue  # bỏ qua giá trị không phải số
            
            # Kiểm tra danh sách rỗng
            if not numbers:
                print("Không có giá trị nào lớn hơn 500.")
                return
            
            avg = sum(numbers) / len(numbers)
            print(f"{avg:.2f}")
    except FileNotFoundError:
        print(f"Không tìm thấy file: {filename}")
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")


if __name__ == "__main__":
    # Kiểm tra số lượng đối số dòng lệnh
    if len(sys.argv) < 2:
        print("Cách dùng: python average.py <tên_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    average_over_500(input_file)
