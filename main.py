import numpy as np
import cv2
import pyautogui as pag
import time
import datetime

# スクショを取る基準
screenShot_rate = 0.05
# 何秒おきにスクショをとるか
sleep_time = 3


def main():
    # 現在のフレーム
    img = ScreenShot()
    SaveScreenShot(img)

    # 最後に保存したフレーム
    old_img = img

    while True:
        img = ScreenShot()

        # 変化量計算
        rate = ImageChangeRate(old_img, img)
        print(rate)

        # 大きな変化があった場合
        if rate > screenShot_rate:
            SaveScreenShot(img)

            # 保存した画像をold_imgに代入
            old_img = img

        time.sleep(sleep_time)


def ImageChangeRate(img1, img2, isShow=False):
    # 画像をグレースケールに変換
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # 2枚の画像の差分を求める
    mdframe = cv2.absdiff(img1, img2, 0.5)
    # 白と黒の2色の画像にする
    thresh = cv2.threshold(mdframe, 10, 255, cv2.THRESH_BINARY)[1]

    # 画像サイズ
    image_size = thresh.size
    # 白のピクセル数／画像サイズ
    whitePixels = cv2.countNonZero(thresh)
    whiteAreaRatio = (whitePixels/image_size)

    # 変化量を1.0~0.0で出力
    return whiteAreaRatio


def ScreenShot():
    # スクリーンショット
    img = pag.screenshot()
    img = img.convert('RGB')
    # pyautoguiの画像をopencvの画像形式に変換
    img = np.array(img)
    img = img[:, :, ::-1].copy()
    return img


def SaveScreenShot(img):
    now = datetime.datetime.now()
    cv2.imwrite("imgs/" + now.strftime('%Y-%m-%d %H.%M.%S') + ".png", img)
    print("Save Screenshot!")


if __name__ == "__main__":
    main()
