from rest_framework import serializers
from django.utils import timezone
from django.utils.translation import gettext as _
from calories_tracker import models
from calories_tracker.reusing.request_casting import object_from_url


class ActivitiesSerializer(serializers.HyperlinkedModelSerializer):
    localname = serializers.SerializerMethodField()
    class Meta:
        model = models.Activities
        fields = ('url', 'id', 'name', 'description', 'multiplier', 'localname')

    def get_localname(self, obj):
        return  _(obj.name)

class AdditiveRisksSerializer(serializers.HyperlinkedModelSerializer):
    localname = serializers.SerializerMethodField()
    class Meta:
        model = models.AdditiveRisks
        fields = ('url', 'id', 'name', 'localname')

    def get_localname(self, obj):
        return  _(obj.name)

class AdditivesSerializer(serializers.HyperlinkedModelSerializer):
    fullname = serializers.SerializerMethodField()
    class Meta:
        model = models.Additives
        fields = ('url', 'id', 'name', 'description', 'additive_risks', 'fullname')
        
    def get_fullname(self, o):
        return o.fullname()
        
        
class BiometricsSerializer(serializers.HyperlinkedModelSerializer):
    bmr = serializers.SerializerMethodField()
    imc = serializers.SerializerMethodField()
    imc_comment = serializers.SerializerMethodField()
    recommended_carbohydrate = serializers.SerializerMethodField()
    recommended_fat = serializers.SerializerMethodField()
    recommended_fiber = serializers.SerializerMethodField()
    recommended_protein = serializers.SerializerMethodField()
    recommended_sugars = serializers.SerializerMethodField()
    class Meta:
        model = models.Biometrics
        fields = ('url', 'id', 'datetime', 'height', 'weight', 'weight_wishes', 'activities', 'bmr', 'imc', 'imc_comment', 'recommended_carbohydrate', 'recommended_fat', 'recommended_fiber', 'recommended_protein', 'recommended_sugars')
                
    def create(self, validated_data):
        validated_data['user']=self.context.get("request").user
        created=serializers.HyperlinkedModelSerializer.create(self,  validated_data)
        return created
        
    def get_bmr(self, o):
        return o.bmr()
        
    def get_imc(self, o):
        return o.imc()
    def get_imc_comment(self, o):
        return o.imc_comment()
    def get_recommended_carbohydrate(self, o):
        return o.recommended_carbohydrate()
    def get_recommended_fat(self, o):
        return o.recommended_fat()
    def get_recommended_fiber(self, o):
        return o.recommended_fiber()
    def get_recommended_protein(self, o):
        return o.recommended_protein()
    def get_recommended_sugars(self, o):
        return o.recommended_sugars()

class CompaniesSerializer(serializers.HyperlinkedModelSerializer):
    is_deletable = serializers.SerializerMethodField()
    is_editable = serializers.SerializerMethodField()
    uses=serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Companies
        fields = ('url', 'id', 'name', 'last', 'obsolete', 'system_companies', 'uses', 'is_deletable', 'is_editable')
        
    def create(self, validated_data):
        validated_data['user']=self.context.get("request").user
        validated_data['last']=timezone.now()
        created=serializers.HyperlinkedModelSerializer.create(self,  validated_data)
        return created

    def get_is_deletable(self, o):
        if o.uses>0:
            return False
        return True

    def get_is_editable(self, o):
        if o.system_companies is None:
            return True
        return False

class ElaboratedProductsProductsInThroughSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ElaboratedProductsProductsInThrough

        fields = ('products',  'amount', 'elaborated_products' )
        
