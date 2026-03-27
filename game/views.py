
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import Texts, GatekeeperFlag, MinisterFlags, KingFlags
from .ai_control import gatekeeper, minister, gatekeeperTrue, ministerTrue, king, kingTrue

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
        flag_now, created = GatekeeperFlag.objects.get_or_create(id=1, defaults={'flag': False})
        if flag_now.flag:
            flag_now.flag = False
            flag_now.save()
        return render(request, "game/stage1.html")
    
stage1 = Stage1View.as_view()

class Stage2View(View):
    def get(self, request):
        flag1_now, created1 = MinisterFlags.objects.get_or_create(id=1, defaults={'flag': False})
        flag2_now, created2 = MinisterFlags.objects.get_or_create(id=2, defaults={'flag': False})
        if flag1_now.flag:
            flag1_now.flag = False
            flag1_now.save()
        if flag2_now.flag:
            flag2_now.flag = False
            flag2_now.save()
        return render(request, "game/stage2.html")
    
stage2 = Stage2View.as_view()

class Stage3View(View):
    def get(self, request):
        flag1_now, created1 = KingFlags.objects.get_or_create(id=1, defaults={'flag': False})
        flag2_now, created2 = KingFlags.objects.get_or_create(id=2, defaults={'flag': False})
        flag3_now, created3 = KingFlags.objects.get_or_create(id=3, defaults={'flag': False})
        if flag1_now.flag:
            flag1_now.flag = False
            flag1_now.save()
        if flag2_now.flag:
            flag2_now.flag = False
            flag2_now.save()
        if flag3_now.flag:
            flag3_now.flag = False
            flag3_now.save()
        return render(request, "game/stage3.html")
    
stage3 = Stage3View.as_view()

class EpilogueView(View):
    def get(self, request):
        return render(request, "game/epilogue.html")
    
epilogue = EpilogueView.as_view()

# game/views.py

class DialogueView(View):
    def post(self, request, stage_tag):
        queryset = Texts.objects.filter(stage_tag=stage_tag).order_by('order')
        dialogue_list = [item.content for item in queryset]
        
        return JsonResponse({
            'dialogues': dialogue_list
        })

        
class GatekeeperResetView(View):
    def post(self, request):
        flag_now = GatekeeperFlag.objects.get(id=1)
        flag_now.flag = False
        flag_now.save()
        
        return JsonResponse({'status': 'success'})
        
class GatekeeperView(View):
    def post(self, request, ask):
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
            # gatekeeperTrueは仮で書いた関数
            message, is_cleared = gatekeeperTrue()
            
            return JsonResponse({
                'result': {
                    'message': message,
                    'is_cleared': is_cleared
                }
            })

class MinisterResetView(View):
    def post(self, request):
        flag1_now = MinisterFlags.objects.get(id=1)
        flag2_now = MinisterFlags.objects.get(id=2)
        flag1_now.flag = False
        flag2_now.flag = False
        flag1_now.save()
        flag2_now.save()
        
        return JsonResponse({'status': 'success'})


class MinisterView(View):
    def post(self, request, ask):
        flag1_now = MinisterFlags.objects.get(id=1)
        flag2_now = MinisterFlags.objects.get(id=2)
        if flag1_now.flag == False or flag2_now.flag == False:
            message, flag1, flag2 = minister(ask, flag1_now.flag, flag2_now.flag)
            flag1_now.flag = flag1
            flag1_now.save()
            flag2_now.flag = flag2
            flag2_now.save()

            return JsonResponse({
                'result': {
                    'message': message,
                    'flag1': flag1,
                    'flag2': flag2
                }
            })
        else:
            # ministerTrueは仮で書いた関数
            message, flag1, flag2 = ministerTrue()
            
            return JsonResponse({
                'result': {
                    'message': message,
                    'flag1': flag1,
                    'flag2': flag2
                }
            })

class KingResetView(View):
    def post(self, request):
        flag1_now = KingFlags.objects.get(id=1)
        flag2_now = KingFlags.objects.get(id=2)
        flag3_now = KingFlags.objects.get(id=3)
        flag1_now.flag = False
        flag2_now.flag = False
        flag3_now.flag = False
        flag1_now.save()
        flag2_now.save()
        flag3_now.save()
        
        return JsonResponse({'status': 'success'})
    
class KingView(View):
    def post(self, request, ask):
        flag1_now = KingFlags.objects.get(id=1)
        flag2_now = KingFlags.objects.get(id=2)
        flag3_now = KingFlags.objects.get(id=3)
        if flag1_now.flag == False or flag2_now.flag == False or flag3_now.flag == False:
            message, flag1, flag2, flag3 = king(ask, flag1_now.flag, flag2_now.flag, flag3_now.flag)
            flag1_now.flag = flag1
            flag1_now.save()
            flag2_now.flag = flag2
            flag2_now.save()
            flag3_now.flag = flag3
            flag3_now.save()

            return JsonResponse({
                'result': {
                    'message': message,
                    'flag1': flag1,
                    'flag2': flag2,
                    'flag3': flag3
                }
            })
        else:
            # kingTrueは仮で書いた関数
            message, flag1, flag2, flag3 = kingTrue()
            
            return JsonResponse({
                'result': {
                    'message': message,
                    'flag1': flag1,
                    'flag2': flag2,
                    'flag3': flag3
                }
            })