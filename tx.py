from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
import hashlib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

THOI_GIAN_PHIEN = 60  
SECRET_KEY = "trungkhoa_vip_key_2026"  

def thuat_toan_xuc_xac_chuan(id_phien: int):
    chuoi_bam = hashlib.sha256(f"Phien_{id_phien}_{SECRET_KEY}".encode()).hexdigest()
    so_nguyen = int(chuoi_bam, 16)
    
    x1 = (so_nguyen % 6) + 1
    x2 = ((so_nguyen // 6) % 6) + 1
    x3 = ((so_nguyen // 36) % 6) + 1
    
    tong_diem = x1 + x2 + x3
    ket_qua = "TAI" if tong_diem >= 11 else "XIU"
    string_xuc_xac = f"{x1}-{x2}-{x3}"
    
    return string_xuc_xac, tong_diem, ket_qua

@app.get("/api/tailoc")
def get_current_game():
    thoi_gian_hien_tai = int(time.time())
    
    id_phien_hien_tai = thoi_gian_hien_tai // THOI_GIAN_PHIEN
    giay_con_lai = THOI_GIAN_PHIEN - (thoi_gian_hien_tai % THOI_GIAN_PHIEN)
    
    # 1. Lấy kết quả thực tế của phiên hiện tại
    xx, td, kq = thuat_toan_xuc_xac_chuan(id_phien_hien_tai)
    chuoi_goc_md5 = f"Phien_{id_phien_hien_tai}|{kq}|{xx}|{SECRET_KEY}"
    ma_md5_cong_khai = hashlib.md5(chuoi_goc_md5.encode()).hexdigest()
    
    # Giả lập Dự đoán của phiên HIỆN TẠI (đã được tính từ phiên trước)
    # Để kiểm tra xem Admin đoán đúng hay sai cho phiên này
    _, _, kq_du_doan_cho_phien_nay = thuat_toan_xuc_xac_chuan(id_phien_hien_tai) 
    
    # Kiểm tra kèo "BÚ" hay "XIN LỖI"
    # (Vì thuật toán hash là cố định nên thực tế và dự đoán sẽ luôn khớp 100% -> Luôn luôn BÚ)
    if kq == kq_du_doan_cho_phien_nay:
        keo_so_sanh = "BUUUUU !!!!!!!!"
    else:
        keo_so_sanh = "Xin loi ban toi sai..."

    # 2. Thuật toán dự đoán trước cho phiên TIẾP THEO (Để Admin làm video gáy trước)
    id_phien_tiep_theo = id_phien_hien_tai + 1
    xx_next, td_next, kq_next = thuat_toan_xuc_xac_chuan(id_phien_tiep_theo)
    ma_md5_next = hashlib.md5(f"Phien_{id_phien_tiep_theo}|{kq_next}|{xx_next}|{SECRET_KEY}".encode()).hexdigest()

    if giay_con_lai > 5:
        return {
            "status": "success",
            "by": "trungkhoa_admin",
            "phien_hien_tai": id_phien_hien_tai,
            "thoi_gian_con_lai": giay_con_lai,
            "game_display": {
                "ma_md5_cong_khai": ma_md5_cong_khai,
                "xuc_xac": "Dang lac... (An ket qua chong hack)",
                "tong_diem": "An",
                "ket_qua": "An",
                "ADMIN_SO_KEO": "Dang cho het phien de doi chieu..."
            },
            "admin_prediction_phiên_sau": {
                "phien_sap_toi": id_phien_tiep_theo,
                "du_doan_ket_qua": kq_next,
                "du_doan_xuc_xac": xx_next,
                "ma_md5_truoc": ma_md5_next
            }
        }
    else:
        # 5 giây cuối mở bát: Show chữ BÚ hay XIN LỖI thẳng lên màn hình công khai!
        return {
            "status": "success",
            "by": "trungkhoa_admin",
            "phien_hien_tai": id_phien_hien_tai,
            "thoi_gian_con_lai": giay_con_lai,
            "game_display": {
                "ma_md5_cong_khai": ma_md5_cong_khai,
                "xuc_xac": xx,
                "tong_diem": td,
                "ket_qua": kq,
                "ADMIN_SO_KEO": keo_so_sanh,  # Hiện chữ BÚ hoặc XIN LỖI ở đây
                "chuoi_goc_check": chuoi_goc_md5
            },
            "admin_prediction_phiên_sau": {
                "phien_sap_toi": id_phien_tiep_theo,
                "du_doan_ket_qua": kq_next,
                "du_doan_xuc_xac": xx_next,
                "ma_md5_truoc": ma_md5_next
            }
        }

@app.get("/api/lichsu")
def get_game_history():
    thoi_gian_hien_tai = int(time.time())
    id_phien_hien_tai = thoi_gian_hien_tai // THOI_GIAN_PHIEN
    
    danh_sach_lich_su = []
    for i in range(1, 21):
        id_phien_cu = id_phien_hien_tai - i
        xuc_xac, tong_diem, ket_qua = thuat_toan_xuc_xac_chuan(id_phien_cu)
        chuoi_goc_cu = f"Phien_{id_phien_cu}|{ket_qua}|{xuc_xac}|{SECRET_KEY}"
        ma_md5_cu = hashlib.md5(chuoi_goc_cu.encode()).hexdigest()
        
        danh_sach_lich_su.append({
            "phien": id_phien_cu,
            "xuc_xac": xuc_xac,
            "tong_diem": tong_diem,
            "ket_qua": ket_qua,
            "ma_md5": ma_md5_cu,
            "ket_qua_so_voi_tool_du_doan": "BUUUUU !!!!!!!", # Lịch sử lưu lại toàn bộ các phiên ăn đậm
            "chuoi_goc_de_check": chuoi_goc_cu
        })
        
    return {
        "status": "success",
        "lich_su_cau": danh_sach_lich_su
    }
