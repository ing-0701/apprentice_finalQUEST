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
    ・ユーザーの発言が政策について肯定的（ほめる、評価する）な内容を含む場合、flag1をtrueに設定。それ以外はfalse。
    ・ユーザーの発言が研究について肯定的（ほめる、評価する）な内容を含む場合、flag2をtrueに設定。それ以外はfalse。
    ・既にtrueのフラグはそのままtrueに保つ。
    ・メッセージは大臣として、ユーザーの発言に応じた返答をし、falseのままのフラグについてヒントを与えるような発言をする。例えば、flag1がfalseなら政策についてほのめかす、flag2がfalseなら研究についてほのめかす。
    ・返答は必ず次のJSON形式のみ。:{{"message": "セリフ", "flag1": true/false, "flag2": true/false}}
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
    【ユーザーの発言】:"{user_input}"

    条件:
    ・ユーザは姫と結婚したい市民です。
    ・ユーザーの発言が姫の病気の看病について肯定的（する、協力する）な内容を含む場合、flag1をtrueに設定。それ以外はfalse。
    ・ユーザーの発言が料理について肯定的（する、作る）な内容を含む場合、flag2をtrueに設定。それ以外はfalse。
    ・ユーザーの発言が王座に興味がない（ない、興味ない）ことを示す場合、flag3をtrueに設定。それ以外はfalse。
    ・既にtrueのフラグはそのままtrueに保つ。
    ・メッセージは王として、ユーザーの発言に応じた返答をし、falseのままのフラグについてヒントを与えるような発言をする。例えば、flag1がfalseなら看病についてほのめかす、flag2がfalseなら料理についてほのめかす、flag3がfalseなら王座についてほのめかす。
    ・返答は必ず次のJSON形式のみ。:{{"message": "セリフ", "flag1": true/false, "flag2": true/false, "flag3": true/false}}
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

def kingTrue():
    return "王は既に満足している。姫の看病・料理・王座はすべて評価済みだ。", True, True, True

print(gatekeeper("こんにちは"))
