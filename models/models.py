from odoo import models, fields, api, exceptions
import re
import secrets
import logging
from datetime import date
from odoo.exceptions import ValidationError



_logger = logging.getLogger(__name__)  

class Supplier(models.Model):
    _name = 'videogames_shop.supplier'

    name = fields.Char(string='Supplier Name')
    image = fields.Binary(string='Image')
    nss = fields.Char(string='NSS')
    contact_info = fields.Char(string='Contact Information')
    product_ids = fields.One2many('videogames_shop.product', 'supplier_id', string='Products')
    product_count = fields.Integer(string='Product Count', compute='_compute_product_count')

    @api.depends('product_ids')
    def _compute_product_count(self):
        for record in self:
            record.product_count = len(record.product_ids)

    @api.constrains('nss')
    def _check_nss(self):
        pattern = r'^\d{12}$' 
        for record in self:
            if not re.match(pattern, record.nss):
                raise exceptions.ValidationError('The NSS must be in the format XXX-XX-XXXX.')

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
    password = fields.Char(string='Password', default=lambda self: self._get_password(), readonly=True, store=True)
    date_joined = fields.Date(string='Date Joined', default=fields.Date.today)
    purchase_ids = fields.One2many('videogames_shop.sale', 'customer_id', string='Purchases')
    purchase_count = fields.Integer(string='Purchase Count', compute='_compute_purchase_count')
    image = fields.Binary(string='Image', attachment=True)

    def _get_password(self):
        password = secrets.token_urlsafe(12)
        _logger.error("Customer: "+str(self.name)+" Password: " + str(password))
        return password

    @api.depends('purchase_ids')
    def _compute_purchase_count(self):
        for record in self:
            record.purchase_count = len(record.purchase_ids)

    def regenerate_password(self):
        for record in self:
            record.password = self._get_password()

class Sale(models.Model):
    _name = 'videogames_shop.sale'

    id_name = fields.Char(string='Sale Identifier', readonly=True)
    sale_date = fields.Date(string='Sale Date')
    sold_products = fields.Many2many('videogames_shop.product', string='Sold Products')
    customer_id = fields.Many2one('videogames_shop.customer', string='Associated Customer')
    employee_id = fields.Many2one('videogames_shop.employee', string='Associated Employee')
    total_sale = fields.Float(string='Total Sale')

    @api.model
    def create(self, vals):
        record = super(Sale, self).create(vals)
        record.id_name = 'Sale {}'.format(record.id)
        return record

class Employee(models.Model):
    _name = 'videogames_shop.employee'

    name = fields.Char(string='Employee Name')
    position = fields.Char(string='Position')
    contact_info = fields.Char(string='Contact Information')
    image = fields.Binary(string='Image', attachment=True)
    join_date = fields.Date(string='Join Date')
    salary = fields.Float(string='Salary', compute='_compute_salary')

    @api.depends('join_date')
    def _compute_salary(self):
        for record in self:
            base_salary = 1100  
            if record.join_date:
                years_of_service = (date.today() - record.join_date).days // 365
                record.salary = base_salary + (base_salary * years_of_service * 0.05)  
            else:
                record.salary = base_salary

class ProductReview(models.Model):
    _name = 'videogames_shop.product_review'

    review_name = fields.Char(string='Review Name', readonly=True)
    comment = fields.Text(string='Comment')
    rating = fields.Float(string='Rating')
    product_id = fields.Many2one('videogames_shop.product', string='Associated Product')
    review_date = fields.Date(string='Review Date', default=fields.Date.today)
    reviewer_name = fields.Char(string='Reviewer Name')
    is_approved = fields.Boolean(string='Is Approved', default=False)

    @api.model
    def create(self, vals):
        # Check if the rating is within a valid range
        if 'rating' in vals and not 1 <= vals['rating'] <= 5:
            raise ValidationError("Rating must be between 1 and 5.")
        
        # Generate a unique review name
        vals['review_name'] = 'Review {}'.format(self.env['ir.sequence'].next_by_code('videogames_shop.product_review'))
        
        return super(ProductReview, self).create(vals)

    def approve_review(self):
        # This function can be called to approve a review
        self.is_approved = True
    
