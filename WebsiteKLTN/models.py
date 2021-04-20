from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from datetime import date, datetime, time

from django_google_maps import fields as map_fields

# Create your models here.


class DoiTac(models.Model):
    MaDoiTac = models.CharField(max_length=60, primary_key=True)
    # KieuDoiTac = models.CharField(max_length=60)
    TenDoiTac = models.CharField(max_length=60)

    class Meta:
        get_latest_by = ['MaDoiTac']

    def __str__(self):
        return self.TenDoiTac


##### Doanh Nghiep ##################################################
class DoanhNghiep(models.Model):
    MaDoanhNghiep = models.CharField(max_length=60, primary_key=True)
    TenDoanhNghiep = models.CharField(max_length=60)
    SoDienThoai = models.CharField(max_length=60, default="NONE")
    Email = models.CharField(max_length=60, default="NONE")
    MoTaDoanhNghiep = models.CharField(max_length=60, default="NONE")
    CoCauDoanhNghiep = models.CharField(max_length=60, default="NONE")
    QuyMoDoanhNghiep = models.CharField(max_length=60, default="NONE")
    NganhNgheKinhDoanh = models.CharField(max_length=60, default="NONE")
    DiaChiTruSoChinh = models.CharField(max_length=120, default="NONE")

    class Meta:
        get_latest_by = ['MaDoanhNghiep']

    def __str__(self):
        return self.TenDoanhNghiep
        

class DoanhNghiepCurrent(models.Model):
    MaDoanhNghiep = models.CharField(max_length=60, primary_key=True)
    TenDoanhNghiep = models.CharField(max_length=60)
    SoDienThoai = models.CharField(max_length=60, default="NONE")
    Email = models.CharField(max_length=60, default="NONE")
    MoTaDoanhNghiep = models.CharField(max_length=60, default="NONE")
    CoCauDoanhNghiep = models.CharField(max_length=60, default="NONE")
    QuyMoDoanhNghiep = models.CharField(max_length=60, default="NONE")
    NganhNgheKinhDoanh = models.CharField(max_length=60, default="NONE")
    DiaChiTruSoChinh = models.CharField(max_length=120, default="NONE")

    def __str__(self):
        return self.TenDoanhNghiep


class DoiTac_DoanhNghiep(models.Model):
    MaDoiTac_DoanhNghiep = models.CharField(max_length=60, primary_key=True)
    MaDoiTac = ForeignKey(DoiTac, on_delete=CASCADE)
    MaDoanhNghiep = ForeignKey(DoanhNghiep, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.MaDoiTac) + " - " + str(self.MaDoanhNghiep)


class TaiKhoanDoanhNghiep(models.Model):
    MaTaiKhoan = models.CharField(max_length=60, primary_key=True)
    MaDoanhNghiep = models.ForeignKey(DoanhNghiep, on_delete=models.CASCADE)
    TenTaiKhoan = models.CharField(max_length=60)
    MatKhau = models.CharField(max_length=60)
    KieuTaiKhoan = models.CharField(max_length=2)

    def __str__(self):
        return str(self.MaDoanhNghiep) + " - " + self.TenTaiKhoan


##### Tu Nhan ##################################################
class TuNhan(models.Model):
    MaTuhan = models.CharField(max_length=60, primary_key=True)
    HoVaTen = models.CharField(max_length=60)
    SoDienThoai = models.CharField(max_length=60, default="NONE")
    Email = models.CharField(max_length=60, default="NONE")
    NgayThangNamSinh = models.DateField
    QueQuan = models.CharField(max_length=120, default="NONE")
    DiaChiThuongTru = models.CharField(max_length=120, default="NONE")
    CMND = models.CharField(max_length=60)

    def __str__(self):
        return self.HoVaTen


class DoiTac_TuNhan(models.Model):
    MaDoiTac_TuNhan = models.CharField(max_length=60, primary_key=True)
    MaDoiTac = ForeignKey(DoiTac, on_delete=CASCADE)
    MaTuNhan = ForeignKey(TuNhan, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.MaDoiTac) + " - " + str(self.MaTuNhan)


##### Chung ##################################################
class Xe(models.Model):
    # MaXe = models.CharField(max_length=60)
    BienSoXe = models.CharField(max_length=60, primary_key=True)
    TinhTrangXe = models.CharField(max_length=60, default="NONE")
    MaChuSoHuu = ForeignKey(DoiTac, on_delete=models.CASCADE)

    def __str__(self):
        return self.BienSoXe


