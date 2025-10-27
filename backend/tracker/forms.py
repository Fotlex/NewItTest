from django import forms

from .models import Category, Subcategory, Transaction


class TransactionAdminForm(forms.ModelForm):
    '''Форма реализующая Бизнес-правила задания'''
    class Meta:
        model = Transaction
        fields = "__all__"

    class Media:
        js = ("tracker/js/transaction_admin_form.js",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["type"].required = True
        self.fields["category"].required = True
        self.fields["subcategory"].required = True

        if self.instance and self.instance.pk:
            if self.instance.type:
                self.fields["category"].queryset = Category.objects.filter(
                    type=self.instance.type
                ).order_by("name")
            if self.instance.category:
                self.fields["subcategory"].queryset = Subcategory.objects.filter(
                    category=self.instance.category
                ).order_by("name")
        elif "type" in self.data:
            try:
                type_id = int(self.data.get("type"))
                self.fields["category"].queryset = Category.objects.filter(
                    type_id=type_id
                ).order_by("name")
            except (ValueError, TypeError):
                pass

        if "category" in self.data:
            try:
                category_id = int(self.data.get("category"))
                self.fields["subcategory"].queryset = Subcategory.objects.filter(
                    category_id=category_id
                ).order_by("name")
            except (ValueError, TypeError):
                pass
        elif not self.instance.pk:
            self.fields["category"].queryset = Category.objects.none()
            self.fields["subcategory"].queryset = Category.objects.none()

    def clean(self):
        cleaned_data = super().clean()

        m_type = cleaned_data.get("type")
        category = cleaned_data.get("category")
        subcategory = cleaned_data.get("subcategory")

        if m_type and category:
            if category.type != m_type:
                self.add_error(
                    "category",
                    f"Выбранная категория '{category.name}' не относится к типу '{m_type.name}'.",
                )

        if category and subcategory:
            if subcategory.category != category:
                self.add_error(
                    "subcategory",
                    f"Выбранная подкатегория '{subcategory.name}' не относится к категории '{category.name}'.",
                )

        return cleaned_data
