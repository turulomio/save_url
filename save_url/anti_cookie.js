(() => {
    try {
        // 1. Trigger CMP consent APIs
        try {
            if (window.Didomi && typeof window.Didomi.setUserAgreeToAll === 'function') {
                window.Didomi.setUserAgreeToAll();
            }
            if (window.OneTrust && typeof window.OneTrust.AllowAll === 'function') {
                window.OneTrust.AllowAll();
            }
        } catch (e) {}

        // 2. Click specific consent accept buttons
        const acceptButtons = [
            '#didomi-notice-agree-button',
            '#onetrust-accept-btn-handler',
            '#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll',
            '.fc-cta-consent',
            '.fc-primary-button',
            '#accept-cookies',
            '#accept-cookie',
            '.accept-cookies-button'
        ];
        for (const sel of acceptButtons) {
            const btn = document.querySelector(sel);
            if (btn && typeof btn.click === 'function') {
                btn.click();
            }
        }

        // 3. Remove only specific known CMP banner root elements
        const bannerRoots = [
            '#didomi-host',
            '#didomi-notice',
            '#didomi-popup',
            '.didomi-popup-container',
            '.didomi-popup-backdrop',
            '#onetrust-consent-sdk',
            '#onetrust-banner-sdk',
            '.onetrust-pc-dark-filter',
            '#onetrust-pc-sdk',
            '#CybotCookiebotDialog',
            '#CybotCookiebotDialogBodyUnderlay',
            '#qc-cmp2-container',
            'div[id^="sp_message_container_"]',
            '.sp_message_container',
            '.fc-consent-root',
            '#usercentrics-root',
            '#cmpbox',
            '#cmpbox2',
            '#cookie-law-info-bar',
            '#cookie-law-info-again'
        ];
        for (const sel of bannerRoots) {
            document.querySelectorAll(sel).forEach(el => {
                try { el.remove(); } catch (e) {}
            });
        }

        // 4. Restore scroll lock
        document.documentElement.style.overflow = 'auto';
        document.body.style.overflow = 'auto';
        document.documentElement.style.position = 'static';
        document.body.style.position = 'static';

        ['no-scroll', 'modal-open', 'didomi-popup-open', 'sp-message-open'].forEach(cls => {
            document.documentElement.classList.remove(cls);
            document.body.classList.remove(cls);
        });
    } catch (err) {}
})();
