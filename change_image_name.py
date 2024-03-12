from PIL import Image
from PIL.ExifTags import TAGS
import os
import shutil
from glob import glob
from collections import defaultdict

## 定数
IN_DIR = "./in/"
OUT_DIR = "./out/"
TMP_DIR = "./tmp/"
LOG_FILE = "log.txt"
EXTENSION_LIST = ["JPG", "JPEG", "PNG", "HEIC"]


def get_exif_data(image):
    '''
    画像ファイルから撮影日時を取得する
    # input 
        image: 画像ファイル[Image object]
    # output
        date: 撮影日時[str]
    '''
    img = Image.open(image)
    exif_info = img._getexif()
    img.close()
    if exif_info == None:
        # with open(LOG_FILE, "a", encoding='utf-8') as f: # ログに追加 
        #     print(f"{image}：exifないよ", file=f)
        date = "no_exif"
    else:
        date_data = exif_info.get(36867)
        if date_data == None:
            # with open(LOG_FILE, "a", encoding='utf-8') as f:
            #     print(f"{image}：撮影日時ないよ", file=f)
            date = "no_date"
        else:
            date = date_data.replace(":", "").replace(" ", "_")
    return date


def init_image_counter(dir: str, extension_list: list[str]):
    '''
    捜査対象フォルダ内の画像ファイルの名前から撮影日時を取得し，同じ日時の写真があるかを確認するための辞書を初期化する．
    # input
        dir: 捜査対象フォルダ[str]
    # output
        image_counter: 画像ファイルの名前から撮影日時を取得し，同じ日時の写真があるかを確認するための辞書[defaultdict(int)]
    '''
    image_counter = defaultdict(int)
    for extension in extension_list:
        img_list = glob(f"{dir}*.{extension}")
        for img in img_list:
            file_name = os.path.basename(img)
            date_data = "_".join(file_name.split(".")[0].split("_")[1:3]) # IMG_YYYYMMDD_HHMMSS.{extension}の形式を想定
            image_counter[date_data] += 1
    return image_counter

def init_name(extension_list: list[str]):
    '''
    画像ファイルの名前を{数字}.{拡張子}のフォーマットで初期化する．
    これをしないと何かがまずい．
    ### input
        extension_list: 対象の拡張子リスト
    '''
    # 作業用フォルダの作成
    if not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR)
    else:
        files = glob(f"{TMP_DIR}*")
        for file in files:
            os.remove(file)
    # 画像ファイルのリストを取得
    cnt = 0
    for extension in extension_list:
        # IN_DIR内の画像ファイルを取得
        img_list = glob(f"{IN_DIR}*.{extension}")
        img_set = set(img_list)
        for img_name in img_list:
            # 改名
            cnt += 1
            initialized_name = str(cnt) + "." + extension
            # 作業用フォルダにコピー
            shutil.copy2(img_name, TMP_DIR + initialized_name)


def change_name(extension_list: list[str]):
    '''
    画像ファイルの名前を{撮影日時}.{拡張子}に変更する．
    同じ日時の写真がある場合は，{撮影日時}_{連番}.{拡張子}に変更する．
    exifデータがなければno_exif.{拡張子}に変更する．
    '''
    # 保存先フォルダの作成
    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)
    # 保存先フォルダのカウンターの初期化
    image_counter = init_image_counter(OUT_DIR, extension_list)
    log_output = []
    for extension in extension_list:
        img_list = glob(f"{TMP_DIR}*.{extension}")
        img_set = set(img_list)
        for img in img_list:
            date_data = get_exif_data(img)
            if image_counter[date_data]: # 同じ日時の写真がすでにある？
                date_data = f"{date_data}_{image_counter[date_data]}"
            image_counter[date_data] += 1
            out_name = "IMG_" + date_data + "." + extension
            shutil.move(img, OUT_DIR + out_name)


init_name(EXTENSION_LIST)
change_name(EXTENSION_LIST)
os.removedirs(TMP_DIR) # 作業用フォルダの削除