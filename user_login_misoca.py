#####################################################################
##loginidとパスワードを使ってMisoca(ミソカ) APIを使うサンプル
#####################################################################


from logging import getLogger, StreamHandler, Formatter
from oauth2_client.credentials_manager import CredentialManager, ServiceInformation
import urllib.request


scopes = ['read', 'write']

service_information = ServiceInformation('https://app.misoca.jp/oauth2/authorize',#authorizeのULR
                                         'https://app.misoca.jp/oauth2/token',#tokenのULR
                                         'アプリケーションIDを設定すること',
                                         'シークレットIDを設定すること',
                                         scopes)
manager = CredentialManager(service_information)

manager.init_with_user_credentials('login idを設定', 'パスワードを設定')
print('Access got = %s' %  manager._access_token)
# Here access and refresh token may be used

response = manager.get("https://app.misoca.jp/api/v3/contacts")
print(response.text)


