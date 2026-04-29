/** @odoo-module **/
import { router } from "@web/core/browser/router";

// 1. Modifikasi cara Odoo menghasilkan URL saat pindah menu
const originalStateToUrl = router.stateToUrl;
router.stateToUrl = function (state) {
    let url = originalStateToUrl(state);
    // Hapus '/odoo' dari awal URL yang di-generate
    if (url && url.startsWith('/odoo/')) {
        url = '/' + url.substring(6);
    } else if (url === '/odoo') {
        url = '/';
    }
    return url;
};

// 2. Modifikasi cara Odoo membaca URL dari Address Bar
const originalUrlToState = router.urlToState;
router.urlToState = function (urlObj) {
    const pathname = urlObj.pathname;
    
    // Kita biarkan URL standar bawaan odoo atau url asset tidak tersentuh
    const isStandard = pathname.startsWith('/odoo') || 
                       pathname.startsWith('/web') || 
                       pathname.startsWith('/scoped_app') ||
                       pathname.startsWith('/@') || // OWL/Vite dev server
                       pathname.startsWith('/session');
    
    let simulatedUrlObj = urlObj;
    if (!isStandard && pathname !== '/') {
        // Asumsikan ini adalah nama aplikasi langsung seperti /discuss
        // Tambahkan "/odoo" secara 'gaib' agar router internal Owl paham
        const newUrl = new URL(urlObj.href);
        newUrl.pathname = '/odoo' + pathname;
        simulatedUrlObj = newUrl;
    }
    
    return originalUrlToState(simulatedUrlObj);
};
