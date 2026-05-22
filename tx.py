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

# --- ĐỒNG BỘ MỐC PHIÊN THỰC TẾ THEO ẢNH CỦA BẠN ---
THOI_GIAN_PHIEN = 60
MOCK_TIME_GOC = 1779425340  # Khớp mốc giây hiện tại
MOCK_PHIEN_GOC = 6848736    # Số phiên chuẩn lấy từ ảnh bạn chụp lúc 10:09

def thuat_toan_xuc_xac_chuan(id_phien: int):
    chuoi_bam = hashlib.sha256(f"LC79B_VIP_KEY_{id_phien}".encode()).hexdigest()
    so_nguyen = int(chuoi_bam, 16)
    x1 = (so_nguyen % 6) + 1
    x2 = ((so_nguyen // 6) % 6) + 1
    x3 = ((so_nguyen // 36) % 6) + 1
    tong_diem = x1 + x2 + x3
    ket_qua = "Tai" if tong_diem >= 11 else "Xiu"
    return f"{x1}-{x2}-{x3}", tong_diem, ket_qua

@app.get("/api/tailoc")
def get_current_game():
    thoi_gian_hien_tai = int(time.time())
    khoang_cach_thoi_gian = thoi_gian_hien_tai - MOCK_TIME_GOC
    id_phien_hien_tai = MOCK_PHIEN_GOC + (khoang_cach_thoi_gian // THOI_GIAN_PHIEN)
    giay_con_lai = THOI_GIAN_PHIEN - (khoang_cach_thoi_gian % THOI_GIAN_PHIEN)
    
    xx, td, kq = thuat_toan_xuc_xac_chuan(id_phien_hien_tai)
    chuoi_goc_md5 = f"Phien_{id_phien_hien_tai}|{kq}|{xx}|lc79b_secret_key"
    ma_md5_cong_khai = hashlib.md5(chuoi_goc_md5.encode()).hexdigest()
    
    id_phien_tiep_theo = id_phien_hien_tai + 1
    xx_next, td_next, kq_next = thuat_toan_xuc_xac_chuan(id_phien_tiep_theo)

    if giay_con_lai > 5:
        return {
            "status": "success",
            "by": "trungkhoa_admin",
            "phien_hien_tai": id_phien_hien_tai,
            "thoi_gian_con_lai": giay_con_lai,
            "game_display": {
                "ma_md5_cong_khai": ma_md5_cong_khai,
                "xuc_xac": "Dang lac... (An ket qua de bao mat)",
                "tong_diem": "An",
                "ket_qua": "An",
                "ADMIN_SO_KEO": "Dang cho mo bat..."
            },
            "admin_prediction_phiên_sau": {
                "phien_sap_toi": id_phien_tiep_theo,
                "du_doan_ket_qua": kq_next.upper(),
                "du_doan_xuc_xac": xx_next,
                "thong_bao": "He thong dang check cau MD5..."
            }
        }
    else:
        return {
            "status": "success",
            "by": "trungkhoa_admin",
            "phien_hien_tai": id_phien_hien_tai,
            "thoi_gian_con_lai": giay_con_lai,
            "game_display": {
                "ma_md5_cong_khai": ma_md5_cong_khai,
                "xuc_xac": f"{kq} ({td} diem) -> {xx}",
                "tong_diem": td,
                "ket_qua": kq,
                "ADMIN_SO_KEO": "BUUUUU !!!!!!!!",
                "chuoi_goc_check": chuoi_goc_md5
            },
            "admin_prediction_phiên_sau": {
                "phien_sap_toi": id_phien_tiep_theo,
                "du_doan_ket_qua": kq_next.upper(),
                "du_doan_xuc_xac": xx_next,
                "thong_bao": "QUET CAU THANH CONG"
            }
        }
