from odoo import models, fields, api

class Supplier(models.Model):
    _name = 'videogames_shop.supplier'

    name = fields.Char(string='Supplier Name')
    contact_info = fields.Char(string='Contact Information')

class Product(models.Model):
    _name = 'videogames_shop.product'

    name = fields.Char(string='Game Name')
    image = fields.Binary(string='Image')
    platform = fields.Selection([('pc', 'PC'), ('console', 'Console')], string='Platform')
    genre = fields.Selection([('action', 'Action'), ('adventure', 'Adventure'), ('rpg', 'RPG'), ('strategy', 'Strategy')], string='Genre')
    available_stock = fields.Integer(string='Available Stock')
    price = fields.Float(string='Price')
    supplier_id = fields.Many2one('videogames_shop.supplier', string='Supplier')
    reserved_stock = fields.Integer(string='Reserved Stock')
    total_stock = fields.Integer(string='Total Stock', compute='_compute_total_stock', store=True, readonly=True)

    @api.depends('available_stock', 'reserved_stock')
    def _compute_total_stock(self):
        for record in self:
            record.total_stock = record.available_stock - record.reserved_stock
    
   
class Customer(models.Model):
    _name = 'videogames_shop.customer'

    name = fields.Char(string='Customer Name')
    contact_info = fields.Char(string='Contact Information')

class Sale(models.Model):
    _name = 'videogames_shop.sale'

    sale_date = fields.Date(string='Sale Date')
    sold_products = fields.Many2many('videogames_shop.product', string='Sold Products')
    customer_id = fields.Many2one('videogames_shop.customer', string='Associated Customer')
    employee_id = fields.Many2one('videogames_shop.employee', string='Associated Employee')
    total_sale = fields.Float(string='Total Sale')

class Employee(models.Model):
    _name = 'videogames_shop.employee'

    name = fields.Char(string='Employee Name')
    position = fields.Char(string='Position')
    contact_info = fields.Char(string='Contact Information')

class ProductReview(models.Model):
    _name = 'videogames_shop.product_review'

    comment = fields.Text(string='Comment')
    rating = fields.Float(string='Rating')
    product_id = fields.Many2one('videogames_shop.product', string='Associated Product')
    
