# mytodo
プログラム課題
## 使用した技術要素
言語:Python3  
フレームワーク:Django  
データベース:SQLite(Djangoの初期設定)  

検索時：jQueryによるAjax  
類似語による検索時：MeCabによる形態素解析、WordNetを用いた単語間の類似度(シソーラス距離)の算出

## 全体の設計・構成
**ファイル構成**   
mytodo(プロジェクト名)  
　　|-cms(アプリ名)  
　　|　　|--template(HTMLなど表示周り)  
　　|　　|--他(内部の実装)  
　　|  
　　|-mytodo(プロジェクトの設定)  
　　|  
　　|-static(BootstrapやjQuery,背景画像)  

**データベース設計**  
テーブル名:ToDoList(属性:ID,ToDoリスト名)  
テーブル名:ToDo(属性:ID,ToDoList(外部キー),ToDo名,締切日,作成日,完了/末完了)  

**機能**
* ToDoリストの追加・編集・削除
* ToDoの追加・編集・削除
* ToDoの締め切り日がどのくらい近いかの自動変色
* 締め切りが近い順にToDoをソートし表示
* ToDoリスト名及びToDo名の検索機能
* 類似語によるToDoリスト名及びToDo名の検索機能(台所:キッチン, 勉強:学習 等)

**動作確認**  
*確認環境*
* OS: macOS Sierra バージョン 10.12.6
* ブラウザ: Google Chrome
* 言語: Python3.6.2
* 以下の必要ライブラリ

*必要ライブラリのインストール方法*  
    `$ pip3 install django`  
    `$ pip3 install numpy`  
    `$ brew install mecab` (macOSの方法)  
    `$ brew install mecab-ipadic` (macOSの方法)  
    `$ pip3 install mecab-python3`  
    `$ pip3 install nltk`  
    `$ pip3 install django-bootstrap-form`  

*開発用サーバの起動*  
`$ python3 manage.py runserver`  
アクセス先：http://127.0.0.1:8000/cms/ToDoList/

## 環境開発のセットアップ手順
1. Python3のインストール
2. pip3を用いてフレームワークの"Django"及び,その他"numpy","nltk","MeCab"及び"django-bootstrap-form"を上記のようにインストール
3. プロジェクトの作成  
`$ django-admin.py startproject プロジェクト名`
4. データベースのセットアップ  
`$ python3 manage.py migrate`
5. スーパーユーザの作成  
`$ python3 manage.py createsuperuser`
6. 開発用サーバの起動  
`$ python3 manage.py runserver`(確認アクセス先：http://127.0.0.1:8000/)
7. アプリケーションの作成  
`$ python3 manage.py startapp アプリ名`

**データベース(model.py)の変更があった時**  
    `$ python3 manage.py makemigrations アプリ名`  
    `$ python3 manage.py sqlmigrate アプリ名 0001`  
    `$ python3 manage.py migrate`  

**HTML周り**
* "Bootstrap"及び"jQuery"をダウンロード
