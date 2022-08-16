from rest_framework import viewsets
from rest_framework.response import Response
from snippet.models import Snippets, Tags,Products,Sales
from .serializer import ProductsSerializer, SalesSerializer, SnippetsSerializer, TagsSerializer,SalesApiViewSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import get_object_or_404

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

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductsSerializer
    permission_classes_by_action = {'create': [IsAuthenticated],
                                    'update': [IsAuthenticated],
                                    'destroy':[IsAuthenticated],
                                    }
    def get_queryset(self):
        return Products.objects.all()
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
    def get(self, request,product_id):
        product = Products.objects.filter(pk=product_id).first()
        # data={'product': product}
        serializer = SalesApiViewSerializer(product =product)
        return Response({'serializer': serializer,"product":product})
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