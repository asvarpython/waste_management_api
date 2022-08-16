from decimal import Decimal
from rest_framework import serializers
from snippet.models import Pickup, Products, Sales, Tags, Snippets
from django.core.validators import DecimalValidator
from rest_framework.reverse import reverse

class TagsSerializer(serializers.ModelSerializer):
    tag_details = serializers.HyperlinkedIdentityField(view_name='tag-detail')
    class Meta:
        model = Tags
        fields = ['id','title', 'tag_details']


class SnippetsSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True, read_only=False,required=False)
    author = serializers.SlugRelatedField(
            read_only=True,
            slug_field='username'
        )
    snippet_details = serializers.HyperlinkedIdentityField(view_name='snippet-detail')
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
    class Meta:
        model = Snippets
        fields = ['id', 'title',"message","file",'tags','author',"created",'snippet_details']
        read_only_fields = ['author']
    def validate(self, attrs):
        #only logged user can update own data only
        if self.instance:
            if  self.context['request'].user.pk != self.instance.author.pk:
                raise serializers.ValidationError({"author": "the user not access for update"})
        else:
            attrs['author'] = self.context['request'].user
        
        return attrs
    def get_validated_data_tag(self,validated_data={}):
        tags_datas ={}
        tags_delete_all=False
        if validated_data.get('tags'):
            tags_datas = validated_data.pop('tags')
        elif "tags" in validated_data: 
            validated_data.pop('tags')
            #if tags exist and it become empty we should delete corresponding tags
            tags_delete_all=True
        return tags_datas,tags_delete_all
    def create(self, validated_data):
        tags_datas,_ = self.get_validated_data_tag(validated_data)
        instance = super(SnippetsSerializer, self).create(validated_data)
        if tags_datas:
            for tags_data in tags_datas:
                tag,created = self.get_or_create_tags(tags_data)
                instance.tags.add(tag)
        return instance
    def update(self, instance, validated_data):
        tags_datas,tags_delete_all = self.get_validated_data_tag(validated_data=validated_data)
        instance = super(SnippetsSerializer, self).update(instance, validated_data)
        if tags_datas:
            for tags_data in tags_datas:
                tag,created = self.get_or_create_tags(tags_data)
                instance.tags.add(tag)
        elif tags_delete_all :
            instance.tags.clear() 
            pass
        return instance
    def get_or_create_tags(self,tags_data={}):
        tag=None
        if tags_data:
            tag,created = Tags.objects.filter(title__iexact=tags_data['title']).get_or_create(
                **tags_data
            )
        return tag,created

    
class ProductsSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
            read_only=True,
            slug_field='username'
        )
    snippet_details = serializers.HyperlinkedIdentityField(view_name='products-detail')
    sale_add = serializers.SerializerMethodField()
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
    class Meta:
        model = Products
        fields = ['id', 'name',"description","image","qty","unit",'user','price',"created",'snippet_details',"sale_add"]
        read_only_fields = ['user']
    def get_sale_add(self, obj):
        result = reverse('sale-new', args=[obj.id], request=self.context['request'])

        return result
    def validate(self, attrs):
        #only logged user can update own data only
        if self.instance:
            if  self.context['request'].user.pk != self.instance.user.pk:
                raise serializers.ValidationError({"user": "the user not access for update"})
        else:
            attrs['user'] = self.context['request'].user
        
        return attrs

    def create(self, validated_data):
        instance = super(ProductsSerializer, self).create(validated_data)
        return instance
    def update(self, instance, validated_data):
        instance = super(ProductsSerializer, self).update(instance, validated_data)
        return instance

class SalesSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
            read_only=True,
            slug_field='username'
        )
    sales_details = serializers.HyperlinkedIdentityField(view_name='sales-detail')
    # products = serializers.PrimaryKeyRelatedField(
    #     queryset=Products.objects.all(), source='products', allow_null=False, required=True
    # )
    def __init__(self, *args, **kwargs):
        self.fields['qty'] = serializers.ChoiceField(choices=[(Decimal('1.00'), '1 Kg'), (Decimal('2.00'), '2 Kg'), (Decimal('3.00'), '3 Kg'),
                                           (Decimal('4.00'), '4 Kg')], validators=[DecimalValidator(max_digits=10, decimal_places=2)])
        super().__init__(*args, **kwargs)
    class Meta:
        model = Sales
        fields = ['id', 'user',"product","qty","estimation_price","sales_details"]
        read_only_fields = ['user']
    def validate(self, attrs):
        #only logged user can update own data only
        if self.instance:
            if  self.context['request'].user.pk != self.instance.user.pk:
                raise serializers.ValidationError({"user": "the user not access for update"})
        else:
            attrs['user'] = self.context['request'].user
        
        return attrs

    def create(self, validated_data):
        instance = super(SalesSerializer, self).create(validated_data)
        return instance
    def update(self, instance, validated_data):
        instance = super(SalesSerializer, self).update(instance, validated_data)
        return instance


class SalesApiViewSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
            read_only=True,
            slug_field='username'
        )
    # products = serializers.PrimaryKeyRelatedField(
    #     queryset=Products.objects.all(), source='products', allow_null=False, required=True
    # )
    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop("product")
        super().__init__(*args, **kwargs)
        # self.fields['product'] = serializers.PrimaryKeyRelatedField(
        #     queryset=[self.product], source='products', allow_null=False, required=True
        # )
        self.fields['qty_estimation_price'] = serializers.ChoiceField(choices=self.get_qty_estimated_price())
    def get_qty_estimated_price(self):
        estimated_price= ()
        for i in range(1,10):
            extimate = (f"{self.product.price*i}-{self.product.qty *i}",f"qty : {self.product.qty *i} {self.product.unit} price :{self.product.price*i}")
            estimated_price = estimated_price + (extimate,)
        return estimated_price    
    class Meta:
        model = Sales
        fields = ['id', 'user',"qty_estimation_price"]
        read_only_fields = ['user']
    def validate(self, attrs):
        #only logged user can update own data only
        if self.instance:
            if  self.context['request'].user.pk != self.instance.user.pk:
                raise serializers.ValidationError({"user": "the user not access for update"})
        else:
            attrs['user'] = self.context['request'].user
        attrs['product'] = self.product
        return attrs

    def create(self, validated_data):
        qty_estimation_price = validated_data.pop("qty_estimation_price")
        qty_estimation_price = qty_estimation_price.split("-")
        validated_data.update({
            "qty":qty_estimation_price[1],
            "estimation_price":qty_estimation_price[0]
        })
        instance = super(SalesApiViewSerializer, self).create(validated_data)
        return instance
    
    def update(self, instance, validated_data):
        instance.product = validated_data.get('product', instance.product)
        instance.qty = validated_data.get('qty', instance.qty)
        instance.estimation_price = validated_data.get('estimation_price', instance.estimation_price)
        instance.save()
        return instance
    

class PickupApiViewSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
            read_only=True,
            slug_field='username'
        )
    def __init__(self, *args, **kwargs):
        self.sale = kwargs.pop("sale")
        super().__init__(*args, **kwargs)
       
    class Meta:
        model = Pickup
        fields = ['id', 'address','user']
        read_only_fields = ['user']
    def validate(self, attrs):
        #only logged user can update own data only
        if self.instance:
            if  self.context['request'].user.pk != self.instance.user.pk:
                raise serializers.ValidationError({"user": "the user not access for update"})
        else:
            attrs['user'] = self.context['request'].user
        attrs['sale'] = self.sale
        return attrs

    def create(self, validated_data):
        instance = super(PickupApiViewSerializer, self).create(validated_data)
        return instance
