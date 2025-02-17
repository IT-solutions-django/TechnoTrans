from django.contrib.admin import SimpleListFilter


class IsClosed(SimpleListFilter): 
    title = 'Обработано'
    parameter_name = 'is_closed' 

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Да'), 
            ('no', 'Нет'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes': 
            return queryset.filter(is_closed=True)
        elif self.value() == 'no':
            return queryset.filter(is_closed=False)
        return queryset