# -*- coding: utf-8 -*-
# from odoo import http


# class VideogamesShop(http.Controller):
#     @http.route('/videogames_shop/videogames_shop', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/videogames_shop/videogames_shop/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('videogames_shop.listing', {
#             'root': '/videogames_shop/videogames_shop',
#             'objects': http.request.env['videogames_shop.videogames_shop'].search([]),
#         })

#     @http.route('/videogames_shop/videogames_shop/objects/<model("videogames_shop.videogames_shop"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('videogames_shop.object', {
#             'object': obj
#         })
