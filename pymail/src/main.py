from imapclient import IMAPClient
from os import environ
from telegram import Bot


env_vars = {
    "imap_server": "IMAP_SERVER",
    "user": "USER",
    "pass": "PASS",
    "user_id": "TELEGRAM_USER_ID",
    "token": "TELEGRAM_TOKEN"
}


def ensure_env_set(vars):
    if type(vars) is not dict:
        raise TypeError("Invalid argument type. It must be of type dictionary")

    for key, value in vars.items():
        if value not in environ:
            raise ValueError('Environmental variable not set. Ensure {} is set.'.format(value))


def resolve_chat_id_for_user(user_id, updates):
    for update in updates:
        if update.effective_user.id == user_id:
            return update.message.chat_id

    raise EnvironmentError('Chat with a user {} not found. Ensure user has subscribed to the bot'.format(user_id))


ensure_env_set(env_vars)

ENV_IMAP_SERVER = environ.get(env_vars['imap_server'])
ENV_USER_NAME = environ.get(env_vars['user'])
ENV_USER_PASSWORD = environ.get(env_vars['pass'])
ENV_USER_ID = int(environ.get(env_vars['user_id']))
ENV_TELEGRAM_TOKEN = environ.get(env_vars['token'])

server = IMAPClient(ENV_IMAP_SERVER, use_uid=True)
server.login(ENV_USER_NAME, ENV_USER_PASSWORD)

print(f'Login for {ENV_USER_NAME} is successful.')

unread_messages = server.search([b'NOT', b'DELETED'])

print(f'{len(unread_messages)} unread messages found.')

bot = Bot(token=ENV_TELEGRAM_TOKEN)
bot_info = bot.get_me()
print(f'Started bot {bot_info.id} {bot_info.username}')

chat_id = resolve_chat_id_for_user(ENV_USER_ID, bot.get_updates())
bot.send_message(chat_id = chat_id, text = "{} unread messages found.".format(len(unread_messages)))

print('Done.')
