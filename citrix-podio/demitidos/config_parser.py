from configparser import ConfigParser


def get_api_keys():
    """Realiza 'parsing' do arquivo ini e retorna tupla com dados para autenticação na api"""
    config = ConfigParser()
    config.read('api_auth.ini')
    client_id = config.get('auth', 'client_id')
    client_secret = config.get('auth', 'client_secret')
    user = config.get('auth', 'user')
    password = config.get('auth', 'password')

    return client_id, client_secret, user, password

if __name__ == '__main__':
    print(get_api_keys())
