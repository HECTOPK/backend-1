import requests
from django.shortcuts import HttpResponse
from afisha.models import Bitcoin
from django.shortcuts import render


def api(request):
    r = requests.get("https://api.blockchain.info/stats")
    if r.status_code == 200:
        btc = Bitcoin()
        for i in r.json():
            print(i, r.json()[i])
            if i == "total_fees_btc":
                btc.total = r.json()[i]
            if i == "blocks_size":
                btc.blocks = r.json()[i]
        btc.save()
        return HttpResponse(r.json())
    else:
        return HttpResponse("Afisha error")


# вывод страницы стписка фильмов
def list(request):
    return render(request, 'index.html')
