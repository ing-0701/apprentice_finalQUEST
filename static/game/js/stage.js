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

    try {
        const response = await fetch(`${apiUrl}${encodeURIComponent(askText)}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
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
        }

        if (isCleared) {
            // 入力エリアを隠す
            userInputField.style.display = 'none';
            // ボタンを包んでいる親要素（btn-wrapperなど）を隠す
            btn.closest('div').style.display = 'none'; 
            
            // 次のアクションを表示（HTML側のデータ属性で指定したIDを出す）
            const nextAction = document.getElementById(nextActionId);
            if (nextAction) {
                nextAction.style.display = 'block';
            }
        } else {
            userInputField.value = '';
        }

    } catch (error) {
        console.error("通信エラーが発生しました:", error);
    }
}
