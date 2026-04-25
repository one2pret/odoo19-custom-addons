from odoo import http
from odoo.addons.web.controllers.home import Home

class CustomHome(Home):

    @http.route('/app', type='http', auth='none')
    def app_redirect(self, **kw):
        return http.redirect_with_hash('/odoo')

    @http.route('/discuss', type='http', auth='user')
    def discuss_shortcut(self, **kw):
        return http.redirect_with_hash('/odoo/discuss')
