from django import db
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.utils import timezone
import datetime
import json
from json import dumps
import pyrebase
# Create your views here.

config = {
    "apiKey": "AIzaSyCz1w7z4RklhcvWlXMq0DOI63C7uT6FdkQ",
    "authDomain": "sharp-technique-304506.firebaseapp.com",
    "databaseURL": "https://sharp-technique-304506-default-rtdb.firebaseio.com/",
    "projectId": "sharp-technique-304506",
    "storageBucket": "sharp-technique-304506.appspot.com",
    "messagingSenderId": "618699052643",
    "appId": "1:618699052643:web:d7b54177c1ba464bad0a56"
}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

def index(request):
    if (request.GET.get('name')):
        return render(request, 'pages/register.html')

    if (request.POST.get('feedback')):
        rating = request.POST.get('rating')
        if (rating == None):
            rating = 0
        comment = request.POST.get('comment')
        if (comment == ""):
            comment = "NONE"
        time = datetime.datetime.now()
        currentDanhGia = DanhGia(Rate=rating, Comment=comment, DateTime=time)
        currentDanhGia.save()

        rateComment = str(request.POST.get('rating')) + " " + str(request.POST.get('comment'))
        
    return render(request, 'pages/index.html')


def login(request):
    displaytaikhoandoanhnghiep = TaiKhoanDoanhNghiep.objects.all()
    displaydoanhnghiep = DoanhNghiep.objects.all()
    displaydncurrent = DoanhNghiepCurrent.objects.first()
    displaydncurrent.TenDoanhNghiep = "NONE"
    displaydncurrent.SoDienThoai = "NONE"
    displaydncurrent.Email = "NONE"
    displaydncurrent.MoTaDoanhNghiep = "NONE"
    displaydncurrent.CoCauDoanhNghiep = "NONE"
    displaydncurrent.QuyMoDoanhNghiep = "NONE"
    displaydncurrent.NganhNgheKinhDoanh = "NONE"
    displaydncurrent.DiaChiTruSoChinh = "NONE"
    displaydncurrent.save()
    if(request.POST.get('username')):
        username = request.POST.get('username')
        password = request.POST.get('password')
        for resulttaikhoandoanhnghiep in displaytaikhoandoanhnghiep:
            if (resulttaikhoandoanhnghiep.TenTaiKhoan == username and resulttaikhoandoanhnghiep.MatKhau == password):
                for resultdn in displaydoanhnghiep:
                    if (resultdn.MaDoanhNghiep == resulttaikhoandoanhnghiep.MaTaiKhoan):
                        displaydncurrent.TenDoanhNghiep = resultdn.TenDoanhNghiep
                        displaydncurrent.SoDienThoai = resultdn.SoDienThoai
                        displaydncurrent.Email = resultdn.Email
                        displaydncurrent.MoTaDoanhNghiep = resultdn.MoTaDoanhNghiep
                        displaydncurrent.CoCauDoanhNghiep = resultdn.CoCauDoanhNghiep
                        displaydncurrent.QuyMoDoanhNghiep = resultdn.QuyMoDoanhNghiep
                        displaydncurrent.NganhNgheKinhDoanh = resultdn.NganhNgheKinhDoanh
                        displaydncurrent.DiaChiTruSoChinh = resultdn.DiaChiTruSoChinh
                        displaydncurrent.save()
                # return redirect('/account/')
                # return HttpResponse(username)
                return render(request, 'pages/account.html')
            # else:
            #     return HttpResponse("Sai")

    return render(request, 'pages/login.html')


def register(request):
    return render(request, 'pages/register.html')

def transport(request):
    displaydncurrent = DoanhNghiepCurrent.objects.first()
    return render(request, 'pages/transport.html', {"doanhnghiep":displaydncurrent})

