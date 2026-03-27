class DialogueManager {
    constructor() {
        this.dialogues = [];
        this.currentIndex = 0;
    }

    async loadStage(stageTag) {
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
            console.error("セリフの読み込みに失敗しました:", error);
            document.getElementById('dialogue-text').innerText = "エラーが発生しました";
        }
    }

    displayNext() {
        console.log("クリックされました！現在のインデックスは:", this.currentIndex);

        if (this.currentIndex < this.dialogues.length) {
            const content = this.dialogues[this.currentIndex];
            document.getElementById('dialogue-text').innerText = content;
            this.currentIndex++;
        } else {
            document.getElementById('dialogue-box').style.display = 'none';
            document.getElementById('next-action').style.display = 'block';
        }
    }
}


const manager = new DialogueManager();

document.addEventListener('click', () => {
    manager.displayNext();
});

// 実行（HTML読み込み完了時に呼ぶ）
window.onload = () => {
    manager.loadStage('prologue');
};