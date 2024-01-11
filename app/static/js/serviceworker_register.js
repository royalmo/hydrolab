if('serviceWorker' in navigator) {
    // Registering Service Worker
    navigator.serviceWorker.register('/serviceworker.js', { scope: '/' });
}

// (A) OBTAIN USER PERMISSION TO SHOW NOTIFICATION
function enable_notifications() {
    if (event) {
        //event.preventDefault();
        if (!event.target.checked) return;
    }
    // (A1) ASK FOR PERMISSION
    if (Notification.permission === "default") {
    Notification.requestPermission().then(perm => {
        if (Notification.permission === "granted") {
        regWorker().catch(err => console.error(err));
        } else {
        alert("Please allow notifications.");
        }
    });
    }

    // (A2) GRANTED
    else if (Notification.permission === "granted") {
    regWorker().catch(err => console.error(err));
    }

    // (A3) DENIED
    else { alert("Please allow notifications."); }
}

// (B) REGISTER SERVICE WORKER
async function regWorker () {
    // (B1) YOUR PUBLIC KEY - CHANGE TO YOUR OWN!
    const publicKey = "BKnamwulEZy2ioRbctK0aehcQU2WH3j76MVtpt8hXzLvRp-UQKYMLl5IfzGF4u6nAu3beet3amCeWFrESxJLIyE";

    // (B3) SUBSCRIBE TO PUSH SERVER
    navigator.serviceWorker.ready
    .then(reg => {
    reg.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: publicKey
    }).then(
        // (B3-1) OK - TEST PUSH NOTIFICATION
        sub => {
        var data = new FormData();
        data.append("sub", JSON.stringify(sub));
        fetch("/subscribe", { method:"POST", body:data })
        .then(res => res.text())
        .then(txt => console.log(txt))
        .catch(err => console.error(err));
        },

        // (B3-2) ERROR!
        err => console.error(err)
    );
    });
}
