
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import Texts, GatekeeperFlag
from .ai_control import gatekeeper

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

class DialogueView(View):
    def post(self, request, stage_tag):
        queryset = Texts.objects.filter(stage_tag=stage_tag).order_by('order')
        dialogue_list = [item.content for item in queryset]
        
        return JsonResponse({
            'dialogues': dialogue_list
        })

        
class GatekeeperView(View):
    def post(self, request, stage_tag, ask):
        flag_now = GatekeeperFlag.objects.get(id=1)
        if flag_now.flag == False:
            message, is_cleared = gatekeeper(ask)
            flag_now.flag = is_cleared
            flag_now.save()

            return JsonResponse({
                'result': {
                    'message': message,
                    'is_cleared': is_cleared
                }
            })
        else:
            message, is_cleared = gatekeeperTrue()
            
            return JsonResponse({
                'result': {
                    'message': message,
                    'is_cleared': is_cleared
                }
            })

