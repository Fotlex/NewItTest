from django.contrib import admin
from rangefilter.filters import DateRangeFilter

from .forms import TransactionAdminForm
from .models import Category, Status, Subcategory, Transaction, Type


'''Регистрация моделей с их взаимосвязями в админ панели'''
@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type")
    list_filter = ("type",)
    search_fields = ("name",)
    list_select_related = ("type",)
    inlines = [SubcategoryInline]
    autocomplete_fields = ["type"]


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")
    list_filter = ("category",)
    search_fields = ("name",)
    list_select_related = ("category",)
    autocomplete_fields = ["category"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    form = TransactionAdminForm

    list_display = (
        "created_date",
        "status",
        "type",
        "category",
        "subcategory",
        "amount",
        "comment",
    )
    list_filter = (
        ("created_date", DateRangeFilter),
        "status",
        "type",
        "category",
        "subcategory",
    )
    search_fields = (
        "comment",
        "amount",
        "status__name",
        "type__name",
        "category__name",
        "subcategory__name",
    )
    list_select_related = ("status", "type", "category", "subcategory")

    autocomplete_fields = ["status"]
