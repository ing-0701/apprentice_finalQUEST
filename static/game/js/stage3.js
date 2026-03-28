class DialogueManager {
    constructor() {
        this.dialogues = [];
        this.currentIndex = 0;
        this.currentTag = ''; // currentTagを初期化
    }

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

        this.dialogues = data.dialogues;
        this.currentIndex = 0;
        this.displayNext();
    } catch (error) {
        console.error("読み込み失敗:", error);
    }
}

    displayNext() {
        const targetElement = document.getElementById('response-area');
        
        if (this.currentIndex < this.dialogues.length) {
            const content = this.dialogues[this.currentIndex];
            targetElement.innerText = content;
            this.currentIndex++;
        } else {
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


// 1. イベントリスナーの設定
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
let decreaseInterval = null;  // ゲージ減少用タイマー
let countdownInterval = null; // 5秒制限用タイマー
let remainingTime = 5;        // 制限時間（秒）

// 1. セリフ終了時の処理
function handleDialogueEnd(tag) {
    if (tag === 'stage3') {
        document.getElementById('love-game-section').style.display = 'block';
        
        // 最初の表示をセット
        remainingTime = 7;
        updateTimerDisplay(); 
        
        // タイマーと減少処理をダブルで開始
        startDecreasing();
        startCountdown();
    } 
}

// 2. 【新設】カウントダウンタイマー（5秒制限）
function startCountdown() {
    if (countdownInterval) clearInterval(countdownInterval);

    countdownInterval = setInterval(() => {
        remainingTime -= 1;
        updateTimerDisplay();

        if (remainingTime <= 0) {
            // 時間切れ：ゲームオーバー
            gameOver();
        }
    }, 1000); // 1秒ごとに実行
}

// 3. 【新設】タイマーの表示更新
function updateTimerDisplay() {
    const responseArea = document.getElementById('response-area');
    if (responseArea) {
        responseArea.innerText = `【連打で愛を証明せよ！】 残り時間: ${remainingTime}秒`;
        responseArea.style.color = remainingTime <= 2 ? "#ff4757" : "#121212"; // 2秒以下で赤文字に
    }
}

// 4. 【新設】ゲームオーバー処理
function gameOver() {
    clearInterval(decreaseInterval);
    clearInterval(countdownInterval);
    alert("時間切れだ！お前の愛はその程度か！");
    window.location.href = '/game/'; 
}

// 5. ゲージを減らす関数（0.1秒ごとに少しずつ減る）
function startDecreasing() {
    if (decreaseInterval) clearInterval(decreaseInterval);
    decreaseInterval = setInterval(() => {
        if (loveCount > 0) {
            loveCount -= 0.2; // 減るスピード（調整可）
            updateGauge();
        }
    }, 100);
}

// 6. ゲージ更新
function updateGauge() {
    const gauge = document.getElementById('love-gauge');
    if (gauge) {
        gauge.style.width = (loveCount * 5) + "%";
    }
}

// 7. 連打ボタンの処理
document.getElementById('love-button').addEventListener('click', (e) => {
    e.stopPropagation();
    
    if (loveCount < 20) {
        loveCount++;
        updateGauge();
    }

    if (loveCount >= 20) {
        // クリア：すべてのタイマーを止める
        clearInterval(decreaseInterval);
        clearInterval(countdownInterval);
        
        document.getElementById('love-game-section').style.display = 'none';
        manager.dialogues = [];
        document.getElementById('response-area').innerText = "そなたの愛が本物であることがようわかった。姫との結婚を認めよう！";
        document.getElementById('response-area').style.color = "#121212";
        document.getElementById('next-action').style.display = 'block';
    }
});