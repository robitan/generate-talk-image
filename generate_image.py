import os
import argparse
from PIL import Image, ImageDraw, ImageFont
import pandas as pd


FONT_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"


def create_chat_bubble(draw, text, position, is_right=False, max_width=300):
    # フォントとテキストの設定
    if not os.path.exists(FONT_PATH):
        print(f"Error: Font file not found at {FONT_PATH}")
        exit(1)

    font = ImageFont.truetype(FONT_PATH, 16)

    padding = 10
    line_spacing = 5

    # テキストを折り返す
    words = text
    lines = []
    current_line = ""
    for char in words:
        test_line = current_line + char
        bbox = font.getbbox(test_line)
        if bbox[2] - bbox[0] > max_width:
            lines.append(current_line)
            current_line = char
        else:
            current_line = test_line
    if current_line:
        lines.append(current_line)

    # バブルのサイズを計算
    line_heights = [font.getbbox(line)[3] - font.getbbox(line)[1]
                    for line in lines]
    bubble_height = sum(line_heights) + (len(lines) - 1) * \
        line_spacing + 2 * padding
    bubble_width = max([font.getbbox(line)[2] - font.getbbox(line)[0]
                       for line in lines]) + 2 * padding

    # バブルの位置を調整
    x, y = position
    if is_right:
        x = x - bubble_width

    # チャットバブルを描画
    bubble_shape = [
        (x, y),
        (x + bubble_width, y),
        (x + bubble_width, y + bubble_height),
        (x, y + bubble_height)
    ]
    bubble_color = "#D9EED6" if is_right else "#D9D6EE"
    draw.polygon(bubble_shape, fill=bubble_color)

    # テキストを描画
    current_y = y + padding
    for line in lines:
        bbox = font.getbbox(line)
        text_width = bbox[2] - bbox[0]
        text_x = x + padding if not is_right else x + bubble_width - text_width - padding
        draw.text((text_x, current_y), line, font=font, fill="black")
        current_y += line_heights[0] + line_spacing

    return bubble_height


def generate_chat_image(csv_path, output_path="output.png"):
    # CSVを読み込む
    df = pd.read_csv(csv_path)

    # 画像サイズを設定
    width = 600
    height = len(df) * 100 + 100  # メッセージごとに100ピクセル + 余白

    # 新しい画像を作成
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    # 各メッセージを描画
    current_y = 20
    for _, row in df.iterrows():
        is_right = row['position'] == 'right'  # 位置情報に基づいてメッセージを配置
        x = 500 if is_right else 50  # 右側か左側かで位置を調整

        # メッセージを描画
        bubble_height = create_chat_bubble(
            draw, row['message'], (x, current_y), is_right)

        # 名前を描画
        name_font = ImageFont.truetype(FONT_PATH, 12)
        name_x = 500 if is_right else 50
        name_y = current_y - 15
        draw.text((name_x, name_y), row['speaker'],
                  font=name_font, fill="#666666")

        current_y += bubble_height + 30

    # 画像を保存
    image.save(output_path)
    print(f"Chat image has been generated: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate chat image from CSV file.')
    parser.add_argument(
        'csv_path', help='Path to the CSV file containing conversation data')
    args = parser.parse_args()

    if not os.path.exists(args.csv_path):
        print(f"Error: {args.csv_path} not found")
        exit(1)

    generate_chat_image(args.csv_path)
