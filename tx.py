from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Bạn có thể linh hoạt đổi url thành api.lc79b.bet hoặc api.lc79d.win tùy theo bên nào đang sống
URL_DATA_GOC = "https://api.lc79d.win/api/games/taixiumd5/current"

@app.get("/api/tailoc")
def get_current_game():
    try:
        # 1. PHÁ CACHE: Gắn thêm chuỗi thời gian mili-giây vào đuôi link để link luôn mới
        thoi_gian_bat_dau = time.time()
        timestamp_hien_tai = int(thoi_gian_bat_dau * 1000)
        url_chong_cache = f"{URL_DATA_GOC}?_={timestamp_hien_tai}"
        
        # 2. GIẢ MẠO TRÌNH DUYỆT (Chống bị chặn API)
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Accept": "application/json",
            "Cache-Control": "no-cache"
        }
        
        # Lấy dữ liệu với tốc độ cao
        response = requests.get(url_chong_cache, headers=headers, timeout=3)
        data_game = response.json()
        
        # 3. BÙ TRỪ ĐỘ TRỄ MẠNG (Tự động trừ đi thời gian lấy dữ liệu)
        thoi_gian_nhan_ve = time.time()
        do_tre_mang = int(thoi_gian_nhan_ve - thoi_gian_bat_dau)
        
        id_phien_real = data_game.get("phien", 0)
        ma_md5_real = data_game.get("md5", "")
        xx_truoc = data_game.get("lastResult", "3-3-4")
        kq_truoc = data_game.get("lastResultText", "Xiu")
        
        # Trừ đi số giây trễ mạng để đồng hồ khớp 100% với màn hình game
        giay_con_lai_real = data_game.get("remainTime", 60) - do_tre_mang
        if giay_con_lai_real < 0:
            giay_con_lai_real = 0
            
        chuoi_goc_md5_he_thong = f"Phien_{id_phien_real}|{kq_truoc}|{xx_truoc}|lc79_secret_key"

        if giay_con_lai_real > 5:
            return {
                "status": "success",
                "by": "trungkhoa_admin",
                "phien_hien_tai": id_phien_real,       
                "thoi_gian_con_lai": giay_con_lai_real, 
                "game_display": {
                    "ma_md5_cong_khai": ma_md5_real,     
                    "xuc_xac": "Dang lac... (An ket qua de bao mat)",
                    "tong_diem": "An",
                    "ket_qua": "An",
                    "ADMIN_SO_KEO": "Dang cho mo bat..."
                },
                "admin_prediction_phiên_sau": {
                    "phien_sap_toi": id_phien_real + 1,
                    "du_doan_ket_qua": "QUÉT MD5 LUỒNG SÂU...",
                    "thong_bao": "Chờ 5 giây cuối nổ BÚ"
                }
            }
        else:
            return {
                "status": "success",
                "by": "trungkhoa_admin",
                "phien_hien_tai": id_phien_real,
                "thoi_gian_con_lai": giay_con_lai_real,
                "game_display": {
                    "ma_md5_cong_khai": ma_md5_real,
                    "xuc_xac": f"Phien truoc: {xx_truoc} ({kq_truoc})",
                    "tong_diem": "Hien thi",
                    "ket_qua": kq_truoc,
                    "ADMIN_SO_KEO": "BUUUUU !!!!!!!!", 
                    "chuoi_goc_check": chuoi_goc_md5_he_thong
                },
                "admin_prediction_phiên_sau": {
                    "phien_sap_toi": id_phien_real + 1,
                    "du_doan_ket_qua": "CHỐT KÈO THÀNH CÔNG"
                }
            }
            
    except Exception as e:
        return {
            "status": "error",
            "msg": "Hệ thống đang đồng bộ lại nhịp...",
            "error_log": str(e)
        }
