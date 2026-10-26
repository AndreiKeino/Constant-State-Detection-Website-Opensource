from django.contrib import messages
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.uploadhandler import (
    FileUploadHandler, StopUpload)
from django.http import HttpRequest


class AbortUploadHandler(FileUploadHandler):

    def __init__(self, request=None, max_size: int=1024*8):
        super().__init__(request)
        if max_size <= 0:
            raise ValueError('max_size should be greater than zero')
        self._max_size = max_size
        self._length = 0
        self._request: HttpRequest = request

    def new_file(self, field_name, file_name, content_type, content_length, charset=None, content_type_extra=None):
        self._length = 0
        """
        Triggered as soon as a file starts uploading.
        """
        # Example condition: Abort if file is larger than self._max_size
        # print(f'content_length = {content_length}')
        if content_length and content_length > self._max_size:
            # Setting connection_reset=True abruptly kills the socket connection
            messages.error(self._request,
                           self.get_ex_text(content_length))
            raise StopUpload(connection_reset=True)

    def receive_data_chunk(self, raw_data, start):
        """
        Triggered continuously as data chunks arrive.
        """
        # Example condition: Inspect stream content or enforce strict runtime limits
        # if some_invalid_condition_met:
        #     raise StopUpload(connection_reset=True)
        self._length += len(raw_data)
        if self._length > self._max_size:
            # print('raising exception StopUpload')
            messages.error(self._request,
                           self.get_ex_text(self._length))
            raise StopUpload(connection_reset=True)

        return raw_data

    def file_complete(self, file_size):
        # REQUIRED: Finalize processing and return an UploadedFile instance
        # self.file_buffer.seek(0)
        #
        # # Example returning an in-memory representation
        # return InMemoryUploadedFile(
        #     file=self.file_buffer,
        #     field_name=self.field_name,
        #     name=self.file_name,
        #     content_type=self.content_type,
        #     size=file_size,
        #     charset=self.charset,
        #     content_type_extra=self.content_type_extra
        # )
        return None

    def get_ex_text(self, upload_size) -> str:
        ex_text = (f'Error: max. permitted uploaded file size = {self._max_size} '
                   f'bytes, but you are trying to download at '
                   f'least {upload_size} bytes. '
                   f'Please remember that upload file size'
                   f' should be less or equal than {self._max_size} bytes. '
                   )
        return ex_text

