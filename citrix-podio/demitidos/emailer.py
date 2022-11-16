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

def email_sender(destinatario, nome_superior, nome_demitido, dt_demissao, modelo_equipamento, patrimonio_equipamento):
    # Create a preferably long-lived app instance which maintains a token cache.
    app = msal.PublicClientApplication(
        client_id=APPLICATION_ID,
        authority=authority_url
        # token_cache=...  # Default cache is in memory only.
        # You can learn how to use SerializableTokenCache from
        # https://msal-python.rtfd.io/en/latest/#msal.SerializableTokenCache
    )

    # The pattern to acquire a token looks like this.
    result = None

    # Firstly, check the cache to see if this end user has signed in before
    accounts = app.get_accounts(username='clnine@outlook.com')
    if accounts:
        logging.info("Account(s) exists in cache, probably with token too. Let's try.")
        print("Account(s) already signed in:")
        for a in accounts:
            print(a["username"])
        chosen = accounts[0]  # Assuming the end user chose this one to proceed
        print("Proceed with account: %s" % chosen["username"])
        # Now let's try to find a token in cache for this account
        result = app.acquire_token_silent(scopes=['Mail.Send'], account=chosen)

    if not result:
        logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
        print("A local browser window will be open for you to sign in. CTRL+C to cancel.")
        result = app.acquire_token_interactive(
            # Only works if your app is registered with redirect_uri as http://localhost
            scopes=['Mail.Send'],
            # parent_window_handle=...,  # If broker is enabled, you will be guided to provide a window handle
            login_hint='clnine@outlook.com',  # Optional.
            # If you know the username ahead of time, this parameter can pre-fill
            # the username (or email address) field of the sign-in page for the user,
            # Often, apps use this parameter during reauthentication,
            # after already extracting the username from an earlier sign-in
            # by using the preferred_username claim from returned id_token_claims.

            # prompt=msal.Prompt.SELECT_ACCOUNT,  # Or simply "select_account". Optional. It forces to show account selector page
            # prompt=msal.Prompt.CREATE,  # Or simply "create". Optional. It brings user to a self-service sign-up flow.
            # Prerequisite: https://docs.microsoft.com/en-us/azure/active-directory/external-identities/self-service-sign-up-user-flow
        )

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
        graph_response = requests.post('https://graph.microsoft.com/v1.0/me/sendMail',
                                       headers={'Authorization': 'Bearer ' + result['access_token']}, json=request_body)

        print(graph_response.text)
        # graph_response = requests.get(  # Use token to call downstream service
        #     'https://graph.microsoft.com/v1.0/me/onenote/notebooks',
        #     headers={'Authorization': 'Bearer ' + result['access_token']},)
        # print(graph_response.text)
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
