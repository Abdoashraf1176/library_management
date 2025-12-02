from odoo import models, fields, api


class LibraryAuthor(models.Model):
    _name = "library.author"

    name = fields.Char(required=True)
    biography = fields.Text()
    book_ids = fields.Many2many("library.book", string="Books")
    book_count = fields.Integer(compute="_compute_book_count")

    @api.depends("book_ids")
    def _compute_book_count(self):
        for rec in self:
            rec.book_count = len(rec.book_ids)
