# HANDOFF.md — ぷち滝行まっぷ

## プロジェクト概要

ぷち滝行まっぷ — 地図に滝行の足跡を刻む掲示板

## ファイル構成

```
takigiri-bbs/
├── index.html          ← メイン（Leaflet + Firebase SDK）
├── HANDOFF.md          ← このファイル
└── src/
    ├── bbs.py          ← 旧Flask API（削除予定）
    └── bbs.json        ← 旧ローカルデータ（削除予定）
```

## 現在の状態

- GitHub: https://github.com/bonsai/takigiri-bbs
- フロントエンド: Leaflet.js + Firebase Firestore（compat SDK v11.7）
- バックエンド: Flask → **Firebase に移行済み**（Flask不要）
- データ保存: Firestore（リアルタイム同期）
- 認証: Firebase Auth（匿名ログイン）

## Firebase Config（現在 = 差し替え前）

```js
const firebaseConfig = {
  apiKey: "AIzaSyD_FKEbaBGIhNJCBdOFqNE3QhFez1KSfzk",
  authDomain: "takigiri-bbs.firebaseapp.com",
  projectId: "takigiri-bbs",
  storageBucket: "takigiri-bbs.firebasestorage.app",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abcdef123456"
};
```

## やること（Firebase CLIで設定後）

- [ ] 上記 config を実キーに差し替え
- [ ] Firestore セキュリティルール設定（誰でも書き込み可、認証済みのみ削除等）
- [ ] GitHub Pages デプロイ（Settings → Pages → Source: master / root）
- [ ] 動作確認: https://bonsai.github.io/takigiri-bbs/
- [ ] src/ 内の旧Flaskファイルを削除（オプション）

## 手順

1. Firebase Console でプロジェクト作成: `takigiri-bbs`
2. Firestore Database 作成（リージョン: asia-northeast1）
3. Authentication → Anonymous 有効化
4. プロジェクト設定 → Webアプリ追加 → config 取得
5. index.html の firebaseConfig を差し替え
6. `firebase deploy --only hosting` または GitHub Pages デプロイ

## 技術スタック

| 層 | 技術 |
|----|------|
| フレームワーク | なし（Vanilla JS） |
| UI | Leaflet.js + OpenStreetMap |
| DB | Firebase Firestore |
| 認証 | Firebase Auth（匿名） |
| ホスティング | GitHub Pages（予定） |

## 画面構成

- 画面全体: OpenStreetMap（地形マップ）
- ヘッダー: タイトル + 現在地ボタン
- 左下: 投稿一覧（折りたたみ可）
- 右下: 投稿フォーム（名前 + コメント）
- 地図クリック → 位置選択 → 投稿
- ピンクリック → ポップアップ表示
