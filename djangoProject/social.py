# encoding: GBK

from django.shortcuts import render
from SchoolModel.models import School
from InfoModel.models import Info
from django.http import HttpRequest
from django.db.models import Q
from . import invite


def get_pages(page, last_page):
    page_list = []
    if last_page < 9:
        for i in range(1, last_page + 1):
            page_list.append(i)
        return page_list
    if page < 7:
        for i in range(1, 9):
            page_list.append(i)
        page_list.extend(["...", last_page - 1, last_page])
    elif page < last_page - 4:
        page_list.extend([1, 2, "..."])
        for i in range(-3, 3):
            page_list.append(page + i)
        page_list.extend(["...", last_page - 1, last_page])
    else:
        page_list.extend([1, 2, "..."])
        for i in range(last_page - 7, last_page + 1):
            page_list.append(i)
    return page_list


def get_ctx(ctx, list_name, all_list, page, last_page, menu_num, query):
    ctx[list_name] = all_list  # 总列表
    ctx["count"] = len(all_list)
    ctx["loop_times"] = range(0, 2)
    ctx["page"] = page  # 当前页数
    ctx['notfirst'] = 0 if page == 1 else -1
    ctx['notlast'] = 0 if page == last_page else 1
    ctx['active'] = ['', '', '', '', '']
    ctx['active'][menu_num] = 'active'
    ctx['pages'] = get_pages(page, last_page)
    ctx["query"] = query
    return ctx


def get_school(request: HttpRequest, ctx=None, school=""):
    if not ctx:
        ctx = {}
    if invite.isIllegal(request):
        return invite.isIllegal(request)
    if "q" in request.GET and ctx=={}:
        school = request.GET["q"]
    if "'" in school:
        school = ""
    each_num = 20  # 每页显示20条数据
    if "page" in request.GET:
        page = int(request.GET["page"])
    else:
        page = 1
    if school == "":
        school_list = School.objects.order_by("id")
    else:
        school_list = School.objects.order_by("id").filter(name__contains=school)
    last_page = invite.get_lastpage(school_list.count(), each_num)
    ctx = get_ctx(ctx, "school_list", school_list[(page - 1) * each_num:page * each_num], page, last_page, 0, "高校名")
    if school == "":
        ctx["page_url"] = "/social/list?page="
    else:
        ctx["page_url"] = "/social/list?q=%s&page=" % school
    return render(request, "school_list.html", ctx)


def get_info(request: HttpRequest, ctx=None):
    if ctx == None:
        ctx = {}
    if invite.isIllegal(request):
        return invite.isIllegal(request)
    each_num = 30  # 每页显示30条数据
    query = ""
    limit = 100000 if request.session["isAdmin"] else 30
    if "school" in request.GET:
        school = request.GET["school"]
        ctx["school"] = school
    else:
        return get_school(request)
    if "q" in request.GET and not "warning" in ctx:
        if not request.session["isAdmin"]:
            ctx = invite.get_ctx(ctx, 0)
            ctx["warning"] = "您不具有查询权限"
        else:
            query = request.GET["q"]
    if "'" in school:
        school = ""
    if 'page' in request.GET:
        page = int(request.GET["page"])
    else:
        page = 1
    if query == "":
        info_list = Info.objects.order_by("id").filter(school=school)[:limit]
    else:
        info_list = Info.objects.order_by("id").filter(Q(school=school),
                                                       Q(xh__contains=query) | Q(name__contains=query))[:limit]
    last_page = invite.get_lastpage(info_list.count(), each_num)
    info_list = info_list[(page - 1) * each_num:page * each_num]
    ctx = get_ctx(ctx, "info_list", info_list, page, last_page, 1, "学号或姓名")
    ctx["page_url"] = "/social/info?school=%s&page=" % school
    return render(request, "info_list.html", ctx)
