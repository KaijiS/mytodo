# mytodo
プログラム課題
## 使用した技術要素
言語:python  
フレームワーク:Django  
データベース:SQLite(Djangoの初期設定)  

検索時：jQueryによるAjax

## 全体の設計・構成
*構成*  
mytodo(プロジェクト名)  
　　|-cms(アプリ名)  
　　|　　|--template(HTMLなど表示周り)  
　　|　　|--他(内部の実装)  
　　|  
　　|-mytodo(プロジェクトの設定)  
　　|  
　　|-static(BootstrapやjQuery,背景画像)  

*データベース設計*  
テーブル名:ToDoList(属性:ID,ToDoリスト名)  
テーブル名:ToDo(属性:ID,ToDoList(外部キー),ToDo名,締切日,作成日,完了/末完了)  

*動作確認*  
開発用サーバの起動
`$ python3 manage.py runserver`  
アクセス先：http://127.0.0.1:8000/cms/ToDoList/

## 環境開発のセットアップ手順
1. python3のインストール
2. pip3を用いて"numpy"及び"Django"をインストール
3. プロジェクトの作成($ django-admin.py startproject プロジェクト名)
4. データベースのセットアップ($ python3 manage.py migrate)
5. スーパーユーザの作成($ python3 manage.py createsuperuser)
6. 開発用サーバの起動($ python3 manage.py runserver)(確認アクセス先：http://127.0.0.1:8000/)
7. アプリケーションの作成($ python3 manage.py startapp アプリ名)

*データベース(model.py)の変更があった時*  
    $ python3 manage.py makemigrations アプリ名  
    $ python3 manage.py sqlmigrate アプリ名 0001  
    $ python3 manage.py migrate  

*HTML周り*
* "Bootstrap"及び"jQuery"をダウンロード
