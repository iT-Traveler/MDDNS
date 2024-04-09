import authomatic
from authomatic.providers import oauth2, oauth1

CONFIG = {
    'github': {
        'class_': oauth2.GitHub,
        'consumer_key': '4e9f3fbb48361dba8271',
        'consumer_secret': '797be89da3c8b859e00cce0e35628c5175191773',
        'access_headers': {'User-Agent': 'Awesome-Octocat-App'},
        'scope': oauth2.GitHub.user_info_scope + ['user:email'],
    }
}
