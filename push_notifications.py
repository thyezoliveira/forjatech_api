import os
import json
from pywebpush import webpush, WebPushException

VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY")
VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY")
VAPID_CLAIMS = {
    "sub": "mailto:thyezoliveira.homeoffice@gmail.com"
}

SUBSCRIPTIONS_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/subscriptions.json')
def get_all_subscriptions():
    """
    Carrega todas as inscrições de um arquivo.
    """
    if not os.path.exists(SUBSCRIPTIONS_FILE):
        return []
    with open(SUBSCRIPTIONS_FILE, "r") as f:
        return json.load(f)

def save_subscription(subscription):
    """
    Salva uma nova inscrição no arquivo.
    """
    subscriptions = get_all_subscriptions()
    subscriptions.append(subscription)
    with open(SUBSCRIPTIONS_FILE, "w") as f:
        json.dump(subscriptions, f)

def send_push_notification(subscription_info, message_body):
    """
    Envia uma notificação push para uma única inscrição.
    """
    if not all([VAPID_PRIVATE_KEY, VAPID_PUBLIC_KEY]):
        print("As chaves VAPID não estão configuradas. A notificação não será enviada.")
        return

    try:
        webpush(
            subscription_info=subscription_info,
            data=message_body,
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims=VAPID_CLAIMS
        )
        print("Notificação enviada com sucesso.")
    except WebPushException as ex:
        print(f"Erro ao enviar notificação: {ex}")
        # Se a inscrição for inválida, pode ser uma boa ideia removê-la
        if ex.response and ex.response.status_code in [404, 410]:
            print("Inscrição inválida ou expirada, removendo.")
            _remove_subscription(subscription_info)

def send_notification_to_all(message):
    """
    Envia uma notificação para todas as inscrições salvas.
    """
    subscriptions = get_all_subscriptions()
    for sub in subscriptions:
        send_push_notification(sub, message)

def _remove_subscription(subscription_to_remove):
    """
    Remove uma inscrição do arquivo.
    """
    subscriptions = get_all_subscriptions()
    updated_subscriptions = [sub for sub in subscriptions if sub['endpoint'] != subscription_to_remove['endpoint']]
    with open(SUBSCRIPTIONS_FILE, "w") as f:
        json.dump(updated_subscriptions, f)
