// CSRFトークン取得用の共通関数
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ページが読み込まれたらボタンに機能を割り当てる
document.addEventListener('DOMContentLoaded', () => {
    const submitBtn = document.getElementById('ask-button');
    if (submitBtn) {
        submitBtn.addEventListener('click', sendDialogue);
    }
});

async function sendDialogue() {
    // ボタンからデータを取得
    const btn = document.getElementById('ask-button');
    const apiUrl = btn.dataset.apiUrl; 
    const stage = btn.dataset.stage;   
    const nextActionId = btn.dataset.nextActionId; // 次のボタンのIDを取得

    const userInputField = document.getElementById('user-input');
    const responseArea = document.getElementById('response-area');
    const askText = userInputField.value;

    if (!askText) return;

    const originalBtnText = btn.innerText;
    responseArea.innerText = "考え中..."; // セリフエリアを「考え中」に変える
    btn.disabled = true;                // ボタンをグレーアウトして連打防止
    btn.innerText = "送信中...";

    try {
        const response = await fetch(`${apiUrl}${encodeURIComponent(askText)}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfToken(),
            }
        });
        const data = await response.json();
        const result = data.result;

        // メッセージを表示
        responseArea.innerText = result.message;

        // ステージごとのクリア判定
        let isCleared = false;
        if (stage === "1") {
            isCleared = (result.is_cleared === true);
        } else if (stage === "2") {
            // ステージ2はflag1とflag2の両方がtrueならクリア
            isCleared = (result.flag1 === true && result.flag2 === true);
        } else if (stage === "3") {
            // ステージ3はflag1とflag2とflag3のすべてがtrueならクリア
            isCleared = (result.flag1 === true && result.flag2 === true && result.flag3 === true);
        }

        if (isCleared) {
            // 入力エリアを隠す
            userInputField.style.display = 'none';
            // ボタンを包んでいる親要素（btn-wrapperなど）を隠す
            btn.closest('div').style.display = 'none'; 
            
            // 次のアクションを表示（HTML側のデータ属性で指定したIDを出す）
            if (isCleared) {
                // 全ステージ共通：入力欄と送信ボタンを隠す
                userInputField.style.display = 'none';
                btn.closest('.btn-wrapper').style.display = 'none'; 
    
                // 全ステージ共通：HTMLで指定された「次へ」ボタンを表示する
                // ステージ1なら「城へ」、ステージ3なら「次へ（物語開始）」が表示される
                const nextAction = document.getElementById(nextActionId);
                if (nextAction) {
                    nextAction.style.display = 'block';
                }
            } else {
                // クリアしていない場合
                userInputField.value = '';
                btn.disabled = false;
                btn.innerText = originalBtnText;
            }
        } else {
            userInputField.value = '';
            btn.disabled = false;
            btn.innerText = originalBtnText;
        }

    } catch (error) {
        console.error("通信エラーが発生しました:", error);
        btn.disabled = false;
        btn.innerText = originalBtnText;
    }
}
