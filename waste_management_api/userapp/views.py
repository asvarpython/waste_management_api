
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

# Create your views here.

class HomeApiView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'userapp/index.html'

    ##@permit_if_role_in(['manager_permission'])
    def get(self, request,sale_id=None):

        return_data =  {}
        return Response(return_data)


