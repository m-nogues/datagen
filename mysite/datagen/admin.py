from django.contrib import admin
from django.contrib.admin.views.main import ChangeList

# Register your models here.
from .models import *
from .forms import *


class ExperimentChangeList(ChangeList):

    def __init__(self, request, model, list_display,
                 list_display_links, list_filter, date_hierarchy,
                 search_fields, list_select_related, list_per_page,
                 list_max_show_all, list_editable, model_admin):

        super(ExperimentChangeList, self).__init__(request, model,
                                                   list_display, list_display_links, list_filter,
                                                   date_hierarchy, search_fields, list_select_related,
                                                   list_per_page, list_max_show_all, list_editable,
                                                   model_admin)

        # these need to be defined here, and not in ExperimentAdmin
        self.list_display = ['action_checkbox', 'name', 'hacker']
        self.list_display_links = ['name']
        self.list_editable = ['hacker']


class ExperimentAdmin(admin.ModelAdmin):

    def get_changelist(self, request, **kwargs):
        return ExperimentChangeList

    def get_changelist_form(self, request, **kwargs):
        return ExperimentChangeListForm


admin.site.register(Action)
admin.site.register(Attack)
admin.site.register(Behavior)
admin.site.register(Bias)
admin.site.register(Command)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Hacker)
admin.site.register(Parameter)
admin.site.register(Service)
admin.site.register(Vm)
