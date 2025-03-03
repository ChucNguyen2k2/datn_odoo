from odoo import models, fields, api

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book ChucDEV'

    name = fields.Char(string = 'Tên sách', required = True)
    author = fields.Char(string = 'Tác giả')
    publish_date = fields.Date(string = 'Ngày xuất bản')
    isbn = fields.Char(string = 'ISBN')
    category = fields.Selection(
        selection=[
            ('novel', 'Tiểu thuyết'),
            ('science', 'Khoa học'),
            ('short_story', 'Truyện ngắn'),
            ('biography', 'Tiểu sử'),
        ],
        string='Thể loại',
        default='novel',
    )

    @api.depends('name', 'author')
    def _compute_display_name(self):
        for book in self:
            book.display_name = f"{book.name} - {book.author or 'Không rõ'}"