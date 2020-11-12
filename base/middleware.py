from base.models import General
from django.db.models import F


class BaseMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

class RequestCountMiddleware(BaseMiddleware):
    def process_view(self, request, view_func, view_args, view_kwargs):
        '''
            Updates request count in general table.
        '''
        gen, _= General.objects.get_or_create(pk=0)
        gen.request_count=F('request_count') + 1
        gen.save()
        return None