class ElaboratedProductsSerializer(serializers.HyperlinkedModelSerializer):
    products_in = ElaboratedProductsProductsInThroughSerializer(many=True, read_only=True, source="elaboratedproductsproductsinthrough_set")
    calories = serializers.SerializerMethodField()
    fat = serializers.SerializerMethodField()
    protein = serializers.SerializerMethodField()
    carbohydrate = serializers.SerializerMethodField()
    salt = serializers.SerializerMethodField()
    cholesterol = serializers.SerializerMethodField()
    sodium = serializers.SerializerMethodField()
    potassium = serializers.SerializerMethodField()
    fiber = serializers.SerializerMethodField()
    sugars = serializers.SerializerMethodField()
    saturated_fat = serializers.SerializerMethodField()
    ferrum = serializers.SerializerMethodField()
    magnesium = serializers.SerializerMethodField()
    phosphor = serializers.SerializerMethodField()
    calcium = serializers.SerializerMethodField()
    glutenfree = serializers.SerializerMethodField()
    class Meta:
        model = models.ElaboratedProducts
        fields = ('url', 'id', 'name', 'last', 'obsolete', 'food_types', 'final_amount', 'products_in', 'calories', 
        'fat', 'protein', 'carbohydrate', 'salt', 'cholesterol', 'sodium', 'potassium', 'fiber', 'sugars', 
        'saturated_fat', 'ferrum', 'magnesium', 'phosphor', 'calcium', 'glutenfree')

    def create(self, validated_data):
        data=self.context.get("request").data
        validated_data['user']=self.context.get("request").user
        validated_data['last']=timezone.now()
        created=serializers.HyperlinkedModelSerializer.create(self,  validated_data)
        created.save()
        for d in data["products_in"]:
            #Create all new
            th=models.ElaboratedProductsProductsInThrough()
            th.amount=d["amount"]
            th.products=object_from_url(d["products"], models.Products)
            th.elaborated_products=created
            th.save()
        created.update_associated_product()
        return created
        
         
    def update(self, instance, validated_data):
        data=self.context.get("request").data
        validated_data['user']=self.context.get("request").user
        validated_data['last']=timezone.now()
        
        updated=serializers.HyperlinkedModelSerializer.update(self, instance, validated_data)
        updated.save()
        
        #Delete all
        qs=models.ElaboratedProductsProductsInThrough.objects.filter(elaborated_products=updated)
        if len(qs)>0:
            qs.delete()

        #Create all new
        for d in data["products_in"]:
            th=models.ElaboratedProductsProductsInThrough()
            th.amount=d["amount"]
            th.products=object_from_url(d["products"], models.Products)
            th.elaborated_products=updated
            th.save()
        
        updated.update_associated_product()
        return updated
        
        

    def get_calories(self, o):
        return o.getElaboratedProductComponent("calories")
    def get_fat(self, o):
        return o.getElaboratedProductComponent("fat")
    def get_protein(self, o):
        return o.getElaboratedProductComponent("protein")
    def get_carbohydrate(self, o):
        return o.getElaboratedProductComponent("carbohydrate")
    def get_salt(self, o):
        return o.getElaboratedProductComponent("salt")
    def get_cholesterol(self, o):
        return o.getElaboratedProductComponent("cholesterol")
    def get_sodium(self, o):
        return o.getElaboratedProductComponent("sodium")
    def get_potassium(self, o):
        return o.getElaboratedProductComponent("potassium")
    def get_fiber(self, o):
        return o.getElaboratedProductComponent("fiber")
    def get_sugars(self, o):
        return o.getElaboratedProductComponent("sugars")
    def get_saturated_fat(self, o):
        return o.getElaboratedProductComponent("saturated_fat")
    def get_ferrum(self, o):
        return o.getElaboratedProductComponent("ferrum")
    def get_magnesium(self, o):
        return o.getElaboratedProductComponent("magnesium")
    def get_phosphor(self, o):
        return o.getElaboratedProductComponent("phosphor")
    def get_calcium(self, o):
        return o.getElaboratedProductComponent("calcium")
    def get_glutenfree(self, o):
        return o.is_glutenfree()
        
class FoodTypesSerializer(serializers.HyperlinkedModelSerializer):
    localname = serializers.SerializerMethodField()
    class Meta:
        model = models.FoodTypes
        fields = ('url', 'id', 'name', 'localname')
    def get_localname(self, obj):
        return  _(obj.name)

class FormatsSerializer(serializers.HyperlinkedModelSerializer):
    localname = serializers.SerializerMethodField()
    class Meta:
        model = models.Formats
        fields = ('url', 'id', 'name', 'localname')

    def get_localname(self, obj):
        return  _(obj.name)

