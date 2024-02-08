from odoo import models, fields, api

class Supplier(models.Model):
    _name = 'my_module.supplier'

    name = fields.Char(string='Supplier Name')
    contact_info = fields.Char(string='Contact Information')

class Product(models.Model):
    _name = 'my_module.product'

    name = fields.Char(string='Game Name')
    platform = fields.Selection([('pc', 'PC'), ('console', 'Console')], string='Platform')
    genre = fields.Char(string='Genre')
    available_stock = fields.Integer(string='Available Stock')
    price = fields.Float(string='Price')
    supplier_id = fields.Many2one('my_module.supplier', string='Supplier')

class Customer(models.Model):
    _name = 'my_module.customer'

    name = fields.Char(string='Customer Name')
    contact_info = fields.Char(string='Contact Information')

class Sale(models.Model):
    _name = 'my_module.sale'

    sale_date = fields.Date(string='Sale Date')
    sold_products = fields.Many2many('my_module.product', string='Sold Products')
    customer_id = fields.Many2one('my_module.customer', string='Associated Customer')
    employee_id = fields.Many2one('my_module.employee', string='Associated Employee')
    total_sale = fields.Float(string='Total Sale')

class Employee(models.Model):
    _name = 'my_module.employee'

    name = fields.Char(string='Employee Name')
    position = fields.Char(string='Position')
    contact_info = fields.Char(string='Contact Information')

class ProductReview(models.Model):
    _name = 'my_module.product_review'

    comment = fields.Text(string='Comment')
    rating = fields.Float(string='Rating')
    product_id = fields.Many2one('my_module.product', string='Associated Product')
