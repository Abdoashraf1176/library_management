from odoo import models, fields


class LibraryOrder(models.Model):
    _name = "library.order"
    _description = "Book Order"

    book_id = fields.Many2one("library.book", required=True)
    customer = fields.Char()
    status = fields.Selection([
        ('draft', 'Draft'),
        ('sold', 'Sold'),
    ], default='draft')

    def action_confirm_order(self):
        for rec in self:
            rec.status = 'sold'
