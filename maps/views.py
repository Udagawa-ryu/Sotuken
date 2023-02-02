from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import generic
from accounts.models import CustomUser,MO6_Visit_record
from .models import MO3_Default_spot,MO4_Original_spot,MO5_Tag
from store.models import MO2_store
from .forms import *
from blog.models import MO7_Blog
import json
import datetime
from django.contrib.auth.decorators import login_required
# Create your views here.

def image_url(spot):
    if spot.MO2_storeNumber.MO2_images1 == "":
        url = "/static/images/noimage.jpg"
        return url
    else:
        url = "/media/store_images/"+spot.MO2_storeNumber.MO2_storeName+"/image1.png"
        return url

@login_required
def Map(request):
    user = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    o_spotform = OspotCreateForm()
    searchform = SpotSearchForm()
    tag_list = MO5_Tag.objects.all()
    d_spot = MO3_Default_spot.objects.select_related('MO2_storeNumber')
    o_spot = MO4_Original_spot.objects.filter(MO1_userNumber = request.user.MO1_userNumber)
    d_list = []
    o_list = []
    for i in d_spot:
        image = image_url(i)
        d_list.append([i.MO2_storeNumber.MO2_address,i.MO2_storeNumber.MO2_storeName,i.MO3_DspotNumber,image])
    for i in o_spot:
        url = "/static/images/noimage.jpg"
        address = [i.MO4_OspotLat,i.MO4_OspotLng]
        o_list.append([address,i.MO4_OspotName, i.MO4_OspotNumber,url])
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
    mine = 0
    if spot.MO1_userNumber != mydata:
        mine = 1
    if MO6_Visit_record.objects.filter(MO4_OspotNumber=spot.MO4_OspotNumber).exists():
        records = MO6_Visit_record.objects.filter(MO4_OspotNumber=spot)
    else:
        records = ""
    blogs = MO7_Blog.objects.filter(MO6_visitRecordNumber__in=records,MO7_openRange=0)
    if records == "":
        count=0
    else:
        count = records.count()
    params = {
        "spot":spot,
        "count":count,
        "records":records,
        "blogs":blogs,
        "mine":mine,
    }
    return render(request,"OspotInfo.html",params)

class OspotVisitRegisterView(generic.TemplateView):
    template_name = "OspotVisitRegister.html"
def OspotVisitRegister(request):
    print(request.POST.get("spot"))
    spot = MO4_Original_spot.objects.get(MO4_OspotNumber=request.POST.get("spot"))
    params = {
        "spot":spot,
    }
    return render(request,"OspotVisitRegister.html",params)


def OspotVisitcreate(request):
    user = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    num = int(request.POST.get("spot"))
    o_spot = MO4_Original_spot.objects.get(MO4_OspotNumber=num)
    time = request.POST.get("time")
    date = request.POST.get("date")
    t =time.split(":")
    d =date.split("-")
    visited = datetime.datetime(int(d[0]),int(d[1]),int(d[2]),int(t[0]),int(t[1]),00)
    record = MO6_Visit_record.objects.create(MO1_userNumber=user,MO4_OspotNumber=o_spot,MO6_visitDate=visited)
    return redirect("maps:originalspotinfo",num)