def test(request):
    displayttvc = ThongTinVanChuyen.objects.all()
    displaydonhang = DonHang.objects.all()
    displaydoitac = DoiTac.objects.all()
    FBThongTinVanChuyen = database.child('Data').child('ThongTinVanChuyen').get().val()

    dh = "DH2"
    for key, value in FBThongTinVanChuyen.items():
        # newTTVC_MTTVC = key
        # newTTVC_DH = value['DH']
        # newTTVC_ThoiGian = value['ThoiGian']
        # newTTVC_X = value['X']
        # newTTVC_Y = value['Y']
        # newTTVC_TrangThai = value['TrangThai']
        newTTVC = ThongTinVanChuyen(key,
                                value['DH'],
                                value['ThoiGian'],
                                20.9984205,
                                105.8170838,
                                value['TrangThai'])
        newTTVC.save()


    return render(request,"pages/test.html", {"dh":dh})


def viewHistory(request):
    displayttvc = ThongTinVanChuyen.objects.all()
    displaydonhang = DonHang.objects.all()
    displaydoitac = DoiTac.objects.all()
    FBThongTinVanChuyen = database.child('Data').child('ThongTinVanChuyen').get().val()

    speed = "500"

    if(request.POST.get('speed')):
        DHHistory = request.POST.get('speed')

    diadiemnhanhang = ""
    diadiemgiaohang = ""
    if(request.POST.get('DH')):
        DHHistory = request.POST.get('DH')
        for resultDH in displaydonhang:
            if (resultDH.MaDonHang == DHHistory):
                diadiemnhanhang = resultDH.DiaDiemNhanHang
                diadiemgiaohang = resultDH.DiaDiemGiaoHang

                return render(request,"pages/viewHistory.html", {"DHHistory":DHHistory, "speed":speed,
                            "diadiemnhanhang":diadiemnhanhang, "diadiemgiaohang":diadiemgiaohang})

    return HttpResponse(DHHistory)


def map(request):
    displayttvc = ThongTinVanChuyen.objects.all()
    displaytaikhoandoanhnghiep = TaiKhoanDoanhNghiep.objects.all()
    displaydonhang = DonHang.objects.all()
    displaycurrentuser = DoanhNghiepCurrent.objects.first()        

    dh = ""
    diadiemnhanhang = ""
    diadiemgiaohang = ""
    hanghoa = ""
    nhanhang = ""
    giaohang = ""
    trangthai = ""

    DonHang.objects.all().delete()
    FBDonHang = database.child('Data').child('DonHang').get().val()
    for key, value in FBDonHang.items():
        newDH = DonHang()
        newDH.MaDonHang = value['IDDonHang']
        for resulttkdn in displaytaikhoandoanhnghiep:
            if (resulttkdn.MaDoanhNghiep.TenDoanhNghiep == value['IDKhachHang']):
                newDH.IDKhachHang = resulttkdn.MaDoanhNghiep
        newDH.IDDoiTac = value['IDDoiTac']
        newDH.LoaiHangHoa = value['LoaiHangHoa']
        newDH.TrongTai = value['TrongTai']
        newDH.DiaDiemNhanHang = value['DiaDiemNhanHang']
        newDH.NgayNhanHang = datetime.datetime.strptime(value['NgayNhanHang'], "%Y-%m-%d").strftime("%Y-%m-%d")
        newDH.GioNhanHang = datetime.datetime.strptime(value['GioNhanHang'], "%H:%M:%S").strftime("%H:%M:%S")
        newDH.DiaDiemGiaoHang = value['DiaDiemGiaoHang']
        newDH.NgayGiaoHang = datetime.datetime.strptime(value['NgayGiaoHang'], "%Y-%m-%d").strftime("%Y-%m-%d")
        newDH.GioGiaoHang = datetime.datetime.strptime(value['GioGiaoHang'], "%H:%M:%S").strftime("%H:%M:%S")
        newDH.ChuY = value['ChuY']
        newDH.TrangThai = value['TrangThai']
        newDH.TrangThaiChiTiet = value['TrangThaiChiTiet']

        hanghoa = newDH.LoaiHangHoa
        nhanhang = newDH.DiaDiemNhanHang
        nhanhangtime = newDH.NgayNhanHang + " " + newDH.GioNhanHang
        giaohang = newDH.DiaDiemGiaoHang
        giaohangtime = newDH.NgayGiaoHang + " " + newDH.GioGiaoHang
        trangthai = newDH.TrangThaiChiTiet

        newDH.save()


    for resultDH in displaydonhang:
        if ((resultDH.IDKhachHang.TenDoanhNghiep == displaycurrentuser.TenDoanhNghiep)
        and (resultDH.TrangThai == "Đang Giao")):
            diadiemnhanhang = resultDH.DiaDiemNhanHang
            diadiemgiaohang = resultDH.DiaDiemGiaoHang
            dh = resultDH.MaDonHang

    strAdd1 = "NONE"
    if(request.GET.get('select')):
        strSelected = request.GET.get('select')
        return HttpResponse(strSelected)

    return render(request, 'pages/map.html', {"strAdd1":strAdd1, "dh":dh,
                "diadiemnhanhang":diadiemnhanhang, "diadiemgiaohang":diadiemgiaohang, 
                "hanghoa":hanghoa, "nhanhang":nhanhang, "nhanhangtime":nhanhangtime,
                "giaohang":giaohang, "giaohangtime":giaohangtime,
                "trangthai":trangthai})


