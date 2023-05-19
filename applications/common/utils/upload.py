import os
from flask import current_app
from applications.extensions.init_upload import photos

def upload_one(photo):
    filename = photos.save(photo)
    file_url = '/_uploads/photos/'+filename
    upload_url = current_app.config.get("UPLOADED_PHOTOS_DEST")
    size = os.path.getsize(upload_url + '/' + filename)
    return file_url

