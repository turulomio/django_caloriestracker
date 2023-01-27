
from factory import Faker, SubFactory, lazy_attribute, post_generation, RelatedFactory
from factory.django import DjangoModelFactory
from calories_tracker import models
from django.utils import timezone
#https://faker.readthedocs.io/en/master/providers/faker.providers.currency.html

class ActivitiesFactory(DjangoModelFactory):
    class Meta:
        model= models.Activities
        
    name = Faker("bothify", text="Activities ??????")
    description = Faker("sentence")
    multiplier = Faker("random_int")
    
    
class WeightWishesFactory(DjangoModelFactory):
    class Meta:
        model= models.WeightWishes
        
    name = Faker("bothify", text="Weight Wish ??????")

class BiometricsFactory(DjangoModelFactory):
    class Meta:
        model= models.Biometrics
    datetime = timezone.now()
    weight = Faker("random_int")
    height = Faker("random_int")
    activities = SubFactory(ActivitiesFactory)
    weight_wishes = SubFactory(WeightWishesFactory) 

class FoodTypesFactory(DjangoModelFactory):
    class Meta:
        model= models.FoodTypes
        
    name = Faker("bothify", text="Food Type ??????")

class RecipesCategoriesFactory(DjangoModelFactory):
    class Meta:
        model= models.RecipesCategories
        
    name = Faker("bothify", text="Recipe Category ??????")

class ActivitiesFactory(DjangoModelFactory):
    class Meta:
        model= models.Activities
        
    name = Faker("bothify", text="Activities ??????")
    description = Faker("sentence")
    multiplier = Faker("random_int")

class AdditiveRisksFactory(DjangoModelFactory):
    class Meta:
        model= models.AdditiveRisks
        
    name = Faker("bothify", text="Additive Risk ??????")
    
class FormatsFactory(DjangoModelFactory):
    class Meta:
        model= models.Formats
        
    name = Faker("bothify", text="Format ??????")
    
class AdditivesFactory(DjangoModelFactory):
    class Meta:
        model= models.Additives
        
    name = Faker("bothify", text="Additives ??????")
    description = Faker("sentence")
    additive_risks = SubFactory(AdditiveRisksFactory)
    
class RecipesLinksTypesFactory(DjangoModelFactory):
    class Meta:
        model= models.RecipesLinksTypes
        
    name = Faker("bothify", text="Recipe Link Type ??????")

class FilesFactory(DjangoModelFactory):
    class Meta:
        model= models.Files

    content=Faker("image")
    mime="image/png"
#    user = models.ForeignKey(User, on_delete=models.DO_NOTHING) 
    @lazy_attribute
    def size(self):
        return len(self.content)
        
    @lazy_attribute
    def thumbnail(self):
        return self.content

class RecipesFactory(DjangoModelFactory):
    class Meta:
        model= models.Recipes
    name = Faker("bothify", text="Recipe ??????")
    datetime=timezone.now()
    last=timezone.now()
    food_types=SubFactory(FoodTypesFactory)
    obsolete =Faker("boolean")
#    user=SubFactory(UserFactory)
    comment=Faker("sentence")
    valoration=Faker("random_int")
    guests=Faker("boolean")
    soon=Faker("boolean")

    @post_generation
    def recipes_categories(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        # Add the iterable of groups using bulk addition
        self.recipes_categories.add(*extracted)

class RecipesLinksFactory(DjangoModelFactory):
    class Meta:
        model= models.RecipesLinks
        
    description = Faker("bothify", text="Recipe Link ??????")
    type=SubFactory(RecipesLinksTypesFactory)
    link=Faker("uri")
    files=SubFactory(FilesFactory)
    recipes=SubFactory(RecipesFactory)

class ElaboratedProductsFactory(DjangoModelFactory):
    class Meta:
        model= models.ElaboratedProducts
        
    name = Faker("bothify", text="Elaborated Product ??????")
    
    final_amount = Faker("random_int")
    last=timezone.now()
    food_types=SubFactory(FoodTypesFactory)
    obsolete =Faker("boolean")
    products_in=None
    recipes=None
    
    @lazy_attribute
    def name(self):
        return f'Leverage x{self.multiplier}'
        
class SystemCompaniesFactory(DjangoModelFactory):
    class Meta:
        model= models.SystemCompanies
    name = Faker("bothify", text="System Company ??????")
    last = timezone.now()
    obsolete = False

class CompaniesFactory(DjangoModelFactory):
    class Meta:
        model= models.Companies
    name = Faker("bothify", text="System Company ??????")
    last = timezone.now()
    obsolete = False
    system_companies=None
    
class SystemProductsFactory(DjangoModelFactory):
    class Meta:
        model= models.SystemProducts
        
    name = Faker("bothify", text="System Product ??????")
    amount=Faker("random_int")
    fat=Faker("random_int")
    protein=Faker("random_int")
    carbohydrate=Faker("random_int")
    calories=Faker("random_int")
    salt=Faker("random_int")
    cholesterol=Faker("random_int")
    sodium=Faker("random_int")
    potassium=Faker("random_int")
    fiber=Faker("random_int")
    sugars=Faker("random_int")
    saturated_fat=Faker("random_int")
    ferrum=Faker("random_int")
    magnesium=Faker("random_int")
    phosphor=Faker("random_int")
    glutenfree=Faker("boolean")
    calcium=Faker("random_int")
    system_companies=SubFactory(SystemCompaniesFactory)
    food_types=SubFactory(FoodTypesFactory)


    density=Faker("random_int")
    obsolete=False
    version_parent=None
    version=timezone.now()
    version_description=None

        
    @post_generation
    def additives(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        # Add the iterable of groups using bulk addition
        self.additives.add(*extracted)


        
                
class SystemProductsFormatsThroughFactory(DjangoModelFactory):
    class Meta:
        model= models.SystemProductsFormatsThrough
    system_products = SubFactory(SystemProductsFactory)
    formats = SubFactory(FormatsFactory)
    amount = Faker("random_int")
    
class SystemProductsFactoryWithFormats(SystemProductsFactory):
    formats = RelatedFactory(
        SystemProductsFormatsThroughFactory,
        factory_related_name='formats',
    )
