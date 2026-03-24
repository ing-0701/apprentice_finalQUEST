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

async function sendDialogue() {
    // 1. inputの内容をキャッチ
    const userInputField = document.getElementById('user-input');
    const askText = userInputField.value;

    if (!askText) return; // 空入力なら何もしない

    try {
        // 2. DjangoのGatekeeperViewへ送信
        // 定義されているURL構造に合わせてパスを修正
        const response = await fetch(`/game/api/gatekeeper_ask/${encodeURIComponent(askText)}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), // または getCsrfToken()
            }
        });
        const data = await response.json();
        const result = data.result;

        // 3. メッセージを画面に表示
        document.getElementById('response-area').innerText = result.message;

        // 4. クリア判定（trueならボタンを切り替え）
        if (result.is_cleared === true) {
            // 入力欄と送信ボタンを隠す
            userInputField.style.display = 'none';
            document.getElementById('ask-button').style.display = 'none';
            
            // 次のステージへのボタンを表示
            document.getElementById('gatekeeper-next-action').style.display = 'block';
        } else {
            // 失敗なら入力欄を空にして次を促す
            userInputField.value = '';
        }

    } catch (error) {
        console.error("通信エラーが発生しました:", error);
    }
}