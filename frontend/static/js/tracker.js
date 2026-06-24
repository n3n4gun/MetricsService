(function() {
    'use strict';

    function sendData(data) {
        fetch('/api/collect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                console.warn('Tracker: ошибка отправки данных', response.status);
            }
        })
        .catch(err => {
            console.warn('Tracker: ошибка сети', err);
        });
    }

    function collectPageData() {
        const data = {
            event_type: 'page_view',
            url: window.location.href,
            path: window.location.pathname,
            title: document.title,
            referrer: document.referrer || 'direct',
            screen_width: window.screen.width,
            screen_height: window.screen.height,
            user_agent: navigator.userAgent,
            timestamp: new Date().toISOString()
        };
        sendData(data);
    }

    function setupClickTracking() {
        document.addEventListener('click', function(event) {
            const target = event.target;
            const data = {
                event_type: 'click',
                target: target.tagName,
                target_text: target.textContent?.trim() || '',
                target_id: target.id || '',
                target_class: target.className || '',
                url: window.location.href,
                timestamp: new Date().toISOString()
            };
            sendData(data);
        });
    }

    if (document.readyState === 'complete') {
        collectPageData();
    } else {
        window.addEventListener('load', collectPageData);
    }

    setupClickTracking();

    console.log('📊 Tracker initialized for:', window.location.pathname);

})();
