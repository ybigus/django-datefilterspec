# -*- coding: utf-8 -*-


'''
Has the filter that allows to filter by a date range.

'''
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime
from django.db import models
from django.utils.translation import ugettext as _
import datetime


class DateRangeForm(forms.Form):

    def __init__(self, *args, **kwargs):
        field_name = kwargs.pop('field_name')
        super(DateRangeForm, self).__init__(*args, **kwargs)

        self.fields['%s__gte' % field_name] = forms.DateField(
            label='', widget=AdminDateWidget(
                attrs={'placeholder': _('From date')}), localize=True,
            required=False)

        self.fields['%s__lte' % field_name] = forms.DateField(
            label='', widget=AdminDateWidget(
                attrs={'placeholder': _('To date')}), localize=True,
            required=False)
        
        #copy params
        data = kwargs['data']
        for key in data.keys():
            if (key.endswith('__lte') or key.endswith('__gte')) and not key.startswith(field_name):
                self.fields[key] = forms.DateField(label='', widget=forms.HiddenInput(attrs={'id':'%s_%s'%(key, field_name)}),required=False)
            if not key.endswith('__lte') and not key.endswith('__gte'):
                self.fields[key] = forms.CharField(widget=forms.HiddenInput,required=False)


class DateTimeRangeForm(forms.Form):

    def __init__(self, *args, **kwargs):
        field_name = kwargs.pop('field_name')
        super(DateTimeRangeForm, self).__init__(*args, **kwargs)
        self.fields['%s__gte' % field_name] = forms.DateTimeField(
                                label='',
                                widget=AdminSplitDateTime(
                                    attrs={'placeholder': _('From Date')}
                                ),
                                localize=True,
                                required=False)
        
        #copy params
        data = kwargs['data']
        for key in data.keys():
            if (key.endswith('__lte') or key.endswith('__gte')) and not key.startswith(field_name):
                self.fields[key] = forms.DateField(label='', widget=forms.HiddenInput(attrs={'id':'%s_%s'%(key, field_name)}),required=False)
            if not key.endswith('__lte') and not key.endswith('__gte'):
                self.fields[key] = forms.CharField(widget=forms.HiddenInput,required=False)


class DateRangeFilter(admin.filters.FieldListFilter):
    template = 'daterange_filter/filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg_since = '%s__gte' % field_path
        self.lookup_kwarg_upto = '%s__lte' % field_path
        super(DateRangeFilter, self).__init__(
            field, request, params, model, model_admin, field_path)
        self.form = self.get_form(request)

    def choices(self, cl):
        return []

    def expected_parameters(self):
        return [self.lookup_kwarg_since, self.lookup_kwarg_upto]

    def get_form(self, request):
        for k,v in request.GET.iterlists():
            self.used_parameters[k] = v[0]
        return DateRangeForm(data=self.used_parameters,
                             field_name=self.field_path)

    def queryset(self, request, queryset):
        if self.form.is_valid():
            # get no null params
            filter_params = dict(filter(lambda x: (x[0].endswith('__lte') or x[0].endswith('__gte')) and bool(x[1]),
                                        self.form.cleaned_data.items()))
            for p in filter_params.keys():
                if p.endswith('__lte'):
                    filter_params[p] = filter_params[p] + datetime.timedelta(days=1)
            return queryset.filter(**filter_params)
        else:
            return queryset


class DateTimeRangeFilter(admin.filters.FieldListFilter):
    template = 'daterange_filter/filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg_since = '%s__gte' % field_path
        self.lookup_kwarg_upto = '%s__lte' % field_path
        super(DateTimeRangeFilter, self).__init__(
            field, request, params, model, model_admin, field_path)
        self.form = self.get_form(request)

    def choices(self, cl):
        return []

    def expected_parameters(self):
        return [self.lookup_kwarg_since, self.lookup_kwarg_upto]

    def get_form(self, request):
        for k,v in request.GET.iterlists():
            self.used_parameters[k] = v[0]
        return DateTimeRangeForm(data=self.used_parameters,
                                 field_name=self.field_path)

    def queryset(self, request, queryset):
        if self.form.is_valid():
            # get no null params
            filter_params = dict(filter(lambda x: (x[0].endswith('__lte') or x[0].endswith('__gte')) and bool(x[1]),
                                        self.form.cleaned_data.items()))
            return queryset.filter(**filter_params)
        else:
            return queryset


# register the filters
admin.filters.FieldListFilter.register(
    lambda f: isinstance(f, models.DateField), DateRangeFilter)
admin.filters.FieldListFilter.register(
    lambda f: isinstance(f, models.DateTimeField), DateTimeRangeFilter)
