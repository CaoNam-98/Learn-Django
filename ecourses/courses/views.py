from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

# Create your views here.
# View là nơi nhận các request từ phía người dùng
# request là nơi sẽ nhận dữ liệu từ client gửi lên và thông qua request mình sẽ bóc tách để lấy data được gửi lên
def index(request):
    return render(request, template_name='index.html', context = { 'name': 'Cao Nam' })

# Tham số luôn luôn có request
# str() dùng để convert sang string
def welcome(request, year):
    return HttpResponse('Hello' + ' ' + str(year))

def welcome2(request, year):
    return HttpResponse('Hello' + ' ' + str(year))

class TestView(View):
    # sẽ gọi get khi mình gửi lên view này là HTTP get
    def get(self, request):
        return HttpResponse('Testing')

    def post(self, request):
        pass