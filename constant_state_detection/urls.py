from django.urls import path

from . import views

app_name = "csd_algo" # Constant State Detection

urlpatterns = [
    path("", views.csd_index, name="index"),

    path("csd-model-rel-wnd-h",
         views.csd_model_rel_wnd_h,
         name="csd_model_rel_wnd_h"),

    path("csd-model-abs-wnd-h",
         views.csd_model_abs_wnd_h,
         name="csd_model_abs_wnd_h"),

    path("csd-userdata-abs-wnd-h",
         views.csd_userdata_abs_wnd_h,
         name="csd_userdata_abs_wnd_h"),

    path("csd-userdata-rel-wnd-h",
         views.csd_userdata_rel_wnd_h,
         name="csd_userdata_rel_wnd_h"),

    path("csd-download-csv-example",
         views.csd_download_csv_example,
         name="csd_download_csv_example"),

]