class TaiKhoanDoiTac(models.Model):
    MaTaiKhoan = models.CharField(max_length=60, primary_key=True)
    MaDoiTac = models.ForeignKey(DoiTac, on_delete=models.CASCADE)
    TenTaiKhoan = models.CharField(max_length=60)
    MatKhau = models.CharField(max_length=60)
    KieuTaiKhoan = models.CharField(max_length=2)

    def __str__(self):
        return str(self.MaDoiTac) + " - " + self.TenTaiKhoan


class TaiKhoanAdmin(models.Model):
    MaTaiKhoan = models.CharField(max_length=60, primary_key=True)
    TenTaiKhoan = models.CharField(max_length=60)
    MatKhau = models.CharField(max_length=60)
    KieuTaiKhoan = models.CharField(max_length=2)

    def __str__(self):
        return self.TenTaiKhoan + " [Admin]"


class DonHang(models.Model):
    MaDonHang = models.CharField(max_length=60, primary_key=True)
    IDKhachHang = models.ForeignKey(DoanhNghiep, on_delete=models.CASCADE)
    IDDoiTac = models.CharField(max_length=60, default="NONE")
    LoaiHangHoa = models.CharField(max_length=60, default="NONE")
    TrongTai = models.CharField(max_length=60, default="NONE")
    DiaDiemNhanHang = models.CharField(max_length=300, default="NONE")
    NgayNhanHang = models.DateField(default=date.today, blank=True)
    GioNhanHang = models.TimeField(blank=True)
    DiaDiemGiaoHang = models.CharField(max_length=300, default="NONE")
    NgayGiaoHang = models.DateField(default=date.today, blank=True)
    GioGiaoHang = models.TimeField(blank=True)
    ChuY = models.CharField(max_length=60, default="NONE")
    TrangThai = models.CharField(max_length=60, default="Chưa Giao")
    TrangThaiChiTiet = models.CharField(max_length=60, default="Nhận đơn")

    class Meta:
        get_latest_by = ['MaDonHang']

    def __str__(self):
        return self.MaDonHang + " [" + str(self.IDKhachHang) + "]"


class DonHangMomentary(models.Model):
    MaDonHang = models.CharField(max_length=60, primary_key=True)
    IDKhachHang = models.ForeignKey(DoanhNghiep, on_delete=models.CASCADE)
    IDDoiTac = models.CharField(max_length=60, default="NONE")
    LoaiHangHoa = models.CharField(max_length=60, default="NONE")
    TrongTai = models.CharField(max_length=60, default="NONE")
    DiaDiemNhanHang = models.CharField(max_length=300, default="NONE")
    NgayNhanHang = models.DateField(default=date.today, blank=True)
    GioNhanHang = models.TimeField(blank=True)
    DiaDiemGiaoHang = models.CharField(max_length=300, default="NONE")
    NgayGiaoHang = models.DateField(default=date.today, blank=True)
    GioGiaoHang = models.TimeField(blank=True)
    ChuY = models.CharField(max_length=60, default="NONE")
    TrangThai = models.CharField(max_length=60, default="Chưa Giao")
    TrangThaiChiTiet = models.CharField(max_length=60, default="Nhận đơn")

    class Meta:
        get_latest_by = ['MaDonHang']

    def __str__(self):
        return self.MaDonHang + " [" + str(self.IDKhachHang) + "]"


class DonVanChuyen(models.Model):
    MaDonVanChuyen =  models.CharField(max_length=60, primary_key=True)
    MaDonHang = models.CharField(max_length=60)
    MaDoiTac = models.CharField(max_length=60)

    def __str__(self):
        return self.MaDonVanChuyen + " [" + str(self.MaDonHang) + "]" + "-[" + str(self.MaDoiTac) + "]"


class ThongTinVanChuyen(models.Model):
    MaThongTinVanChuyen =  models.CharField(max_length=60, primary_key=True)
    MaDonHang = models.CharField(max_length=120)
    ThoiGian = models.CharField(max_length=150, default="NONE")
    X = models.FloatField()
    Y = models.FloatField()
    TrangThai = models.CharField(max_length=150, default="NONE")

    def __str__(self):
        return self.MaThongTinVanChuyen + " [" + str(self.MaDonHang) + "]"


class DanhGia(models.Model):
    Rate = models.IntegerField()
    Comment = models.CharField(max_length=450, default="NONE")
    DateTime = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return str(self.Rate) + " - " + str(self.Comment) + " - " + str(self.DateTime)


################### Map
class Rental(models.Model):
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)