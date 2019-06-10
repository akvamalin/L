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
        print(update)
        if update.effective_user.id == user_id:
            return update.message.chat_id

    raise EnvironmentError('Chat with a user {} not found. Ensure user has subscribed to the bot'.format(user_id))


def handler(event, context):
    ensure_env_set(env_vars)

    env_imap_server = environ.get(env_vars['imap_server'])
    env_user_name = environ.get(env_vars['user'])
    env_user_password = environ.get(env_vars['pass'])
    env_user_id = int(environ.get(env_vars['user_id']))
    env_telegram_token = environ.get(env_vars['token'])

    with IMAPClient(env_imap_server, use_uid=True) as client:
        client.login(env_user_name, env_user_password)
        client.select_folder('INBOX')
        print(f'Login for {env_user_name} is successful.')

        unread_messages = client.search([u'UNSEEN'])

        print(f'{len(unread_messages)} unread messages found.')

        bot = Bot(token=env_telegram_token)
        bot_info = bot.get_me()
        print(f'Started bot {bot_info.id} {bot_info.username}')

        chat_id = resolve_chat_id_for_user(env_user_id, bot.get_updates())
        bot.send_message(chat_id = chat_id, text = "{} unread messages found.".format(len(unread_messages)))

        print('Done.')



