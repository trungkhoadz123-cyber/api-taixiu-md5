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
