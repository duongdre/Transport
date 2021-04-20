from django.contrib import admin
from .models import *
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields
import json

# Register your models here.
admin.site.register(DoanhNghiep)
admin.site.register(DoiTac_DoanhNghiep)
admin.site.register(TaiKhoanDoanhNghiep)
admin.site.register(TuNhan)
admin.site.register(DoiTac_TuNhan)
admin.site.register(DoiTac)
admin.site.register(Xe)
admin.site.register(TaiKhoanDoiTac)
admin.site.register(TaiKhoanAdmin)
admin.site.register(DonHang)
admin.site.register(DonHangMomentary)
admin.site.register(DanhGia)
admin.site.register(DoanhNghiepCurrent)
admin.site.register(DonVanChuyen)
admin.site.register(ThongTinVanChuyen)

class RentalAdmin(admin.ModelAdmin): formfield_overrides = {
    map_fields.AddressField: { 'widget':
    map_widgets.GoogleMapsAddressWidget(attrs={
      'data-autocomplete-options': json.dumps({ 'types': ['geocode',
      'establishment'], 'componentRestrictions': {
                  'country': 'us'
              }
          })
      })
    },
}