class MealsSerializer(serializers.HyperlinkedModelSerializer):
    calories = serializers.SerializerMethodField()
    fat = serializers.SerializerMethodField()
    protein = serializers.SerializerMethodField()
    carbohydrate = serializers.SerializerMethodField()
    salt = serializers.SerializerMethodField()
    cholesterol = serializers.SerializerMethodField()
    sodium = serializers.SerializerMethodField()
    potassium = serializers.SerializerMethodField()
    fiber = serializers.SerializerMethodField()
    sugars = serializers.SerializerMethodField()
    saturated_fat = serializers.SerializerMethodField()
    ferrum = serializers.SerializerMethodField()
    magnesium = serializers.SerializerMethodField()
    phosphor = serializers.SerializerMethodField()
    calcium = serializers.SerializerMethodField()
    glutenfree = serializers.SerializerMethodField()
    class Meta:
        model = models.Meals
        fields = ('url', 'id', 'datetime', 'products', 'amount', 'calories', 
        'fat', 'protein', 'carbohydrate', 'salt', 'cholesterol', 'sodium', 'potassium', 'fiber', 'sugars', 
        'saturated_fat', 'ferrum', 'magnesium', 'phosphor', 'calcium', 'glutenfree')       

    def create(self, validated_data):
        validated_data['user']=self.context.get("request").user
        created=serializers.HyperlinkedModelSerializer.create(self,  validated_data)
        return created
        
    def get_calories(self, o):
        return o.getProductComponent("calories", 0)
    def get_fat(self, o):
        return o.getProductComponent("fat")
    def get_protein(self, o):
        return o.getProductComponent("protein")
    def get_carbohydrate(self, o):
        return o.getProductComponent("carbohydrate")
    def get_salt(self, o):
        return o.getProductComponent("salt")
    def get_cholesterol(self, o):
        return o.getProductComponent("cholesterol")
    def get_sodium(self, o):
        return o.getProductComponent("sodium")
    def get_potassium(self, o):
        return o.getProductComponent("potassium")
    def get_fiber(self, o):
        return o.getProductComponent("fiber")
    def get_sugars(self, o):
        return o.getProductComponent("sugars")
    def get_saturated_fat(self, o):
        return o.getProductComponent("saturated_fat")
    def get_ferrum(self, o):
        return o.getProductComponent("ferrum")
    def get_magnesium(self, o):
        return o.getProductComponent("magnesium")
    def get_phosphor(self, o):
        return o.getProductComponent("phosphor")
    def get_calcium(self, o):
        return o.getProductComponent("calcium")
    def get_glutenfree(self, o):
        return o.products.glutenfree
    
class ProductsFormatsThroughSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ProductsFormatsThrough

        fields = ('amount', 'formats')
        
class ProductsSerializer(serializers.HyperlinkedModelSerializer):
    formats= ProductsFormatsThroughSerializer(many=True, read_only=True, source="productsformatsthrough_set")
    uses_meals = serializers.IntegerField(read_only=True)
    fullname = serializers.SerializerMethodField()
    

    is_deletable = serializers.SerializerMethodField()
    is_editable = serializers.SerializerMethodField()

    class Meta:
        model = models.Products
        fields = ('url', 'id', 'additives', 'amount', 'calcium', 'calories','carbohydrate', 'cholesterol', 'companies', 'elaborated_products', 'fat', 'ferrum', 'fiber', 'food_types', 'formats', 'glutenfree', 'magnesium', 'name', 'obsolete', 'phosphor', 'potassium', 'protein', 'salt', 'saturated_fat', 'sodium', 'sugars', 'system_products', 'version', 'version_description', 'version_parent', 'fullname', 'uses_meals', 'is_editable', 'is_deletable')
        
    def create(self, validated_data):
        data=self.context.get("request").data
        validated_data['user']=self.context.get("request").user
        validated_data['version']=timezone.now()
        created=serializers.HyperlinkedModelSerializer.create(self,  validated_data)
        created.save()
        for d in data["formats"]:
            #Create all new
            th=models.ProductsFormatsThrough()
            th.amount=d["amount"]
            th.formats=object_from_url(d["formats"], models.Formats)
            th.products=created
            th.save()
        
        return created
        
         
    def update(self, instance, validated_data):
        data=self.context.get("request").data
        validated_data['user']=self.context.get("request").user
        validated_data['version']=timezone.now()
        
        updated=serializers.HyperlinkedModelSerializer.update(self, instance, validated_data)
        updated.save()
        
        #Delete all
        qs=models.ProductsFormatsThrough.objects.filter(products=updated)
        if len(qs)>0:
            qs.delete()

        #Create all new
        for d in data["formats"]:
            th=models.ProductsFormatsThrough()
            th.amount=d["amount"]
            th.formats=object_from_url(d["formats"], models.Formats)
            th.products=updated
            th.save()
        
        return updated

    def get_fullname(self, o):
        return o.fullname()
        
    def get_is_deletable(self, o):
        if o.uses_meals>0:
            return False
        return True

    def get_is_editable(self, o):
        if o.system_products is None:
            return True
        return False

class ProfilesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Profiles
        fields = ('url', 'id', 'birthday', 'male')

class SystemCompaniesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.SystemCompanies
        fields = ('url', 'id', 'name', 'last', 'obsolete')

    def create(self, validated_data):
        validated_data['last']=timezone.now()
        created=serializers.HyperlinkedModelSerializer.create(self,  validated_data)
        created.save()
        return created
        
         
    def update(self, instance, validated_data):
        validated_data['last']=timezone.now()
        
        updated=serializers.HyperlinkedModelSerializer.update(self, instance, validated_data)
        updated.save()
       
        return updated
        
class SystemProductsFormatsThroughSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.SystemProductsFormatsThrough

        fields = ('id','system_products',  'amount', 'formats' )
        
class SystemProductsSerializer(serializers.HyperlinkedModelSerializer):
    system_company_name = serializers.SerializerMethodField()
    formats= SystemProductsFormatsThroughSerializer(many=True, read_only=True, source="systemproductsformatsthrough_set")
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = models.SystemProducts
        fields = ('url', 'id', 'additives', 'amount', 'calcium', 'calories','carbohydrate', 'cholesterol', 'fat', 'ferrum', 'fiber', 'food_types', 'formats', 'glutenfree', 'magnesium', 'name', 'obsolete', 'phosphor', 'potassium', 'protein', 'salt', 'saturated_fat', 'sodium', 'sugars', 'system_companies', 'version', 'version_description', 'version_parent', 'system_company_name', 'fullname')

    def create(self, validated_data):
        request=self.context.get("request")
        validated_data['version']=timezone.now()
        created=serializers.HyperlinkedModelSerializer.create(self,  validated_data)
        created.save()
        for d in request.data["formats"]:
            #Create all new
            th=models.SystemProductsFormatsThrough()
            th.amount=d["amount"]
            th.formats=object_from_url(d["formats"], models.Formats)
            th.system_products=created
            th.save()
        created.update_linked_product(request.user)
        
        return created
        
         
    def update(self, instance, validated_data):
        request=self.context.get("request")
        validated_data['version']=timezone.now()
        
        updated=serializers.HyperlinkedModelSerializer.update(self, instance, validated_data)
        updated.save()
        
        #Delete all
        qs=models.SystemProductsFormatsThrough.objects.filter(system_products=updated)
        if len(qs)>0:
            qs.delete()

        #Create all new
        for d in request.data["formats"]:
            th=models.SystemProductsFormatsThrough()
            th.amount=d["amount"]
            th.formats=object_from_url(d["formats"], models.Formats)
            th.system_products=updated
            th.save()
        updated.update_linked_product(request.user)
        
        return updated

    def get_system_company_name(self, o):
        if o.system_companies is None:
            return None
        return o.system_companies.name

    def get_fullname(self, o):
        return o.fullname()

class WeightWishesSerializer(serializers.HyperlinkedModelSerializer):
    localname = serializers.SerializerMethodField()
    class Meta:
        model = models.WeightWishes
        fields = ('url', 'id', 'name', 'localname')

    def get_localname(self, obj):
        return  _(obj.name)