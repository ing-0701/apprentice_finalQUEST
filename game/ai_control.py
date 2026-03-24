import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key = os.getenv("API_KEY"))

model = genai.GenerativeModel('gemini-2.5-flash')



def gatekeeper(user_input): # userinput -> message, flag

    prompt = f"""
    あなたは城を守るお酒好きの門番です。以下の条件で返答してください。
    【ユーザーの発言】:"{user_input}"

    条件:
    ・ユーザは姫と結婚したい商人です。
    ・100万~1000万の金額提示のみクリア。それ以外の質問に対しては、お金が必要であることをほのめかすような解答にしてください。
    ・いくらほしい？と聞かれても具体的な金額は言わないでください。
    ・返答は必ず次のJSON形式のみ。:{{"message": "セリフ", "is_cleared": true/false}}
    ・セリフの口調は統一してください。（一般市民に対する口調）
    """

    response = model.generate_content(prompt)
    raw_text = response.text

    try:
        if "```json" in raw_text:
            res_json = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
            res_json = raw_text.split("```")[1].split("```")[0].strip()
        else:
            res_json = raw_text
        result = json.loads(res_json)
        
        return result["message"], result["is_cleared"]
    
    except:
        return "(門番は困惑している...)", False


def minister(user_input, flag1, flag2): # userinput, flag1(政策), flag2(研究) -> message, flag1(政策), flag2(研究)

    prompt = f"""
    あなたは城にいる大臣です。以下の条件で返答してください。
    【政策について】: {flag1}
    【研究について】: {flag2}
    【ユーザーの発言】:"{user_input}"

    条件:
    ・ユーザは姫と結婚したい市民です。
    ・政策と研究両方をほめるとクリア。両方ともfalseの場合、ユーザーの発言に対して政策または研究についての言及をしてください。
      片方のみTrueの場合、もう片方についてほのめかすような解答にしてください。
    ・政策・研究のいずれかについてインプットがtrueの場合、そのフラグはそのままtrueで返してください。
    ・返答は必ず次のJSON形式のみ。:{{"message": "セリフ", "flag1": true/false, "flag2": true/false}}
    ・ただし、flag1が政策について、flag2が研究についてのフラグです。
    ・セリフの口調は統一してください。（一般市民に対する口調）
    """

    response = model.generate_content(prompt)
    raw_text = response.text

    try:
        if "```json" in raw_text:
            res_json = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
            res_json = raw_text.split("```")[1].split("```")[0].strip()
        else:
            res_json = raw_text
        result = json.loads(res_json)
        
        return result["message"], result["flag1"], result["flag2"]
    
    except:
        return "(大臣は困惑している...)", False, False

def king(user_input, flag1, flag2, flag3): # userinput, flag1(看病), flag2(料理), flag3(王座の興味) -> flag1(看病), flag2(料理), flag3(王座の興味)

    prompt = f"""
    あなたは城にいる王です。以下の条件で返答してください。
    【姫の病気の看病について】: {flag1}
    【料理について】: {flag2}
    【王座について】: {flag3}
    【ユーザーの発言】:"{user_input}

    条件:
    ・ユーザは姫と結婚したい市民です。
    ・「姫の病気の看病をする」「料理をする」「王座に興味はない」の3つの条件が揃えばクリア。
      いずれかがFalseの場合、他の条件についてのヒントを出すような発言をしてください
    ・「姫の病気の看病をする」「料理をする」「王座に興味はない」のいずれかについてインプットがtrueの場合、そのフラグはそのままtrueで返してください。
    ・返答は必ず次のJSON形式のみ。:{{"message": "セリフ", "flag1": true/false, "flag2": true/false, "flag3" : true/false}}
    ・ただし、flag1が姫の病気の看病について、flag2が料理について、flag3が王座についてのフラグです。
    ・セリフの口調は統一してください。（一般市民に対する口調）
    """

    response = model.generate_content(prompt)
    raw_text = response.text

    try:
        if "```json" in raw_text:
            res_json = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
            res_json = raw_text.split("```")[1].split("```")[0].strip()
        else:
            res_json = raw_text
        result = json.loads(res_json)
        
        return result["message"], result["flag1"], result["flag2"], result["flag3"]
    
    except:
        return "(王は困惑している...)", False, False, False


def gatekeeperTrue():
    return "早く行け", True


def ministerTrue():
    return "大臣は既に満足している。政策・研究は両方とも評価済みだ。", True, True

print(gatekeeper("こんにちは"))
