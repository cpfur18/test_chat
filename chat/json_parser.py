import json

class JsonCheck:
    # 후속 질문 확인
    def multi_check(self, req):
        result = False
        json_data = json.loads(req.text)
        response = len(json_data['bubbles'])

        if response > 1:
            result = True
        return result

    # 템플릿 형식 답변 확인
    def template_check(self, req):
        result = False
        json_data = json.loads(req.text)
        response = json_data['bubbles'][0]['type']

        if response == 'template':
            result = True
        return result

    # 템플릿 형식 답변 텍스트 + 버튼
    def template_text_check(self, req):
        result = False
        json_data = json.loads(req.text)
        response = json_data['bubbles'][0]['data']['cover']['type']

        if response == 'text':
                result = True

        return result

    # 템플릿 형식 답변 이미지 + 버튼
    def template_image_check(self, req):
        result = False
        json_data = json.loads(req.text)
        response = json_data['bubbles'][0]['data']['cover']['type']

        if response == 'image':
            result = True
        return result

    # 템플릿 형식 답변 이미지 리스트
    def template_imagelist_check(self, req):
        result = False
        json_data = json.loads(req.text)
        response = json_data['bubbles'][0]['data']['cover']['contentTable']['data']['type']

        if response == 'image':
            result = True
        return result

    # 텍스트 형식 답변 확인
    def text_check(self, req):
        result = False
        json_data = json.loads(req.text)
        response = json_data['bubbles'][0]['type']

        if response == 'text':
            result = True
        return result

    # 풀 스타일 텍스트 형식 답변 확인
    def text_full_check(self, req):
        result = False
        json_data = req
        response = json_data['bubbles'][0]['data']
        if 'url' in response:
            result = True
        return result

    # 이미지 형식 답변 확인
    def img_check(self, req):
        result = False
        json_data = json.loads(req.text)
        response = json_data['bubbles'][0]['type']

        if response == 'image':
            result = True
        return result

    # 풀 스타일 이미지 형식 답변 확인
    def img_full_check(self, req):
        result = False
        json_data = req
        response = json_data['bubbles'][0]['data']['optional']

        if response == 'imagePosition is top, full style':
            result = True
        return result