from rest_framework.response import Response


class JsonResponse(Response):
    def __init__(
            self,
            code=200,
            success=True,
            msg='成功',
            data=None,
            status=None,
            headers=None,
            content_type=None,
            **kwargs
    ):
        dic = {
            'success': success,
            'code': code,
            'msg': msg,
            'data': data if data else ''
        }
        dic.update(kwargs)
        super().__init__(
            data=dic,
            status=status,
            template_name=None,
            headers=headers,
            exception=False,
            content_type=content_type
        )
