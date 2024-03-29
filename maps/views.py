from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import generic
from accounts.models import CustomUser,MO6_Visit_record
from .models import MO3_Default_spot,MO4_Original_spot,MO5_Tag
from store.models import MO2_store,MO12_storeEng
from .forms import *
from blog.models import MO7_Blog
import json
import datetime
from django.contrib.auth.decorators import login_required
from django.db import connection

# 翻訳APIをインポート
from googletrans import Translator

# Translatorクラスのインスタンスを生成
translator = Translator()
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
    d_spot = MO3_Default_spot.objects.select_related('MO2_storeNumber').order_by('MO2_storeNumber')
    o_spot = MO4_Original_spot.objects.filter(MO1_userNumber = request.user.MO1_userNumber)
    d_list = []
    o_list = []
    eng_d_spot = MO12_storeEng.objects.filter(MO12_storeNameLng=user.MO1_language).values_list("MO2_storeNumber","MO12_storeNameEng").order_by("MO2_storeNumber")
    dic_eng = dict(list(eng_d_spot))
    for i in d_spot:
        image = image_url(i)
        print(image)
        if user.MO1_language == "ja":
            name = i.MO2_storeNumber.MO2_storeName
        else:
            name = dic_eng[i.MO2_storeNumber.MO2_storeNumber]
        d_list.append([i.MO2_storeNumber.MO2_address,name.replace('\'', '`'),i.MO3_DspotNumber,image])
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
    trans_info = translator.translate(str(spot.MO2_storeNumber.MO2_storeInfo),dest="en",str="auto").text
    trans_name = MO12_storeEng.objects.get(MO12_storeNameLng="en",MO2_storeNumber=spot.MO2_storeNumber)
    tag = spot.MO5_tagNumber.all()
    params = {
        "spot":spot,
        "count":count,
        "myrecords":myrecords,
        "blogs":blogs,
        "trans_info":trans_info,
        "trans_name":trans_name,
        "img_link":img_link,
        "img_id":img_id,
        "img_count":img_count,
        "tag":tag,
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
    eng_d_spot = MO12_storeEng.objects.filter(MO12_storeNameLng=mydata.MO1_language).values_list("MO2_storeNumber","MO12_storeNameEng").order_by("MO2_storeNumber")
    dic_eng = dict(list(eng_d_spot))
    for i in d_spot:
        image = image_url(i)
        if mydata.MO1_language == "ja":
            name = i.MO2_storeNumber.MO2_storeName
        else:
            name = dic_eng[i.MO2_storeNumber.MO2_storeNumber]
        d_list.append([i.MO2_storeNumber.MO2_address,name,i.MO3_DspotNumber,image])
    for i in o_spot:
        url = "/static/images/noimage.jpg"
        address = [i.MO4_OspotLat,i.MO4_OspotLng]
        o_list.append([address,i.MO4_OspotName, i.MO4_OspotNumber,url])
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
    if request.method == 'POST':
        tags_id = request.POST.getlist('tags')
        keword = request.POST.get('keyword')
        print("tags=",tags_id)
        print("keword=",keword)
        tag_counter = len(tags_id)
        user = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
        user_lang = user.MO1_language
        sql = """ select count(*), "MO2_storeNumber" from maps_mo3_default_spot inner join store_mo2_store on ( store_mo2_store."MO2_storeNumber" = "maps_mo3_default_spot"."MO2_storeNumber_id" ) """
        if tag_counter!=0:
            sql += """ inner join "maps_mo3_default_spot_MO5_tagNumber" on ( "maps_mo3_default_spot"."MO3_DspotNumber" = "maps_mo3_default_spot_MO5_tagNumber"."mo3_default_spot_id" ) """
        if keword != "":
            if user_lang == "ja":
                sql += """ where "store_mo2_store"."MO2_storeName" LIKE '%{}%' """
            else:
                sql += """ inner join store_mo12_storeeng on ("store_mo2_store"."MO2_storeNumber" = "store_mo12_storeeng"."MO2_storeNumber_id") where \"MO12_storeNameEng\" LIKE '%{}%' """;
        else:
            sql += """ where 1=1 """
        if tag_counter != 0:
            sql += """ and (1=0 """
            for i in tags_id:
                sql += """ or "mo5_tag_id" = """+i
            sql += """)"""
        sql += """ group by "MO2_storeNumber";"""
        cursor = connection.cursor()
        cursor.execute(sql.format(keword))
        res = cursor.fetchall()
        sql = """select * from maps_mo3_default_spot where 1=0 """
        for i in range(len(res)):
            if tag_counter == 0:
                sql += """ or "MO2_storeNumber_id" = """+str(res[i][1])
            elif res[i][0] == tag_counter:
                sql += """ or "MO2_storeNumber_id" = """+str(res[i][1])
        sql += """ ; """
        serch = MO3_Default_spot.objects.raw(sql)
        if request.POST.get("MO1_userID")==request.POST.get("page_user"):
            o_spot = MO4_Original_spot.objects.filter(MO1_userNumber = user)
            page_user = user
        else:
            page_user = CustomUser.objects.get(MO1_userNumber = int(request.POST.get("page_user")))
            o_spot = MO4_Original_spot.objects.filter(MO1_userNumber = page_user)
        o_spotform = OspotCreateForm()
        searchform = SpotSearchForm()
        tag_list = MO5_Tag.objects.all()
        sea_tags = MO5_Tag.objects.filter(MO5_tagNumber__in = tags_id)
        eng_d_spot = MO12_storeEng.objects.filter(MO12_storeNameLng=user_lang).values_list("MO2_storeNumber","MO12_storeNameEng").order_by("MO2_storeNumber")
        dic_eng = dict(list(eng_d_spot))
        d_list = []
        o_list = []
        for i in serch:
            image = image_url(i)
            if user.MO1_language == "ja":
                name = i.MO2_storeNumber.MO2_storeName
            else:
                name = dic_eng[i.MO2_storeNumber.MO2_storeNumber]
            d_list.append([i.MO2_storeNumber.MO2_address,name,i.MO3_DspotNumber,image])
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
            'sea_tags':sea_tags,
            'keyword':keword,
            'user':user,
            'page_user':page_user,
        }
        if user == page_user:
            return render(request,"Map.html",params)
        else:
            return render(request,"OtherMap.html",params)
    return render(request,"Map.html",params)