def directionConfirm(request):
    displaydonhang = DonHang.objects.all()
    addDonHang = DonHangMomentary.objects.latest()
    displaytaikhoandoanhnghiep = TaiKhoanDoanhNghiep.objects.all()
    displaydncurrent = DoanhNghiepCurrent.objects.first()

    if (request.POST.get('loaihanghoa')):
        madonhang = "DH" + str(displaydonhang.count()+1)
        loaihanghoa = request.POST.get('loaihanghoa')
        trongtai = request.POST.get('trongtai')
        diadiemnhanhang = request.POST.get('diadiemnhanhang')
        ngaynhanhang = request.POST.get('date1')
        gionhanhang = request.POST.get('time1')
        # thoigiannhanhang = "NONE"
        diadiemgiaohang = request.POST.get('diadiemgiaohang')
        ngaygiaohang = request.POST.get('date2')
        giogiaohang = request.POST.get('time2')
        # thoigiangiaohang = "NONE"
        chuy = request.POST.get('yeucaukhac')
        tkkhachhang = request.POST.get('order')
        # doanhnghiepduocchon = DoanhNghiep()

        addDonHang.MaDonHang = madonhang
        for resulttkdn in displaytaikhoandoanhnghiep:
            if (resulttkdn.MaDoanhNghiep.TenDoanhNghiep == displaydncurrent.TenDoanhNghiep):
                addDonHang.IDKhachHang = resulttkdn.MaDoanhNghiep
        addDonHang.IDDoiTac = "NONE"
        addDonHang.LoaiHangHoa = loaihanghoa
        addDonHang.TrongTai = trongtai
        addDonHang.DiaDiemNhanHang = diadiemnhanhang
        addDonHang.NgayNhanHang = ngaynhanhang
        addDonHang.GioNhanHang = gionhanhang
        addDonHang.DiaDiemGiaoHang = diadiemgiaohang
        addDonHang.NgayGiaoHang = ngaygiaohang
        addDonHang.GioGiaoHang = giogiaohang
        addDonHang.ChuY = chuy
        addDonHang.TrangThai = "Chưa Giao"
        addDonHang.TrangThaiChiTiet = "Nhận đơn"
        addDonHang.save()
        
        displaydonhang = DonHang.objects.all().order_by("MaDonHang")

        messages.success(request, "Lên đơn thành công")

        return render(request, 'pages/direction_confirm.html', {"diadiemnhanhang":diadiemnhanhang, "diadiemgiaohang":diadiemgiaohang,
                "madonhang":madonhang, "loaihanghoa":loaihanghoa, "trongtai":trongtai, 
                "ngaynhanhang":ngaynhanhang, "gionhanhang":gionhanhang, "ngaygiaohang":ngaygiaohang,
                "giogiaohang":giogiaohang, "chuy":chuy, "tkkhachhang":tkkhachhang,
                "donhangadd":addDonHang, "doanhnghiep":displaydncurrent})

    return render(request, 'pages/direction_confirm.html')


