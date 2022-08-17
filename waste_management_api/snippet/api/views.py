from rest_framework import viewsets
from rest_framework.response import Response
from snippet.models import Pickup, Snippets, Tags,Products,Sales
from .serializer import PickupApiViewSerializer, ProductsSerializer, SalesSerializer, SnippetsSerializer, TagsSerializer,SalesApiViewSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import get_object_or_404
from snippet.decorators import permit_if_role_in
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

class SnippetsViewSet(viewsets.ModelViewSet):
    serializer_class = SnippetsSerializer
    permission_classes_by_action = {'create': [IsAuthenticated],
                                    'update': [IsAuthenticated],
                                    'destroy':[IsAuthenticated],
                                    }
    def get_queryset(self):
        return Snippets.objects.all()
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            pass
        return self.list(request, *args, **kwargs)
    def get_permissions(self):
        try:
            # return permission_classes depending on action 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # when exception occure jump to default permission_classes
            return [permission() for permission in self.permission_classes]
class TagsViewSet(viewsets.ModelViewSet):
    serializer_class = TagsSerializer

    def get_queryset(self):
        return Tags.objects.all()
#if request.user.has_perm('app_name.can_add_cost_price'):

# @method_decorator(permission_required("manager_permission"), name="dispatch")
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductsSerializer
    permission_classes_by_action = {'create': [IsAuthenticated],
                                    'update': [IsAuthenticated],
                                    'destroy':[IsAuthenticated],
                                    }
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'snippet/product.html'
    def get_queryset(self):
        return Products.objects.all()

    #@permit_if_role_in(['manager_permission'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    #@permit_if_role_in(['manager_permission'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    #@permit_if_role_in(['manager_permission'])
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            pass
        return self.list(request, *args, **kwargs)
    def get_permissions(self):
        try:
            # return permission_classes depending on action 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # when exception occure jump to default permission_classes
            return [permission() for permission in self.permission_classes]

class SalesViewSet(viewsets.ModelViewSet):
    serializer_class = SalesSerializer
    permission_classes_by_action = {'create': [IsAuthenticated],
                                    'update': [IsAuthenticated],
                                    'destroy':[IsAuthenticated],
                                    }
    def get_queryset(self):
        return Sales.objects.all()
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            pass
        return self.list(request, *args, **kwargs)
    def get_permissions(self):
        try:
            # return permission_classes depending on action 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # when exception occure jump to default permission_classes
            return [permission() for permission in self.permission_classes]


class SalesApiView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'snippet/sales.html'
    # def get(self, request):
    #     self.template_name = 'snippet/get_sales.html'
    #     sales = Sales.objects.all()
    #     # the many param informs the serializer that it will be serializing more than a single sales.
    #     serializer = SalesApiViewSerializer(sales, many=True)
    #     return Response({"sales": serializer.data})
    def get(self, request,product_id=None):
        if product_id:
            return self.get_product_sale(request,product_id)
        else:
            return self.get_sales_list(request)
    def post(self, request,product_id):
        product = Products.objects.filter(pk=product_id).first()
        sales = request.data
        # Create an sales from the above data
        serializer = SalesApiViewSerializer(data=sales,product =product,context={'request': request})
        if serializer.is_valid():
            sales_saved = serializer.save()
            return Response({'serializer': serializer,"product":product,"success":"Buy Successfully"})
        return Response({'serializer': serializer,"product":product})
    

    def put(self, request, pk):
        saved_sales = Sales.objects.filter(pk=pk).first()
        data = request.data.get('sales')
        serializer = SalesApiViewSerializer(instance=saved_sales, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            sales_saved = serializer.save()
        return Response({"success": "Sales '{}' updated successfully".format(sales_saved.title)})


    def delete(self, request, pk):
        # Get object with this pk
        sales = get_object_or_404(Sales.objects.all(), pk=pk)
        sales.delete()
        return Response({"message": "Sales with id `{}` has been deleted.".format(pk)},status=204)
    def get_product_sale(self,request,product_id=None):
        product = Products.objects.filter(pk=product_id).first()
        # data={'product': product}
        serializer = SalesApiViewSerializer(product =product)
        return Response({'serializer': serializer,"product":product})
    
    def get_sales_list(self,request):
        self.template_name = 'snippet/sales_list.html'
        sales = Sales.objects.filter(user=request.user).all()
        return Response({'sales': sales})


class PickupApiView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'snippet/pickup.html'
    message =  "Your address is updated pickup take place with in 24 hour"

    ##@permit_if_role_in(['manager_permission'])
    def get(self, request,sale_id=None):
        sale = Sales.objects.filter(pk=sale_id).first()
        pickup =  Pickup.objects.filter(sale_id=sale_id).first()
        serializer =None
        return_data = {"sale":sale,"pickup":pickup}
        if not pickup:
            serializer = PickupApiViewSerializer(sale =sale)
            return_data.update({
                'serializer':serializer
            })
        else:
            return_data.update({'message':self.message})
        return Response(return_data)

    #@permit_if_role_in(['manager_permission'])
    def post(self, request,sale_id=None):
        sale = Sales.objects.filter(pk=sale_id).first()
        pickup =  Pickup.objects.filter(pk=sale_id).first()
        serializer = PickupApiViewSerializer(data=request.data,sale =sale,context={'request': request})
        return_data = {'serializer': serializer,"sale":sale,"pickup":pickup}
        
        
        if serializer.is_valid():
            pickup_saved = serializer.save()
            return_data ={"message":self.message,"sale":sale,"pickup":pickup_saved}

        return Response(return_data)
    

   
   