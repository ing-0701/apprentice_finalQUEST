from django.shortcuts import render
from django.views import View

class StartView(View):
    def get(self, request):
        return render(request, "game/start.html")
    
start = StartView.as_view()

class PrologueView(View):
    def get(self, request):
        return render(request, "game/prologue.html")
    
prologue = PrologueView.as_view()

class Stage1View(View):
    def get(self, request):
        return render(request, "game/stage1.html")
    
stage1 = Stage1View.as_view()

class Stage2View(View):
    def get(self, request):
        return render(request, "game/stage2.html")
    
stage2 = Stage2View.as_view()

class Stage3View(View):
    def get(self, request):
        return render(request, "game/stage3.html")
    
stage3 = Stage3View.as_view()

class EpilogueView(View):
    def get(self, request):
        return render(request, "game/epilogue.html")
    
epilogue = EpilogueView.as_view()