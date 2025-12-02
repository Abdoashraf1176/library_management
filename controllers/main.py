from odoo import http
from odoo.http import request


class LibraryWebsite(http.Controller):

    @http.route('/library/books', type='http', auth='public', website=True)
    def books_list(self, **kwargs):
        books = request.env['library.book'].sudo().search([
            ('is_available', '=', True)
        ])
        return request.render('library_management.books_list_template', {
            'books': books,
        })

    @http.route('/library/book/<int:book_id>', type='http', auth='public', website=True)
    def book_detail(self, book_id, **kwargs):
        book = request.env['library.book'].sudo().browse(book_id)
        if not book.exists() or not book.is_available:
            return request.redirect('/library/books')
        return request.render('library_management.book_detail_template', {
            'book': book,
        })

    @http.route('/library/book/<int:book_id>/order', type='http', auth='public', website=True, methods=['POST'],
                csrf=True)
    def create_order(self, book_id, customer_name='', **kwargs):
        book = request.env['library.book'].sudo().browse(book_id)

        if not book.exists() or not book.is_available:
            return request.redirect('/library/books')

        order = request.env['library.order'].sudo().create({
            'book_id': book_id,
            'customer': customer_name or 'Website Customer',
            'status': 'draft',
        })

        return request.redirect('/library/book/%s?order_created=1' % book_id)
