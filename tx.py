from fastapi import FastAPI, HTTPException
import hashlib

app = FastAPI()

# 1. ĐỊNH NGHĨA SẴN BỘ CẦU THEO Ý BẠN (Kết quả không còn random nữa)
# Bạn có thể tự sửa chuỗi này theo ý muốn. T: Tài, X: Xỉu
# Ví dụ dưới đây là: Bệt Tài, xong đến 1-1, xong đến bệt Xỉu...
DANH_SACH_CAU = ["T", "T", "T", "X", "T", "X", "T", "X", "X", "X", "X"]

# Biến dùng để đếm số phiên đã chạy (Lưu trong bộ nhớ)
id_phien_hien_tai = 0

@app.get("/")
def home():
    return {
        "status": "online",
        "game": "Tai Xiu MD5 Co Quy Luat (Khong Random)",
        "author": "trungkhoa"
    }

@app.get("/api/tailoc")
def play_tai_xiu():
    global id_phien_hien_tai
    
    # Tính toán vị trí dựa trên tổng số cầu (hết bộ cầu sẽ tự động quay lại từ đầu)
    vi_tri = id_phien_hien_tai % len(DANH_SACH_CAU)
    loai_ket_qua = DANH_SACH_CAU[vi_tri]
    
    # 2. Tính toán điểm Xúc Xắc cẩn thận tương ứng với kết quả
    if loai_ket_qua == "T":
        ket_qua = "Tai"
        # Định sẵn bộ nút cho Tài (ví dụ: 4-5-6 = 15 điểm)
        xuc_xac = [4, 5, 6]
        tong_diem = 15
    else:
        ket_qua = "Xiu"
        # Định sẵn bộ nút cho Xỉu (ví dụ: 1-2-3 = 6 điểm)
        xuc_xac = [1, 2, 3]
        tong_diem = 6
        
    # 3. Tạo chuỗi bí mật MD5 dựa trên ID phiên để người chơi check
    chuoi_bi_mat = f"Phien_{id_phien_hien_tai}|{ket_qua}|{xuc_xac[0]}-{xuc_xac[1]}-{xuc_xac[2]}|trungkhoa_secret"
    ma_md5 = hashlib.md5(chuoi_bi_mat.encode('utf-8')).hexdigest()
    
    # Lưu lại thông tin phiên này để trả về
    data_tra_ve = {
        "status": "success",
        "by": "trungkhoa",
        "phien": id_phien_hien_tai,
        "ma_md5": ma_md5,
        "xuc_xac": f"{xuc_xac[0]}, {xuc_xac[1]}, {xuc_xac[2]}",
        "tong_diem": tong_diem,
        "ket_qua": ket_qua,
        "phien_goc_de_check": chuoi_bi_mat
    }
    
    # Tăng ID phiên lên 1 cho lượt gọi API tiếp theo
    id_phien_hien_tai += 1
    
    return data_tra_ve
