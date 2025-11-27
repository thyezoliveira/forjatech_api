const VAPID_PUBLIC_KEY = 'Ne7DAygbOlnBYY4E3jT9nHSpoSNS5XFa1UIFsTd1wgXaGKhU5oBfFriCrpYJ0vBhKrATBAqFWqUIGF_3XAFFkQ'; // Substitua pela sua chave pública VAPID

function urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
}

async function subscribeUser() {
    try {
        const registration = await navigator.serviceWorker.ready;
        const subscription = await registration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC_KEY)
        });

        console.log('User is subscribed:', subscription);

        await fetch('/api/save-subscription', {
            method: 'POST',
            body: JSON.stringify(subscription),
            headers: {
                'Content-Type': 'application/json'
            }
        });

        console.log('Subscription sent to server.');

    } catch (error) {
        console.error('Failed to subscribe the user: ', error);
    }
}

async function initSW() {
    if ('serviceWorker' in navigator && 'PushManager' in window) {
        try {
            const registration = await navigator.serviceWorker.register('/static/js/service-worker.js');
            console.log('Service Worker registered with scope:', registration.scope);

            // Verifica se o usuário já concedeu permissão
            if (Notification.permission === 'granted') {
                console.log('Permission for notifications was already granted');
                subscribeUser();
            } else if (Notification.permission !== 'denied') {
                // Solicita a permissão
                const permission = await Notification.requestPermission();
                if (permission === 'granted') {
                    console.log('Permission for notifications was granted');
                    subscribeUser();
                }
            }
        } catch (error) {
            console.error('Service Worker registration failed:', error);
        }
    } else {
        console.warn('Push messaging is not supported');
    }
}

initSW();
