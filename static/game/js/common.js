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

// --- [パーツ2] セリフ管理クラス ---
class DialogueManager {
    constructor() {
        this.dialogues = [];
        this.currentIndex = 0;
    }

    async loadStage(stageTag) {
        try {
            // 注意：URLは実際のDjangoのurls.pyの設定に合わせて調整してください
            const response = await fetch(`/api/dialogue/${stageTag}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });
            const data = await response.json();
            
            this.dialogues = data.dialogues;
            this.currentIndex = 0;
            this.displayNext();
        } catch (error) {
            console.error("セリフの読み込みに失敗しました:", error);
            document.getElementById('dialogue-text').innerText = "エラーが発生しました";
        }
    }

    displayNext() {
        if (this.currentIndex < this.dialogues.length) {
            const content = this.dialogues[this.currentIndex];
            document.getElementById('dialogue-text').innerText = content;
            this.currentIndex++;
        } else {
            document.getElementById('dialogue-text').innerText = "（おわり）";
        }
    }
}

// --- [パーツ3] 実行 ---
const manager = new DialogueManager();

document.addEventListener('click', () => {
    manager.displayNext();
});

// 実行（HTML読み込み完了時に呼ぶ）
window.onload = () => {
    manager.loadStage('prologue');
};