# encoding: GBK

from django.shortcuts import render
from SchoolModel.models import School
from django.http import HttpRequest, HttpResponse, FileResponse
from InfoModel.models import Info
from . import infofile

def get_ctx(ctx):
    ctx['active'] = ['', '', '']
    ctx['active'][2] = 'active'
    return ctx

def get_model(request):
    file = open("model/model.csv", "rb")
    response = FileResponse(file)
    response['content_type'] = "application/octet-stream"
    response['Content-Disposition'] = 'attachment; filename="model.csv"'
    return response

def get_form(request: HttpRequest):
    ctx = get_ctx({})
    return render(request, 'update.html', ctx)

def update_info(request: HttpRequest):
    ctx = get_ctx({})
    if request.method == "POST":
        if 'file' in request.FILES:
            result = infofile.handle_file(request.FILES['file'])
        elif 'text' in request.POST:
            result = infofile.handle_text(request.POST['text'])
        else:
            result = {"info_list":[], "warning":"请上传数据"}
        if result["warning"] != "":
            result["count"] = 0
        else:
            save_result = infofile.save_info(result["info_list"])
            result["count"] = save_result[0]
            result["warning"] = save_result[1]
            if 'both' in request.POST:
                if request.POST['both'] == 'true':
                    update_school(request)
        del result['info_list']
        ctx["result"] = result
    return render(request, "update.html", ctx)



def update_school(request: HttpRequest):
    old__results = School.objects.all()
    old_schools = []
    for i in old__results:
        old_schools.append(i.name)
    new_results = Info.objects.values("school").distinct()
    new_school_list = []
    for i in new_results:
        try:
            new_school_list.append(i["school"])
        except:
            pass
    new_school_list = set(new_school_list)
    total = len(old_schools)
    count = 0
    del_count = 0
    for i in new_school_list:
        if not i in old_schools:
            count += 1
            school = School(name=i, id=total+count)
            school.save()
    for i in old_schools:
        if not i in new_school_list:
            school = School.objects.get(name=i)
            school.delete()
            del_count += 1
    return HttpResponse(r'<script>alert("更新完毕，共增加%d组学校数据， 删除%d组学校数据");window.location.href="/social/list"</script>'%(count, del_count))