@login_required
def DspotInfo(request,spot_num):
    mydata = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    spot = MO3_Default_spot.objects.get(MO3_DspotNumber=spot_num)
    # store = MO2_store.objects.get(MO2_storeNumber=spot.MO2_storeNumber)
    img_link = []
    img_id = []
    img_count = 0
    if spot.MO2_storeNumber.MO2_images1 != "":
        url = "/media/"+str(spot.MO2_storeNumber.MO2_images1)
        img_link.append(url)
        img_id.append("carousel-1")
        img_count += 1
    if spot.MO2_storeNumber.MO2_images2 != "":
        url = "/media/"+str(spot.MO2_storeNumber.MO2_images2)
        img_link.append(url)
        img_id.append("carousel-2")
        img_count += 1
    if spot.MO2_storeNumber.MO2_images3 != "":
        url = "/media/"+str(spot.MO2_storeNumber.MO2_images3)
        img_link.append(url)
        img_id.append("carousel-3")
        img_count += 1
    records = MO6_Visit_record.objects.filter(MO3_DspotNumber=spot)
    if MO6_Visit_record.objects.filter(MO3_DspotNumber=spot,MO1_userNumber=mydata).exists():
        myrecords = MO6_Visit_record.objects.filter(MO3_DspotNumber=spot,MO1_userNumber=mydata)
    else:
        myrecords = ""
    myrecords = MO6_Visit_record.objects.filter(MO3_DspotNumber=spot,MO1_userNumber=mydata)
    blogs = MO7_Blog.objects.filter(MO6_visitRecordNumber__in=records,MO7_openRange=0)
    if myrecords == "":
        count = 0
    else:
        count = myrecords.count()
    params = {
        "spot":spot,
        "count":count,
        "myrecords":myrecords,
        "blogs":blogs,
        "img_link":img_link,
        "img_id":img_id,
        "img_count":img_count
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
        address = [i.MO4_OspotLat,i.MO4_OspotLng]
        o_list.append([address,i.MO4_OspotName, i.MO4_OspotNumber])
    params = {
        'd_list': json.dumps(d_list),
        'o_list': json.dumps(o_list),
        's_form':searchform,
        'tag_list':tag_list,
        'user':mydata,
        'page_user':page_user,
    }
    return render(request,"OtherMap.html",params)

@login_required
def OspotCreate(request):
    if request.method == 'POST':
        initial_data = {
            "MO1_userNumber":request.POST.get("MO1_userNumber"),
            "MO4_OspotName":request.POST.get("MO4_OspotName"),
            "MO4_OspotInfo":request.POST.get("MO4_OspotInfo"),
            "MO4_OspotLat":request.POST.get("lat"),
            "MO4_OspotLng":request.POST.get("lng"),
        }
        form = OspotCreateForm(initial_data)
        if form.is_valid() == False:
            for i in form:
                print(i)
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
    if request.method == 'POST':
        tags_id = request.POST.getlist('tags')
        keword = request.POST.get('keyword')
        tag_counter = len(tags_id)
        if tag_counter!=0:
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
            res = MO2_store.objects.raw(sql)
            print("r = ",res)
            for i in res:
                print("i = {}-{}".format(i.count,i.MO2_storeNumber))
            
            sql = """select * from maps_mo3_default_spot where 1=0 """
            for i in res:
                if i.count == tag_counter:
                    sql += """ or "MO2_storeNumber_id" = """+str(i.MO2_storeNumber)
            sql += """ ; """
        else:
            sql = "select * from maps_mo3_default_spot;"
        print("sql2="+sql)
        serch = MO3_Default_spot.objects.raw(sql)
        flg = 0
        user = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
        if request.POST.get("MO1_userID")==request.POST.get("page_user"):
            o_spot = MO4_Original_spot.objects.filter(MO1_userNumber = user)
            page_user = user
        else:
            page_user = CustomUser.objects.get(MO1_userNumber = int(request.POST.get("page_user")))
            o_spot = MO4_Original_spot.objects.filter(MO1_userNumber = page_user)
        o_spotform = OspotCreateForm()
        searchform = SpotSearchForm()
        tag_list = MO5_Tag.objects.all()
        d_list = []
        o_list = []
        for i in serch:
            d_list.append([i.MO2_storeNumber.MO2_address,i.MO2_storeNumber.MO2_storeName,i.MO3_DspotNumber])
        for i in o_spot:
            address = [i.MO4_OspotLat,i.MO4_OspotLng]
            o_list.append([address,i.MO4_OspotName, i.MO4_OspotNumber])
        print(d_list)
        params = {
            'd_list': json.dumps(d_list),
            'o_list': json.dumps(o_list),
            'o_form':o_spotform,
            's_form':searchform,
            'tag_list':tag_list,
            'user':user,
            'page_user':page_user,
        }
        if user == page_user:
            return render(request,"Map.html",params)
        else:
            return render(request,"OtherMap.html",params)
    return render(request,"Map.html",params)
