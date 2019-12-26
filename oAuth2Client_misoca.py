#####################################################################
##oauth2_clientを使ってMisoca(ミソカ) APIを使うサンプル
#####################################################################

#oauth2_client本家のサンプルを元に作成
#https://pypi.org/project/oauth2-client/


#以下のサンプルは、ブラウザーでアクセスして承認ボタンを押すタイプ
#前提条件として、misocaにログインしてアプリの設定をしていること
from logging import getLogger, StreamHandler, Formatter
from oauth2_client.credentials_manager import CredentialManager, ServiceInformation

#スコープの設定
scopes = ['read', 'write']
service_information = ServiceInformation('https://app.misoca.jp/oauth2/authorize', #authorizeのULR
                                         'https://app.misoca.jp/oauth2/token',#tokenのULR
                                         'アプリケーションIDを設定すること',
                                         'シークレットIDを設定すること',
                                         scopes)
manager = CredentialManager(service_information)

#リダイレクトURLを設定する
redirect_uri = 'http://0.0.0.0:5001/callback_misoca'
url = manager.init_authorize_code_process(redirect_uri, 'state_test')

#ここでブラウザを開いて、コンソールに表示されたURLをブラウザーに入力する
print('Open this url in your browser\n%s'% url)
code = manager.wait_and_terminate_authorize_code_process()



print('Code got = %s' %  code)
manager.init_with_authorize_code(redirect_uri, code)

#ここでTokenをゲットできている
print('Access got = [%s]' %  manager._access_token)

#contactsにアクセスして取引先（送り先）一覧を取得する
#他にもpostメソッドを使う場合は、manager.postなどの処理がある
response = manager.get("https://app.misoca.jp/api/v3/contacts")
print(response.text)
