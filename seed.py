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