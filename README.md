# Chat Image Generator

会話の CSV ファイルから、チャット形式の画像を生成するプログラムです。

## 必要条件

- Docker

## 使用方法

1. Docker イメージのビルド:

```bash
docker build -t chat-image-generator .
```

2. プログラムを実行:

```bash
docker run -v $(pwd):/app chat-image-generator python generate_image.py [csvファイルのパス]
```

例:

```bash
docker run -v $(pwd):/app chat-image-generator python generate_image.py sample_conversation.csv
```

注意:

- カレントディレクトリがコンテナの `/app` にマウントされます
- CSV ファイルはカレントディレクトリに配置してください
- 生成された画像もカレントディレクトリに出力されます

## CSV ファイルの形式

CSV ファイルは以下の列が必要です：

- speaker: 発言者の名前
- message: 発言内容
- position: メッセージの表示の左右指定

## 出力

- 出力ファイル名: output.png（デフォルト）
- 画像形式: PNG
