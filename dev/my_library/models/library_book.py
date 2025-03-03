from odoo import models, fields, api, exceptions
from odoo.addons.mail.models.mail_thread import MailThread
import base64

class LibraryBook(models.Model, MailThread):
    _name = 'library.book'
    _description = 'Library Book ChucDEV'

    name = fields.Char(string='Tên sách', required=True)
    author = fields.Char(string='Tác giả')
    publish_date = fields.Date(string='Ngày xuất bản')
    isbn = fields.Char(string='ISBN')
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

    @api.constrains('book_file')
    def _check_book_file(self):
        for record in self:
            if record.book_file:
                try:
                    import base64
                    file_data = base64.b64decode(record.book_file)
                    if not file_data.startswith(b'%PDF'):
                        raise exceptions.ValidationError("Chỉ chấp nhận file PDF cho sách!")
                except Exception:
                    raise exceptions.ValidationError("File sách không hợp lệ!")

    @api.constrains('cover_image')
    def _check_cover_image(self):
        for record in self:
            if record.cover_image:
                try:
                    # Giải mã dữ liệu base64 thành bytes
                    image_data = base64.b64decode(record.cover_image)
                    # Kiểm tra magic number của JPG và PNG
                    if not any(image_data.startswith(prefix) for prefix in [b'\xFF\xD8', b'\x89PNG']):
                        raise exceptions.ValidationError("Chỉ chấp nhận ảnh JPG hoặc PNG cho bìa sách!")
                except Exception:
                    raise exceptions.ValidationError("Ảnh bìa không hợp lệ! Vui lòng kiểm tra lại file.")

    # Trong create (thêm thông báo popup sau khi tạo)
    # Trong create (nếu muốn thêm popup nhưng giữ logic Odoo)
    @api.model
    def create(self, vals):
        if 'book_file' not in vals or not vals['book_file']:
            raise exceptions.ValidationError("Vui lòng tải file sách lên trước khi lưu")
        record = super(LibraryBook, self).create(vals)
        record.message_post(body=f'Sách "{record.display_name}" đã được tạo thành công!', message_type="notification")
        # Thêm action popup nhưng không trả về nó trực tiếp
        action = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thành công',
                'message': f'Sách "{record.display_name}" đã được tạo thành công!',
                'type': 'success',
                'sticky': False,
            }
        }
        # Gửi action qua JavaScript hoặc không làm gián đoạn return
        return record  # Vẫn trả về bản ghi


    # Trong write (cho cover_image, tương tự)
    def write(self, vals):
        res = super(LibraryBook, self).write(vals)
        if 'cover_image' in vals:
            for record in self:
                if vals['cover_image']:
                    try:
                        self._check_cover_image()
                        record.message_post(body="Ảnh bìa đã được tải lên thành công!", message_type="notification")
                        return {
                            'type': 'ir.actions.client',
                            'tag': 'display_notification',
                            'params': {
                                'title': 'Thành công',
                                'message': 'Ảnh bìa đã được tải lên thành công!',
                                'type': 'success',
                                'sticky': False,
                            }
                        }
                    except exceptions.ValidationError:
                        raise
                else:
                    record.message_post(body="Ảnh bìa đã bị xóa", message_type="notification")
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'title': 'Thông báo',
                            'message': 'Ảnh bìa đã bị xóa',
                            'type': 'info',
                            'sticky': False,
                        }
                    }
        return res