def account(request):
    displaytaikhoandoanhnghiep = TaiKhoanDoanhNghiep.objects.all()
    displaydoanhnghiep = DoanhNghiep.objects.all()
    displaydonhang = DonHang.objects.all()
    intSoChuyenHang = 0
    if(request.POST.get('username')):
        username = request.POST.get('username')
        password = request.POST.get('password')
        for resulttaikhoandoanhnghiep in displaytaikhoandoanhnghiep:
            if (resulttaikhoandoanhnghiep.TenTaiKhoan == username and 
                resulttaikhoandoanhnghiep.MatKhau == password):
                # return redirect('/account/')
                for resultdonhang in displaydonhang:
                   if (resultdonhang.IDKhachHang == resulttaikhoandoanhnghiep.MaDoanhNghiep):
                        intSoChuyenHang = intSoChuyenHang + 1
                return render(request, 'pages/account.html', {"doanhnghiep":displaydoanhnghiep,
                        "taikhoan":resulttaikhoandoanhnghiep, "tkduocchon":username, "soChuyenHang":intSoChuyenHang})
    
    if(request.POST.get('back')):
        back = request.POST.get('back')
        for resulttaikhoandoanhnghiep in displaytaikhoandoanhnghiep:
            if (resulttaikhoandoanhnghiep.TenTaiKhoan == back):
                for resultdonhang in displaydonhang:
                    if (resultdonhang.IDKhachHang == resulttaikhoandoanhnghiep.MaDoanhNghiep):
                        intSoChuyenHang = intSoChuyenHang + 1
                return render(request, 'pages/account.html', {"doanhnghiep":displaydoanhnghiep,
                        "taikhoan":resulttaikhoandoanhnghiep, "tkduocchon":back, "soChuyenHang":intSoChuyenHang})

    return render(request, 'pages/account.html')


