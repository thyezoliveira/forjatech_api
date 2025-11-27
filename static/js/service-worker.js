self.addEventListener('push', function(event) {
  const data = event.data.json();
  const options = {
    body: data.body,
    icon: 'static/icon.png', // Opcional: adicione um ícone
    badge: 'static/badge.png' // Opcional: adicione um badge
  };

  event.waitUntil(
    self.registration.showNotification(data.title, options)
  );
});

self.addEventListener('notificationclick', function(event) {
  event.notification.close();
  // Adicione aqui a lógica para abrir uma janela ou focar em uma existente
  // Exemplo:
  // event.waitUntil(
  //   clients.openWindow('https://example.com')
  // );
});