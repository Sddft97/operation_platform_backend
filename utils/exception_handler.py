from django.http.response import JsonResponse as JResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.views import exception_handler

from utils.response import JsonResponse


def custom_exception_handler(exc, context):
    """
    DRF的全局异常处理

    用于处理DRF定义的APIException,
    也可在此编写逻辑扩展处理自定义Exception

    无法处理的Exception将传递给django的异常处理器
    """
    response = exception_handler(exc, context)
    if response:
        return JsonResponse(data=response.data,
                            code=response.status_code,
                            msg=exc.detail,
                            success=False)
    return response


class ExceptionMiddleware(MiddlewareMixin):
    """
    自定义Django中间件

    此中间件用于处理全局异常
    """

    def process_exception(self, request, exception):
        """
        中间件中定义此方法可用于处理异常
        """

        ex_data = {
            'success': False,
            'msg': 'Server Error',
            'code': 500,
            'data': ''
        }
        # 注意，此处返回时只能使用django原生JsonResponse
        # 使用DRF的Response会出现问题
        return JResponse(data=ex_data, status=500)


def http404handler(request, exception=None):
    """
    处理404页面

    原生django处理404时会返回一个html页面,
    重写此逻辑使其返回json
    """
    data = {
        'success': False,
        'msg': 'The resource is not found',
        'code': 404,
        'data': ''
    }
    return JResponse(data, status=404)


def http500handler(request, exception=None):
    """
    处理500页面

    原生django处理500时会返回一个html页面,
    重写此逻辑使其返回json
    """
    data = {
        'success': False,
        'msg': 'Server Error',
        'code': 500,
        'data': ''
    }
    return JResponse(data, status=500)
