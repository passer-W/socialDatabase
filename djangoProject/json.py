from django.http import HttpRequest, HttpResponse
from InviteModel.models import Invitee
import json

def get_info(request: HttpRequest):
    data_dict = {}
    try:
        if "id" in request.POST and request.session["isAdmin"]:
            user = Invitee.objects.get(id=request.POST["id"])
            data_dict = {"name":user.name, "code": user.code, "isActive": user.isActive, "isAdmin": user.isAdmin}
    except:
        pass
    return HttpResponse(json.dumps(data_dict))