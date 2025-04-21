from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import Transaction, Category


class TransactionResource(resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, field='name')
    )

    class Meta:
        model = Transaction
        fields = (
            'amount',
            'type',
            'date',
            'category',
        )
        import_id_fields = (
            'amount',
            'type',
            'date',
            'category',
        )

    def after_init_instance(self, instance, new, row, **kwargs):
        instance.user = kwargs.get('user')
