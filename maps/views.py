from django.shortcuts import render,redirect
from django.views import generic
from accounts.models import CustomUser,MO6_Visit_record
from .models import MO3_Default_spot,MO4_Original_spot,MO5_Tag
from .forms import *
from blog.models import MO7_Blog
import json
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def Map(request):
    user = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    o_spotform = OspotCreateForm()
    searchform = SpotSearchForm()
    tag_list = MO5_Tag.objects.all()
    d_spot = MO3_Default_spot.objects.all()
    o_spot = MO4_Original_spot.objects.filter(MO1_userNumber = request.user.MO1_userNumber)
    d_list = []
    o_list = []
    for i in d_spot:
        d_list.append([i.MO2_storeNumber.MO2_address,i.MO2_storeNumber.MO2_storeName,i.MO3_DspotNumber])
    for i in o_spot:
        o_list.append([i.MO4_OspotAdress,i.MO4_OspotName, i.MO4_OspotNumber])
    params = {
        'd_list': json.dumps(d_list),
        'o_list': json.dumps(o_list),
        'o_form':o_spotform,
        's_form':searchform,
        'tag_list':tag_list,
        'user':user,
    }
    return render(request,"Map.html",params)


class MapView(generic.TemplateView):
    template_name= "Map.html"

class OspotInfoView(generic.TemplateView):
    template_name= "OspotInfo.html"

def OspotInfo(request,spot_num):
    mydata = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    spot = MO4_Original_spot.objects.get(MO4_OspotNumber = spot_num)
    if MO6_Visit_record.objects.filter(MO4_OspotNumber=spot.MO4_OspotNumber).exists():
        records = MO6_Visit_record.objects.filter(MO4_OspotNumber=spot)
    else:
        records = ""
    blogs = MO7_Blog.objects.filter(MO6_visitRecordNumber__in=records)
    params = {
        "spot":spot,
        "count":1,
        "records":records,
        "blogs":blogs,
    }
    return render(request,"OspotInfo.html",params)

class OspotVisitRegisterView(generic.TemplateView):
    template_name = "OspotVisitRegister.html"

@login_required
def DspotInfo(request,spot_num):
    mydata = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    spot = MO3_Default_spot.objects.get(MO3_DspotNumber=spot_num)
    print("s = ",spot)
    records = MO6_Visit_record.objects.filter(MO3_DspotNumber=spot)
    myrecords = MO6_Visit_record.objects.filter(MO3_DspotNumber=spot,MO1_userNumber=mydata)
    blogs = MO7_Blog.objects.filter(MO6_visitRecordNumber__in=records,MO7_openRange=0)
    for i in records:
        print("r = ",i)
    for i in blogs:
        print("b = ",i)
    params = {
        "spot":spot,
        "count":len(myrecords),
        "myrecords":myrecords,
        "blogs":blogs,
    }
    return render(request,"DspotInfo.html",params)


class OtherMapView(generic.TemplateView):
    template_name: str = "OtherMap.html"

def OtherMap(request,num):
    mydata = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    page_user = CustomUser.objects.get(MO1_userNumber=num)
    searchform = SpotSearchForm()
    tag_list = MO5_Tag.objects.all()
    d_spot = MO3_Default_spot.objects.all()
    o_spot = MO4_Original_spot.objects.filter(MO1_userNumber = num)
    d_list = []
    o_list = []
    for i in d_spot:
        d_list.append([i.MO2_storeNumber.MO2_address,i.MO2_storeNumber.MO2_storeName,i.MO3_DspotNumber])
    for i in o_spot:
        o_list.append([i.MO4_OspotAdress,i.MO4_OspotName, i.MO4_OspotNumber])
    params = {
        'd_list': json.dumps(d_list),
        'o_list': json.dumps(o_list),
        's_form':searchform,
        'tag_list':tag_list,
        'user':mydata,
        'page_user':page_user,
    }
    return render(request,"Map.html",params)

@login_required
def OspotCreate(request):
    if request.method == 'POST':
        initial_data = {
            "MO1_userNumber":request.POST.get("MO1_userNumber"),
            "MO4_OspotName":request.POST.get("MO4_OspotName"),
            "MO4_OspotAdress":request.POST.get("MO4_OspotAdress"),
            "MO4_OspotInfo":request.POST.get("MO4_OspotInfo")
        }
        form = OspotCreateForm(request.POST or initial_data)
        if form.is_valid():
            form.save()
            return redirect("maps:Map")
    return redirect("maps:Map")

@login_required
def SpotSearch(request):
    if request.method == 'POST':
        tags_id = request.POST.getlist('tags')
        keword = request.POST.get('keyword')
    for i in tags_id:
        print("tag=",i)
    print("keyword=",keword)
    return Map(request)

def SpotSearch(request):
    from django.db import connection
    cursor = connection.cursor()
    if request.method == 'POST':
        tags_id = request.POST.getlist('tags')
        keword = request.POST.get('keyword')
        tag_counter = len(tags_id)
        if keword == "":
            sql = """select count(*), "MO2_storeNumber" from maps_mo3_default_spot inner join store_mo2_store on ( store_mo2_store."MO2_storeNumber" = "maps_mo3_default_spot"."MO2_storeNumber_id" ) inner join "maps_mo3_default_spot_MO5_tagNumber" on 
            ( "maps_mo3_default_spot"."MO3_DspotNumber" = "maps_mo3_default_spot_MO5_tagNumber"."mo3_default_spot_id" ) where 1=1 """
        else:
            sql = """select count(*), "MO2_storeNumber" from maps_mo3_default_spot inner join store_mo2_store on ( store_mo2_store."MO2_storeNumber" = "maps_mo3_default_spot"."MO2_storeNumber_id" ) inner join "maps_mo3_default_spot_MO5_tagNumber" on 
            ( "maps_mo3_default_spot"."MO3_DspotNumber" = "maps_mo3_default_spot_MO5_tagNumber"."mo3_default_spot_id" ) where "MO2_storeName" LIKE '%大原%' """
        if tag_counter != 0:
            sql += """ and (1=0 """
            for i in tags_id:
                sql += """ or "mo5_tag_id" = """+i
            sql += """)"""
        sql += """ group by "MO2_storeNumber";"""
        print("sql1="+sql)
        
        # ここでエラー
        res = cursor.execute(sql)
        print(res)
        sql = """select * from store_mo2_store where 1=0 """
        for i in res:
            if i["count"] == tag_counter:
                sql += """ or "MO2_storeNumber" = """+i["MO2_storeNumber"]
        sql += """ group by "MO2_storeNumber"; """
        print("sql2="+sql)
        serch = cursor.execute(sql)
        print(serch)
    return Map(request)