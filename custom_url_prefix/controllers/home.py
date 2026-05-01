from odoo import http
from odoo.addons.web.controllers.home import Home


class CustomHome(Home):
    # Daftarkan base-url aplikasi yang ingin dihilangkan "/odoo"-nya di sini
    @http.route(
        [
            "/discuss",
            "/discuss/<path:subpath>",
            "/inventory",
            "/inventory/<path:subpath>",
            "/calendar",
            "/calendar/<path:subpath>",
            "/contacts",
            "/contacts/<path:subpath>",
            "/sales",
            "/sales/<path:subpath>",
            "/apps",
            "/apps/<path:subpath>",
            "/settings",
            "/settings/<path:subpath>",
        ],
        type="http",
        auth="none",
    )
    def custom_app_routes(self, **kw):
        # Langsung load web client, biarkan router JS kita yang menangani sisanya
        return self.web_client(**kw)
