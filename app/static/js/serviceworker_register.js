const sendSubscriptionToServer = async (subscription) => {
    const SERVER_URL = 'api/save-subscription'
    const response = await fetch(SERVER_URL, {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(subscription),
    })
    return response.json()
}

if('serviceWorker' in navigator) {
    // Registering Service Worker
    navigator.serviceWorker.register('/serviceworker.js', { scope: '/' });

    if (!('PushManager' in window)) {
        console.warn('Push messaging isn\'t supported.');
    }
    else {
        navigator.serviceWorker.ready.then((swReg) => {
            // Do we already have a push message subscription?
            swReg.pushManager.getSubscription()
            .then((subscription) => {
                if(!subscription){
                    console.log('No Subscription endpoint present')
                }
                else {
                    alert(subscription);
                    sendSubscriptionToServer(subscription)
                }
            });
        });
    }

    // navigator.serviceWorker.ready.then((swReg) => {
    //     options = {
    //        userVisibleOnly: true,
    //        applicationServerKey: urlB64ToUint8Array(applicationPushPublicKey)
    //        // urlB64ToUint8Array is helper function
    //     }
    //     swReg.pushManager.subscribe(options)
    //     .then(function(subscription) {
    //        // sendSubscriptionToServer function is implemented in Code Snippet 13
    //        return sendSubscriptionToServer(subscription);
    //     })
    // });
}
