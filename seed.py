import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

django.setup()

from game.models import Texts, GatekeeperFlag, MinisterFlags

def run():
    Texts.objects.filter(stage_tag='prologue').delete()
    
    prologue_texts = [
        "ここはとある王国",
        "僕は、この国の姫と密かに愛し合っていた",
        "ただの商人であるぼくにとって、身分を越えた関係…… ずっと隠し通すつもりだった",
        "だけど、正式に結婚して、堂々と会えるようになりたい！",
        "城に出向いて、直接王様にお願いしよう！！",
    ]
    
    for i, text in enumerate(prologue_texts, start=1):
        Texts.objects.create(
            stage_tag='prologue',
            order=i,
            content=text
        )
        
        
    Texts.objects.filter(stage_tag='stage3_clear_before').delete()
    
    stage3_texts = [
        "じゃが、最後に確かめたいことがある。",
        "お前は本当に……心の底から、あの子を愛しているのか？",
        "ならば、証明してみせよ！ 喉が枯れ、指が動かなくなるまで、その想いを叫び続けるのじゃ！",
        "さあ、お前の真実を……その叫びを、私に刻みつけてみせろ！！",
    ]
    
    for i, text in enumerate(stage3_texts, start=1):
        Texts.objects.create(
            stage_tag='stage3_clear_before',
            order=i,
            content=text
        )
    
    
    Texts.objects.filter(stage_tag='epilogue').delete()
    
    epilogue_texts = [
        "王に認められた僕たちは、正式に結婚した",
        "王座に就かないと約束した通り、僕は一般貴族として暮らすことになった",
        "料理の勉強をして、毎日姫のために食事を作っている　最近は体調もずいぶんよくなった",
        "そうして僕たちは、いつまでも幸せに暮らした",
    ]
    
    for i, text in enumerate(epilogue_texts, start=1):
        Texts.objects.create(
            stage_tag='epilogue',
            order=i,
            content=text
        )
        
        
    GatekeeperFlag.objects.all().delete()
    GatekeeperFlag.objects.create(
        flag=False
    )
    
    MinisterFlags.objects.all().delete()
    MinisterFlags.objects.create(
        flag=False
    )
    MinisterFlags.objects.create(
        flag=False
    )
        
if __name__ == '__main__':
    run()