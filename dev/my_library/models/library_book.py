from odoo import models, fields, api, exceptions

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book ChucDEV'

    name = fields.Char(string = 'Tên sách', required = True)
    author = fields.Char(string = 'Tác giả')
    publish_date = fields.Date(string = 'Ngày xuất bản')
    isbn = fields.Char(string = 'ISBN')
    count = fields.Char(string='Số lượng')
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
    book_file = fields.Binary(string='File sách', attachment=True)
    cover_image = fields.Binary(string='Ảnh bìa', attachment=True)

    @api.depends('name', 'author')
    def _compute_display_name(self):
        for book in self:
            book.display_name = f"{book.name} - {book.author or 'Không rõ'}"

    @api.constrains('book_file', 'book_filename')
    def _check_book_file(self):
        for record in self:
            if record.book_file and not record.book_filename.lower().endswith('.pdf'):
                raise exceptions.ValidationError("Chỉ chấp nhận file PDF cho sách")

    @api.constrains('cover_image')
    def _check_cover_image(self):
        for record in self:
            if record.cover_image and not any(record.cover_image.startswith(prefix) for prefix in [b'\xFF\xD8', b'\x89PNG']):
                raise exceptions.ValidationError("Chỉ chấp nhận ảnh JPG hoặc PNG cho bìa sách")