# encoding: GBK

user_list = ["admin", "jonny", "sammy"]

from django.shortcuts import render
import random
from InviteModel.models import Invitee
from django.http import HttpRequest, HttpResponse, FileResponse
#
# def get_page(url: str):
#     return url.split(r"/")[-2]

def isIllegal(request):
    if not "name" in request.session:
        ctx = get_ctx({}, 3)
        ctx["warning"] = "请先登录！"
        return get_form(request, ctx)
    else:
        return False

def get_lastpage(count, each_num):
    if count == 0:
        return 1
    if count % each_num == 0:
        return int(count/each_num)
    else:
        return int(count/each_num)+1

def get_ctx(ctx, num):
    ctx['active'] = ['', '', '', '', '']
    ctx['active'][num] = 'active'
    return ctx

def create_code(name):
    num = random.randint(1000, 9999)
    code = name + "@" + str(num)
    return code


def get_form(request: HttpRequest, ctx=None):
    if ctx == None:
        ctx = get_ctx({}, 3)
    try:
        if "name" in request.session and request.session["name"] != "null":
            ctx["name"] = request.session["name"]
            ctx["isAdmin"] = request.session["isAdmin"]
            ctx["code"] = request.session["code"]
            return render(request, "result.html", ctx)
    except:
        pass
    return render(request, "invite.html", ctx)


def select_user(name, code):
    try:
        if code:
            user = Invitee.objects.get(code=code)
            if user:
                return [user, ""]
        else:
            user = Invitee.objects.get(name=name)
            if user.isActive and not user.isAdmin:
                return [user, "请使用邀请码登录"]
            else:
                user.code = create_code(user.name)
                user.isActive = True
                user.save()
                return [user, ""]
    except:
        pass
    return [Invitee(name="null"), "抱歉，您暂时未获得邀请资格"]


def test_code(code):
    if Invitee.objects.filter(name=code):
        result = select_user(code, "")
    else:
        result = select_user("", code)
    return result


def verify(request: HttpRequest):
    ctx = get_ctx({}, 3)
    ctx["name"] = "null"
    if request.method == "POST":
        if "code" in request.POST or True:
            code = request.POST["code"]
            result = test_code(code)
            ctx["warning"] = result[1]
            if ctx["warning"] == "":
                ctx["code"] = request.session["code"] = result[0].code
                ctx["name"] = request.session["name"] = result[0].name
                ctx["isAdmin"] = request.session["isAdmin"] = result[0].isAdmin
                ctx["success_message"] = "登陆成功"
                request.session["login"] = True
    else:
        ctx["warning"] = "禁止GET请求"
    return get_form(request, ctx)

def exit(request):
    ctx = get_ctx({}, 3)
    session_list = ["name", "login", "code", "isAdmin"]
    try:
        isLogin = True
        for i in session_list:
            if not i in request.session:
                isLogin =False
        if isLogin:
            request.session.flush()
            ctx["success_message"] = "注销成功"
            print(request.session["name"])
        else:
            ctx["warning"] = "您尚未登陆"
    except:
        pass
    return get_form(request, ctx)
