import os
import numpy as np
import cv2
import pyautogui as pag
import time
import datetime

# 画像変化のしきい値（大きな変化があったとみなす割合）
change_threshold = 0.05
# スクリーンショットを取る間隔（秒）
screenshot_interval = 6

def main():
    # 初期フレームをキャプチャ
    current_image = capture_screenshot()
    save_screenshot(current_image)

    # 最後に保存したフレームを保持
    last_saved_image = current_image

    while True:
        current_image = capture_screenshot()

        # 画像の変化量を計算
        change_rate = calculate_change_rate(last_saved_image, current_image)
        print(change_rate)

        # しきい値以上の変化があった場合、スクリーンショットを保存
        if change_rate > change_threshold:
            save_screenshot(current_image)
            last_saved_image = current_image

        time.sleep(screenshot_interval)

def calculate_change_rate(image1, image2):
    # 画像をグレースケールに変換
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # 画像の差分を計算
    diff_image = cv2.absdiff(gray_image1, gray_image2)
    # 差分画像を二値化
    _, threshold_image = cv2.threshold(diff_image, 10, 255, cv2.THRESH_BINARY)

    # 白のピクセル数と全体のピクセル数から変化量を算出
    white_pixels = cv2.countNonZero(threshold_image)
    total_pixels = threshold_image.size
    change_ratio = white_pixels / total_pixels

    return change_ratio

def capture_screenshot():
    # スクリーンショットを取得してOpenCV形式に変換
    screenshot = pag.screenshot()
    screenshot = np.array(screenshot.convert('RGB'))[:, :, ::-1]
    return screenshot


def save_screenshot(image):
    # スクリーンショットを保存するフォルダのパス
    folder_path = "imgs"
    
    # フォルダが存在しない場合は作成
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # 現在の日時をファイル名に使用してスクリーンショットを保存
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S')
    cv2.imwrite(f"{folder_path}/{timestamp}.png", image)
    print("Screenshot saved!")

if __name__ == "__main__":
    main()
