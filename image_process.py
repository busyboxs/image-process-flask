from base import Base
from base import base64

client_id = 'your API Key'
client_secret = 'your Secret Key'


class ImageProcess(Base):
    __process_url = 'https://aip.baidubce.com/rest/2.0/image-process/v1/'
    __image_quality_enhance_url = __process_url + 'image_quality_enhance'
    __dehaze_url = __process_url + 'dehaze'
    __contrast_enhance_url = __process_url + 'contrast_enhance'
    __colorize_url = __process_url + 'colourize'
    __stretch_restore_url = __process_url + 'stretch_restore'
    __style_trans_url = __process_url + 'style_trans'

    def image_quality_enhance(self, image, options=None):
        options = options or {}
        data = {}
        data['image'] = base64.b64encode(image).decode()
        data.update(options)
        return self._request(self.__image_quality_enhance_url, data)

    def dehaze(self, image, options=None):
        options = options or {}
        data = {}
        data['image'] = base64.b64encode(image).decode()
        data.update(options)
        return self._request(self.__dehaze_url, data)

    def contrast_enhance(self, image, options=None):
        options = options or {}
        data = {}
        data['image'] = base64.b64encode(image).decode()
        data.update(options)
        return self._request(self.__contrast_enhance_url, data)

    def colorize(self, image, options=None):
        options = options or {}
        data = {}
        data['image'] = base64.b64encode(image).decode()
        data.update(options)
        return self._request(self.__colorize_url, data)

    def stretch_restore(self, image, options=None):
        options = options or {}
        data = {}
        data['image'] = base64.b64encode(image).decode()
        data.update(options)
        return self._request(self.__stretch_restore_url, data)

    def style_trans(self, image, options=None):
        options = options or {}
        data = {}
        data['image'] = base64.b64encode(image).decode()
        data.update(options)
        return self._request(self.__style_trans_url, data)
