from django.db import migrations

def populate_initial_data(apps, schema_editor):
    Status = apps.get_model('tracker', 'Status')
    Type = apps.get_model('tracker', 'Type')
    Category = apps.get_model('tracker', 'Category')
    Subcategory = apps.get_model('tracker', 'Subcategory')

    Status.objects.bulk_create([
        Status(name='Бизнес'),
        Status(name='Личное'),
        Status(name='Налог'),
    ])

    Type.objects.bulk_create([
        Type(name='Пополнение'),
        Type(name='Списание'),
    ])

    expense_type = Type.objects.get(name='Списание')

    infra_category = Category.objects.create(name='Инфраструктура', type=expense_type)
    Subcategory.objects.bulk_create([
        Subcategory(name='VPS', category=infra_category),
        Subcategory(name='Proxy', category=infra_category),
    ])
    
    marketing_category = Category.objects.create(name='Маркетинг', type=expense_type)
    Subcategory.objects.bulk_create([
        Subcategory(name='Farpost', category=marketing_category),
        Subcategory(name='Avito', category=marketing_category),
    ])


def reverse_data_population(apps, schema_editor):
    Status = apps.get_model('tracker', 'Status')
    Type = apps.get_model('tracker', 'Type')

class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_initial_data, reverse_code=reverse_data_population),
    ]