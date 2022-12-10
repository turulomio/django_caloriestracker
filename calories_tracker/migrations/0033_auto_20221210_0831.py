# Generated by Django 4.1.3 on 2022-12-10 08:22

from django.db import migrations
from tqdm import tqdm
from mimetypes import guess_type


def move_recipelinkscontent_to_files(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    RecipesLinks= apps.get_model('calories_tracker', 'RecipesLinks')
    Files=apps.get_model('calories_tracker', 'Files')
    for rl in tqdm(RecipesLinks.objects.select_related("recipes").filter(content__isnull=False,files_id__isnull=True).all()):
        f=Files()
        f.content=rl.content
        f.size=len(f.content)
        f.thumbnail=b"from_migration_i_will_be_regenerated"
        if rl.mime is None: #If there is some null mime
            with open("delete_me", "wb") as guess_mime_f:
                guess_mime_f.write(f.content)
            f.mime=guess_type("delete_me")
        else:
            f.mime=rl.mime
        f.user=rl.recipes.user
        f.save()
        #Links RecipesLinks to new Files object
        rl.files=f
        rl.save()

class Migration(migrations.Migration):

    dependencies = [
        ('calories_tracker', '0032_recipeslinks_files'),
    ]

    operations = [
    
        migrations.RunPython(move_recipelinkscontent_to_files),
    ]