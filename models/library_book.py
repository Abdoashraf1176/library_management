from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LibraryBook(models.Model):
    _name = "library.book"

    name = fields.Char(required=True)
    isbn = fields.Char()
    author_ids = fields.Many2many("library.author", string="Authors")
    published_date = fields.Date()
    cover_image = fields.Binary()
    summary = fields.Text()
    total_copies = fields.Integer(default=1)
    sold_copies = fields.Integer(compute="_compute_sold_copies")
    is_available = fields.Boolean(compute="_compute_is_available")
    show_on_website = fields.Boolean(string="Show on Website")
    order_count = fields.Integer(compute="_compute_order_count")
    order_ids = fields.One2many("library.order", "book_id")

    def get_order_ids(self):
        return {
            'name': 'Orders',
            'domain': [('book_id', '=', self.id), ('status', '=', 'sold')],
            'view_type': 'form',
            'res_model': 'library.order',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    @api.depends('order_ids.status')
    def _compute_sold_copies(self):
        for rec in self:
            if rec.order_ids:
                rec.sold_copies = self.env['library.order'].search_count([
                    ('book_id', '=', rec.id),
                    ('status', '=', 'sold')
                ])
            else:
                rec.sold_copies = 0

    @api.depends("total_copies", "sold_copies")
    def _compute_is_available(self):
        for rec in self:
            if rec.sold_copies > 0 or rec.total_copies > 0:
                rec.is_available = rec.total_copies > rec.sold_copies
            else:
                rec.is_available = False

    def _compute_order_count(self):
        for rec in self:
            if rec.order_ids:
                rec.order_count = len(rec.order_ids.filtered(lambda o: o.status == 'sold'))
            else:
                rec.order_count = 0

    # Constraint: Cannot show on website if unavailable
    @api.constrains("show_on_website", "is_available")
    def _check_available_for_website(self):
        for rec in self:
            if rec.show_on_website and not rec.is_available:
                raise ValidationError("You cannot display a book on the website unless it is available.")
