# encoding: GBK

from InfoModel.models import Info

key = ["name","school","identity","xh","mm","sfzh","phone","email"]

def handle_file(file):
    info_list = []
    count = 0
    warning = ""
    try:
        if file.name.split(".")[-1] == "csv":
            for i in file.readlines():
                if count == 0:
                    count += 1
                    pass
                else:
                    try:
                        i = i.decode("GBK")
                    except:
                        i = i.decode("UTF-8")
                    info = i.strip().split(",")
                    info_list.append(info)
        else:
            warning = "不支持."+file.name.split(".")[-1]+"格式文件"
    except Exception as e:
        print(e)
        warning = "处理文件出错"
    return {"info_list":info_list, "warning":warning}

def handle_text(text):
    info_list = []
    warning = ""
    count = 0
    try:
        for i in text.split("\n"):
            info = i.strip().split(",")
            info_list.append(info)
            count += 1
    except:
        warning = "处理数据出错"
    return {"info_list": info_list, "warning": warning}

def save_info(info_list):
    count = 0
    warning = ""
    for info in info_list:
        try:
            info_model = Info(name=info[0], school=info[1], identity=info[2], xh=info[3], mm=info[4], sfzh=info[5], phone=info[6], email=info[7])
            info_model.save()
            count += 1
        except:
            warning = "数据格式有误，转换失败"
    return [count, warning]