def history(request):
    displaytaikhoandoanhnghiep = TaiKhoanDoanhNghiep.objects.all()
    displaydoanhnghiep = DoanhNghiep.objects.all()
    displaydonhang = DonHang.objects.all().order_by("MaDonHang")
    displaydncurrent = DoanhNghiepCurrent.objects.first()
    addDonHangMomentary = DonHangMomentary.objects.latest()
    addDonHang = DonHang.objects.latest()
    

    # if (request.POST.get('history')):
    #     username = request.POST.get('history')
    #     for resulttaikhoandoanhnghiep in displaytaikhoandoanhnghiep:
    #         if (resulttaikhoandoanhnghiep.TenTaiKhoan == username):
    #             tkkhachhang = resulttaikhoandoanhnghiep.MaDoanhNghiep
    #             displaydonhang = DonHang.objects.all().order_by("MaDonHang")
    #             return render(request, 'pages/history.html', {"donhang":displaydonhang,
    #                     "doanhnghiepduocchon":tkkhachhang, "tkduocchon":username,
    #                     "doanhnghiep":displaydncurrent})


    if (request.POST.get('history_new')):

        addDonHang.MaDonHang = addDonHangMomentary.MaDonHang
        addDonHang.IDKhachHang = addDonHangMomentary.IDKhachHang
        addDonHang.IDDoiTac = addDonHangMomentary.IDDoiTac
        addDonHang.LoaiHangHoa = addDonHangMomentary.LoaiHangHoa
        addDonHang.TrongTai = addDonHangMomentary.TrongTai
        addDonHang.DiaDiemNhanHang = addDonHangMomentary.DiaDiemNhanHang
        addDonHang.NgayNhanHang = addDonHangMomentary.NgayNhanHang
        addDonHang.GioNhanHang = addDonHangMomentary.GioNhanHang
        addDonHang.DiaDiemGiaoHang = addDonHangMomentary.DiaDiemGiaoHang
        addDonHang.NgayGiaoHang = addDonHangMomentary.NgayGiaoHang
        addDonHang.GioGiaoHang = addDonHangMomentary.GioGiaoHang
        addDonHang.ChuY = addDonHangMomentary.ChuY
        addDonHang.TrangThai = addDonHangMomentary.TrangThai
        addDonHang.save()

        ###############################################
        data = dict()
        data['IDDonHang'] = str(addDonHang.MaDonHang)
        data['IDKhachHang'] = str(addDonHang.IDKhachHang)
        data['IDDoiTac'] = str(addDonHang.IDDoiTac)
        data['LoaiHangHoa'] = str(addDonHang.LoaiHangHoa)
        data['TrongTai'] = str(addDonHang.TrongTai)
        data['DiaDiemNhanHang'] = str(addDonHang.DiaDiemNhanHang)
        data['NgayNhanHang'] = str(addDonHang.NgayNhanHang)
        data['GioNhanHang'] = str(addDonHang.GioNhanHang)
        data['DiaDiemGiaoHang'] = str(addDonHang.DiaDiemGiaoHang)
        data['NgayGiaoHang'] = str(addDonHang.NgayGiaoHang)
        data['GioGiaoHang'] = str(addDonHang.GioGiaoHang)
        data['ChuY'] = str(addDonHang.ChuY)
        data['TrangThai'] = str(addDonHang.TrangThai)
        data['TrangThaiChiTiet'] = str(addDonHang.TrangThaiChiTiet)

        database.child("Data").child("DonHang").child(addDonHang.MaDonHang).set(data)

        username = request.POST.get('history_new')
        for resulttaikhoandoanhnghiep in displaytaikhoandoanhnghiep:
            if (resulttaikhoandoanhnghiep.TenTaiKhoan == username):
                tkkhachhang = resulttaikhoandoanhnghiep.MaDoanhNghiep
                displaydonhang = DonHang.objects.all().order_by("MaDonHang")

                messages.success(request, "Lên đơn thành công")

                return render(request, 'pages/history.html', {"donhang":displaydonhang,
                        "doanhnghiepduocchon":tkkhachhang, "donhangadd":addDonHang, "tkduocchon":username,
                        "doanhnghiep":displaydncurrent})

    # if (request.GET.get('back')):
    #     username = request.GET.get('back')
    #     for resulttaikhoandoanhnghiep in displaytaikhoandoanhnghiep:
    #         if (resulttaikhoandoanhnghiep.TenTaiKhoan == username):
    #             # return redirect('/account/')
    #             return render(request, 'pages/account.html', {"doanhnghiep":displaydoanhnghiep,"taikhoan":resulttaikhoandoanhnghiep, "tkduocchon":username})

    # if (request.GET.get('loaihanghoa')):
    #     displaydonhang = DonHang.objects.all()
    #     madonhang = "DH" + str(displaydonhang.count()+1)
    #     loaihanghoa = request.GET.get('loaihanghoa')
    #     trongtai = request.GET.get('trongtai')
    #     diadiemnhanhang = request.GET.get('diadiemnhanhang')
    #     ngaynhanhang = request.GET.get('date1')
    #     gionhanhang = request.GET.get('time1')
    #     # thoigiannhanhang = "NONE"
    #     diadiemgiaohang = request.GET.get('diadiemgiaohang')
    #     ngaygiaohang = request.GET.get('date2')
    #     giogiaohang = request.GET.get('time2')
    #     # thoigiangiaohang = "NONE"
    #     chuy = request.GET.get('yeucaukhac')
    #     tkkhachhang = request.GET.get('order')
    #     # doanhnghiepduocchon = DoanhNghiep()

    #     for resulttkdn in displaytaikhoandoanhnghiep:
    #         if (resulttkdn.TenTaiKhoan == tkkhachhang):
    #             addDonHang = DonHang(MaDonHang = madonhang,
    #                                 IDKhachHang = resulttkdn.MaDoanhNghiep,
    #                                 LoaiHangHoa = loaihanghoa,
    #                                 TrongTai = trongtai,
    #                                 DiaDiemNhanHang = diadiemnhanhang,
    #                                 # ThoiGianNhanHang = thoigiannhanhang,
    #                                 NgayNhanHang = ngaynhanhang,
    #                                 GioNhanHang = gionhanhang,
    #                                 DiaDiemGiaoHang = diadiemgiaohang,
    #                                 NgayGiaoHang = ngaygiaohang,
    #                                 GioGiaoHang = giogiaohang,
    #                                 # ThoiGianGiaoHang = thoigiangiaohang,
    #                                 ChuY = chuy,
    #                                 TrangThai = "Chưa Giao")
    #             addDonHang.save()
    #             displaydonhang = DonHang.objects.all().order_by("MaDonHang")

    #             tkkhachhang = resulttkdn.MaDoanhNghiep
    #             # thoigiannhanhang = "[" + str(gionhanhang) + "] [" + str(ngaynhanhang) + "]"
    #             # thoigiangiaohang = "[" + str(giogiaohang) + "] [" + str(ngaygiaohang) + "]"

    #             messages.success(request, "Lên đơn thành công")
                
    #             return render(request, 'pages/history.html', {"donhang":displaydonhang, "doanhnghiepduocchon":tkkhachhang, 
    #                     "donhangadd":addDonHang, "tkduocchon":request.GET.get('order'),
    #                     "doanhnghiep":displaydncurrent})

    return render(request, 'pages/history.html', {"doanhnghiep":displaydncurrent, "donhang":displaydonhang,
            "donhangadd":addDonHang})


