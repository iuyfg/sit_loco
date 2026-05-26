# main/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import RepairRequest


@admin.register(RepairRequest)
class RepairRequestAdmin(admin.ModelAdmin):
    # Отображаемые поля в списке
    list_display = (
        'id',
        'full_name',
        'phone',
        'company',
        'locomotive_number',
        'repair_type',
        'urgent_icon',
        'status_badge',        # ← Красивый бейдж (HTML)
        'created_at_short',
    )

    # ❌ ЗАКОММЕНТИРОВАНО: нельзя редактировать 'status' в списке,
    # если в list_display вместо него используется 'status_badge'
    # list_editable = ('status',)

    # Фильтры по бокам
    list_filter = (
        'status',
        'urgent',
        'repair_type',
        'created_at',
        'locomotive_type',
    )

    # Поля для поиска
    search_fields = (
        'full_name',
        'phone',
        'email',
        'company',
        'locomotive_number',
        'problem_description',
    )

    # Количество записей на странице
    list_per_page = 25

    # Поля, которые отображаются при редактировании
    fieldsets = (
        ('Контактная информация', {
            'fields': (
                ('full_name', 'phone'),
                ('email', 'company'),
            )
        }),
        ('Информация о локомотиве', {
            'fields': (
                ('locomotive_type', 'locomotive_model', 'locomotive_number'),
                ('repair_type', 'urgent'),
            )
        }),
        ('Детали заявки', {
            'fields': ('problem_description',)
        }),
        ('Статус и служебная информация', {
            'fields': ('status', 'user', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    # Только для чтения
    readonly_fields = ('created_at', 'updated_at')

    # Действия с несколькими заявками (массовое изменение статуса)
    actions = ['mark_as_new', 'mark_as_in_progress', 'mark_as_completed', 'mark_as_cancelled']

    # Кастомные иконки и статусы
    def urgent_icon(self, obj):
        if obj.urgent:
            return format_html('<span style="color: #E30613; font-size: 1.2rem;">⚠️</span> Срочно')
        return '—'

    urgent_icon.short_description = 'Срочность'

    def status_badge(self, obj):
        status_colors = {
            'new': '#0d6efd',
            'in_progress': '#fd7e14',
            'completed': '#198754',
            'cancelled': '#dc3545',
        }
        status_names = {
            'new': '🆕 Новая',
            'in_progress': '⚙️ В работе',
            'completed': '✅ Выполнена',
            'cancelled': '❌ Отменена',
        }
        color = status_colors.get(obj.status, '#6c757d')
        name = status_names.get(obj.status, obj.status)
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 15px; font-size: 0.85rem;">{}</span>',
            color, name
        )

    status_badge.short_description = 'Статус'

    def created_at_short(self, obj):
        return obj.created_at.strftime('%d.%m.%Y %H:%M')

    created_at_short.short_description = 'Дата создания'

    # Действия (массовое изменение статуса)
    def mark_as_new(self, request, queryset):
        updated = queryset.update(status='new')
        self.message_user(request, f'{updated} заявок переведены в статус "Новая"')

    mark_as_new.short_description = '📋 Отметить как "Новая"'

    def mark_as_in_progress(self, request, queryset):
        updated = queryset.update(status='in_progress')
        self.message_user(request, f'{updated} заявок переведены в статус "В работе"')

    mark_as_in_progress.short_description = '🔧 Отметить как "В работе"'

    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} заявок отмечены как "Выполнены"')

    mark_as_completed.short_description = '✅ Отметить как "Выполнена"'

    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} заявок отменены')

    mark_as_cancelled.short_description = '❌ Отметить как "Отменена"'