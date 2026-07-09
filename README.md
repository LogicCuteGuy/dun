# dun

Tarot-based structured reflection for Claude Code.

[English](#english) · [ภาษาไทย](#ภาษาไทย) · [日本語](#日本語)

---

## English

### What is dun?

Structured reflection with a tarot frame — not prediction, not therapy, but a single session of being heard with real psych grounding.

- Up to **7 grounding probes** before drawing cards (one at a time, with recommended answers)
- Reads from real psych science: CBT distortions, IFS-lite, somatic awareness, window of tolerance
- Deterministic card draw from user's own words (`draw.py`)
- Default 3-card Past / Present / Future spread
- Reads past sessions from `memory/` to pick up threads
- Hard emotional-safety boundaries: crisis > cards, never fabricate, never promise outcomes
- Default mode: **healing** (reflection). Predictive mode only when user explicitly asks.

### Install

```bash
npx skills add your-username/dun
```

### Usage

```
/dun
```

Then answer the questions. The more honest you are, the deeper the reading goes.

### What it is not

- ❌ Not therapy
- ❌ Not prediction
- ❌ Not a chatbot persona

---

## ภาษาไทย

### dun คืออะไร?

สะท้อนตัวเองผ่านไพ่ทาโร่ — ไม่ใช่ทำนาย ไม่ใช่บำบัด แต่เป็นเซสชันเดียวที่ได้ยินตัวเองจริงๆ ด้วยหลักจิตวิทยาที่แข็งแรง

- ถาม **3-7 คำถาม ground** ก่อนจั่วไพ่ (ทีละข้อ พร้อมตัวอย่างคำตอบ)
- ใช้จิตวิทยาจริง: CBT distortions, IFS-lite, somatic awareness, window of tolerance
- สุ่มไพ่จากคำพูดของผู้ใช้ (deterministic — seed เดียวกัน ผลลัพธ์เดียวกัน)
- ไพ่ 3 ใบ: อดีต / ปัจจุบัน / อนาคต
- อ่านเซสชันเก่าจาก `memory/` ต่อเนื่องได้
- กฎเหล็ก: วิกฤต > ไพ่ ห้ามสร้างเรื่อง ห้ามสัญญาผลลัพธ์
- Default: **healing mode** — ทำนายเฉพาะตอนที่ขอ

### ติดตั้ง

```bash
npx skills add your-username/dun
```

### วิธีใช้

```
/dun
```

แล้วตอบคำถาม ยิ่งจริงใจ ยิ่งลึก

### สิ่งที่ dun ไม่ใช่

- ❌ ไม่ใช่บำบัด
- ❌ ไม่ใช่ทำนาย
- ❌ ไม่ใช่แชทบอท

---

## 日本語

### dun って何？

タロットを枠にした構造化的な振り返り — 占いでもセラピーでもなく、心理学に基づいた「听见される」セッション。

- カードを引く前に**3〜7つのグランディング・プローブ**（1つずつ、推奨回答つき）
- 実際の心理学をベースに：CBT歪み、IFS-lite、身体感覚、許容ウィンドウ
- ユーザーの言葉からカードを決定的に引く（`draw.py` — 同じシード = 同じ結果）
- デフォルト3カード：過去 / 現在 / 未来
- `memory/` から過去セッションを読み、スレッドを継続
- 厳格な感情安全ルール：危機 > カード、捏造禁止、結果保証禁止
- デフォルト：**ヒーリングモード** — 予測は明確にリクエストされた場合のみ

### インストール

```bash
npx skills add your-username/dun
```

### 使い方

```
/dun
```

質問に正直に答えてください。正直であればあるほど、リーディングは深くなります。

### dun ではないもの

- ❌ セラピーではない
- ❌ 占いではない
- ❌ チャットボットのペルソナではない