def profile(request):
    displaytaikhoandoanhnghiep = TaiKhoanDoanhNghiep.objects.all()
    displaydoanhnghiep = DoanhNghiep.objects.all()
    displaydncurrent = DoanhNghiepCurrent.objects.first()
    # displaydncurrent.TenDoanhNghiep = "NONE"
    # displaydncurrent.SoDienThoai = "NONE"
    # displaydncurrent.Email = "NONE"
    # displaydncurrent.MoTaDoanhNghiep = "NONE"
    # displaydncurrent.CoCauDoanhNghiep = "NONE"
    # displaydncurrent.QuyMoDoanhNghiep = "NONE"
    # displaydncurrent.NganhNgheKinhDoanh = "NONE"
    # displaydncurrent.DiaChiTruSoChinh = "NONE"
    # displaydncurrent.save()

    if(request.POST.get('username')):
        username = request.POST.get('username')
        password = request.POST.get('password')
        for resulttaikhoandoanhnghiep in displaytaikhoandoanhnghiep:
            if (resulttaikhoandoanhnghiep.TenTaiKhoan == username and resulttaikhoandoanhnghiep.MatKhau == password):
                for resultdn in displaydoanhnghiep:
                    if (resultdn.MaDoanhNghiep == resulttaikhoandoanhnghiep.MaTaiKhoan):
                        displaydncurrent.TenDoanhNghiep = resultdn.TenDoanhNghiep
                        displaydncurrent.SoDienThoai = resultdn.SoDienThoai
                        displaydncurrent.Email = resultdn.Email
                        displaydncurrent.MoTaDoanhNghiep = resultdn.MoTaDoanhNghiep
                        displaydncurrent.CoCauDoanhNghiep = resultdn.CoCauDoanhNghiep
                        displaydncurrent.QuyMoDoanhNghiep = resultdn.QuyMoDoanhNghiep
                        displaydncurrent.NganhNgheKinhDoanh = resultdn.NganhNgheKinhDoanh
                        displaydncurrent.DiaChiTruSoChinh = resultdn.DiaChiTruSoChinh
                        displaydncurrent.save()

    displaydncurrent = DoanhNghiepCurrent.objects.first()
    
    return render(request, 'pages/profile.html', {"doanhnghiep":displaydncurrent})