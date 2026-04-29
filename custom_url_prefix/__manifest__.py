{
    'name': 'Custom URL Prefix',
    'version': '19.0.1.0.0',
    'summary': 'URL alias tanpa prefix /odoo',
    'depends': ['web'],
    'assets': {
        'web.assets_backend': [
            'custom_url_prefix/static/src/js/custom_router.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'author': 'Wawan',
    'website' : 'mochwawankurnia@gmail.com',
}
