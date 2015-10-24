__author__ = 'suquark'

import base64
import json

import robogame.unused.HttpClient


class OnlineOCR:
    """
    curl 'https://www.projectoxford.ai/Demo/Ocr'
     -H 'Cookie: __RequestVerificationToken=vxIdQTNJ5i1Ijfex_-QR_oOMJ1lHIs3KbwaS1dr4L-mc5D2xwG6F1JuwSoAMhtQaCy0kGwUQMu2bHg6els_aXHWj_xGvtZB41fjNSWQMibo1'
    --data '@/Users/suquark/Desktop/pic_base64.dat' --compressed
    """

    def __init__(self):
        try:
            self.client = robogame.unused.HttpClient.HttpClient()
            text = self.client.Get('https://www.projectoxford.ai/demo/visions')
            sp = '<input name="__RequestVerificationToken" type="hidden" value="'
            txt = text[text.find(sp) + len(sp):]
            self.token = txt[:txt.find('"')]
        except:
            print '[ERROR] OCR Error!'

    def recg(self, path):

            data = base64.encodestring(open(path).read())
            r = self.client.Post('https://www.projectoxford.ai/Demo/Ocr',
                                 {'Data': data, 'isUrl': 'false', 'languageCode': 'en',
                                  '__RequestVerificationToken': self.token})
            dr = json.loads(json.loads(unicode(r)))
            s = ''
            for lines in dr['regions']:
                for line in lines['lines']:
                    for box in line['words']:
                        s += box['text'] + ' '
                    s += '\r\n'
                s += '\r\n'
            return s



"""
EXAMPLE:

a = OnlineOCR()
print a.recg('/Users/suquark/Desktop/camera.jpeg')

b = {
    "language": "en",
    "textAngle": 0.0,
    "orientation": "Up",
    "regions": [
        {
            "boundingBox": "5,146,508,263",
            "lines":
                [
                    {
                        "boundingBox": "159,146,178,44",
                        "words":
                            [
                                {"boundingBox": "159,146,178,44", "text": "Microsoft"}
                            ]
                    },
                    {
                        "boundingBox": "8,206,357,63",
                        "words":
                            [
                                {"boundingBox": "8,212,133,57", "text": "Hello"},
                                {"boundingBox": "182,206,183,63", "text": "01STC"}
                            ]
                    },
                    {
                        "boundingBox": "5,290,508,73",
                        "words":
                            [
                                {"boundingBox": "5,300,110,63", "text": "The"},
                                {"boundingBox": "159,293,162,63", "text": "BEST"},
                                {"boundingBox": "344,290,169,71", "text": "TEAM"}
                            ]
                    },
                    {
                        "boundingBox": "252,371,197,38",
                        "words":
                            [
                                {"boundingBox": "252,371,197,38", "text": "INTERNET"}
                            ]
                    }
                ]
        }]
}
"""
