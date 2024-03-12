# change_image_name
## つかいかた（.exe）
- "./in/"に名前を変更したいファイルを移動する
	- 変更対象のファイル拡張子は（jpg, jpeg, png, heic）
- exeファイルをダブルクリックで実行
- "./out/"に変更されたファイルが作成される
	- "./out/"ディレクトリは自動生成されるので，作る必要はない

## つかいかた（.py）
- pip install -r requirements.txt
- python change_image_name.py

## 各種パラメータ
- IN_DIR：捜査対象のディレクトリ（デフォルト：./in/）
- OUT_DIR：保存先のディレクトリ（デフォルト：./out/）
- EXTENSION_LIST：変更対象のファイル拡張子は（デフォルト：jpg, jpeg, png, heic）
