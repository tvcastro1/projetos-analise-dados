import webbrowser

import msal
import logging
import requests
import json
from msal import PublicClientApplication

APPLICATION_ID = '31a4641c-9cae-4d30-a2d4-c104bf383785'
CLIENT_SECRET = '5M78Q~QVl-rib2HqHVJ4xhRe-XWcGySwtZMgPbjz'
authority_url = 'https://login.microsoftonline.com/common/'

base_url = 'https://graph.microsoft.com/v1.0/'
endpoint = base_url + 'me'
SCOPES = ['User.Read', 'User.Export.All']


#
# # method 2: Login to acquire access_token
#
# client = PublicClientApplication(client_id=APPLICATION_ID,
#                               authority=authority_url)
#
# flow = client.initiate_device_flow(scopes=SCOPES)
# print(flow['user_code'])
# webbrowser.open(flow['verification_uri'])
#
# token_response = client.acquire_token_by_device_flow(flow)
# print(token_response['access_token'])

def email_sender(destinatario, nome_superior=None, nome_demitido=None, dt_demissao=None, modelo_equipamento=None, patrimonio_equipamento=None):
    f = open('parameters.json')
    config = json.load(f)
    app = msal.ConfidentialClientApplication(
        config["client_id"], authority=config["authority"],
        client_credential=config["secret"],
        # token_cache=...  # Default cache is in memory only.
        # You can learn how to use SerializableTokenCache from
        # https://msal-python.rtfd.io/en/latest/#msal.SerializableTokenCache
    )

    # The pattern to acquire a token looks like this.
    result = None

    # Firstly, looks up a token from cache
    # Since we are looking for token for the current app, NOT for an end user,
    # notice we give account parameter as None.
    result = app.acquire_token_silent(config["scope"], account=None)

    if not result:
        logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
        result = app.acquire_token_for_client(scopes=config["scope"])
    if "access_token" in result:
        # Calling graph using the access token
        request_body = {
            'message': {
                # recipient list
                'toRecipients': [
                    {
                        'emailAddress': {
                            'address': f'{destinatario}'
                        }
                    }
                ],
                # email subject
                'subject': 'TESTE - Transferência de Equipamentos',
                'importance': 'normal',
                'body': {
                    'contentType': 'HTML',
                    'content': f'<b>Prezado {nome_superior}, \n ex-colaborador:{nome_demitido} desligado em '
                               f'{dt_demissao}, favor 'f'transferir equipamento{modelo_equipamento},'
                               f' patrimônio {patrimonio_equipamento}'f' para outro colaborador ativo</b>'
                },

            }
        }
        graph_response = requests.post(config['endpoint'],
                                       headers={'Authorization': 'Bearer ' + result['access_token']}, json=request_body)
        print("Graph API call result: ")
        print(graph_response)
    else:
        print(result.get("error"))
        print(result.get("error_description"))
        print(result.get("correlation_id"))  # You may need this when reporting a bug


# request_body = {
#     'message': {
#         # recipient list
#         'toRecipients': [
#             {
#                 'emailAddress': {
#                     'address': '<recipient email address>'
#                 }
#             }
#         ],
#         # email subject
#         'subject': 'You got an email',
#         'importance': 'normal',
#         'body': {
#             'contentType': 'HTML',
#             'content': '<b>Be Awesome</b>'
#         },
#         # include attachments
#         'attachments': [
#             draft_attachment('hello.txt'),
#             draft_attachment('image.png')
#         ]
#     }
# }


if __name__ == '__main__':
    email_sender('thiagovieirac@gmail.com')
