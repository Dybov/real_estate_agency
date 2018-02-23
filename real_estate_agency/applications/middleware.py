from urllib.parse import urlencode

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

UTM_PARAMS = ('utm_source', 'utm_medium',
              'utm_campaign', 'utm_content', 'utm_term')


class UTMMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ''' It reads get parameters for utm marketing links
        If it finds then save them in COOKIES and redirect

        Following parameter are possible:
        utm_source=yandex.search
        utm_medium=cpc
        utm_campaign={campaign_id}
        utm_content={ad_id}
        utm_term={keyword}
        '''
        if 'utm_source' in request.GET:
            url = request.path
            get = request.GET.copy()
            print(get)
            utm_dict = {}
            for utm_param in UTM_PARAMS:
                utm_dict[utm_param] = get.pop(utm_param, ['-'])[0]
            print(utm_dict)
            if get:
                url += '?' + urlencode(get)

            response = redirect(url)
            for utm_param in UTM_PARAMS:
                response.set_cookie(utm_param, utm_dict.get(
                    utm_param), max_age=2592000)
            return response
        return None
