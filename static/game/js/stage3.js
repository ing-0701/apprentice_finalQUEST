class DialogueManager {
    constructor() {
        this.dialogues = [];
        this.currentIndex = 0;
        this.currentTag = ''; // currentTagを初期化
    }

    // stage3.js の loadStage 内を少し補強
async loadStage(stageTag) {
    this.currentTag = stageTag;
    try {
        const response = await fetch(`/game/api/dialogue/${stageTag}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            }
        });
        const data = await response.json();
        
        if (!data.dialogues || data.dialogues.length === 0) {
            console.error(`警告: タグ "${stageTag}" のセリフが1件も見つかりませんでした。`);
            return; // データがないなら何もしない（勝手に進ませない）
        }

        this.dialogues = data.dialogues;
        this.currentIndex = 0;
        this.displayNext();
    } catch (error) {
        console.error("読み込み失敗:", error);
    }
}

    displayNext() {
        // 表示先のIDを 'response-area' に統一（HTMLと合わせてください）
        const targetElement = document.getElementById('response-area');
        
        if (this.currentIndex < this.dialogues.length) {
            const content = this.dialogues[this.currentIndex];
            targetElement.innerText = content;
            this.currentIndex++;
            console.log("セリフ表示中:", this.currentIndex);
        } else {
            console.log("全セリフ終了。次のステップへ");
            handleDialogueEnd(this.currentTag);
        }
    }
}

const manager = new DialogueManager();

// 終わった後の分岐処理
function handleDialogueEnd(tag) {
    if (tag === 'stage3') {
        document.getElementById('love-game-section').style.display = 'block';
        document.getElementById('response-area').innerText = "連打で愛を証明せよ！";
    } 
}

// --- 修正ポイント：イベントの制御 ---

// 1. 「次へ」ボタン
document.getElementById('go-to-dialogue').addEventListener('click', (e) => {
    // 【重要】このボタンクリックが「documentのクリック」として扱われないように防ぐ
    e.stopPropagation(); 
    
    document.getElementById('start-story-btn').style.display = 'none';
    manager.loadStage('stage3');
});

// 2. 画面クリックでセリフを送る
document.addEventListener('click', (e) => {
    // ボタンをクリックした時は、セリフ送りを二重に実行させない
    if (e.target.tagName === 'BUTTON' || e.target.tagName === 'INPUT') return;

    // 連打ゲームが表示されていない時だけ進める
    const loveSection = document.getElementById('love-game-section');
    if (loveSection && loveSection.style.display === 'none') {
        // セリフが読み込まれているかチェック
        if (manager.dialogues.length > 0) {
            manager.displayNext();
        }
    }
});

// 3. 連打ボタン
let loveCount = 0;
document.getElementById('love-button').addEventListener('click', (e) => {
    e.stopPropagation(); // 連打がセリフ送りに干渉しないように
    loveCount++;
    document.getElementById('love-gauge').style.width = (loveCount * 5) + "%";
    if (loveCount >= 20) {
        document.getElementById('love-game-section').style.display = 'none';
        manager.dialogues = [];
        document.getElementById('response-area').innerText = "そなたの愛が本物であることがようわかった。姫との結婚を認めよう！";
        document.getElementById('next-action').style.display = 'block';
        console.log("連打クリア！王の認可が降りました。");
    }
});