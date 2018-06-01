from datetime import datetime

from django.shortcuts import render

from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic import (ListView, DetailView,
                                  CreateView,
                                  UpdateView)  # TODO: What is the diffrence between this import and the above?
from djgeojson.views import GeoJSONLayerView

from .forms import ReserveAirspaceForm, AppliedReserveAirspaceUpdateForm
from .models import ReserveAirspace


class ReserveAirspaceMainView(TemplateView):
    template_name = 'applications/includes/reserve_main.html'


class ReserveAirspaceCreateView(CreateView):
    form_class = ReserveAirspaceForm
    model = ReserveAirspace
    template_name = 'applications/create_reserve.html'
    success_url = '/applications/airspace'

    def form_valid(self, form):
        reserveairspace = form.save(commit=False)
        reserveairspace.created_by = User.objects.get(username=self.request.user)  # use your own profile here
        reserveairspace.save()
        return HttpResponseRedirect(self.success_url)

    def get_form_kwargs(self):
        kwargs = super(ReserveAirspaceCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ReserveAirspaceListView(ListView):
    context_object_name = 'my_reserves'
    template_name = 'applications/my_reserve_list.html'

    def get_queryset(self):
        return ReserveAirspace.objects.filter(created_by=self.request.user)


##############################################################################################


# this one will just output all datasets to template
def my_reserve_datasets(request):
    airspace = serialize('geojson', ReserveAirspace.objects.filter(created_by=request.user))
    return HttpResponse(airspace, content_type='json')


# this one you have to pass on a pk in template to access a single instance
def my_airspace_datasets(request, pk):
    my_reserve_airspace = ReserveAirspace.objects.filter(pk=pk)
    path = serialize('geojson', my_reserve_airspace)
    return HttpResponse(path, content_type='json')


################################################################################################


class ReserveAirspaceDetailView(DetailView):
    model = ReserveAirspace
    template_name = 'applications/reserveairspace_detail.html'


class ReserveAirspaceUpdateView(UpdateView):
    template_name = 'applications/update_my_airspace.html'
    model = ReserveAirspace
    form_class = ReserveAirspaceForm


def view_airspace(request):
    airspaces = ReserveAirspace.objects.all()
    return render(request, 'applications/airspaces.html', {'airspaces': airspaces})


class MyModelLayer(GeoJSONLayerView):

    def get_queryset(self):
        a = ReserveAirspace.objects.exclude(expiry=True)
        # a = ReserveAirspace.objects.all()
        for x in a:
            t = datetime.combine(x.start_day, x.end) - datetime.now()
            d = t.total_seconds()
            if (d / 3600) < 0:
                x.expiry = True
                x.save()
        context = a.filter(expiry=False)
        return context


class AppliedReserveAirspaceListView(ListView):
    context_object_name = 'applied_reserves'
    template_name = 'applications/applied_reserve_list.html'

    def get_queryset(self):
        return ReserveAirspace.objects.filter(status=0)


class AppliedReserveAirspaceDetailView(DetailView):
    model = ReserveAirspace
    template_name = 'applications/includes/detail.html'


class AppliedReserveAirspaceUpdateView(UpdateView):
    form_class = AppliedReserveAirspaceUpdateForm
    model = ReserveAirspace
    # template_name = 'applications/applied_reserveairspace_update.html'
    template_name = 'applications/approve.html'
    success_url = '/applications/applied-reserves'


class MyApprovalLettersListView(ListView):
    context_object_name = 'my_approval_letters'
    template_name = 'applications/my_approval_letters_list.html'

    def get_queryset(self):
        return ReserveAirspace.objects.filter(created_by=self.request.user, status=2)


class MyApprovalLettersDetailView(DetailView):
    model = ReserveAirspace
    template_name = 'applications/appoval-letter.html'

########################################################################################
# class LogsUploadCreateView(CreateView):
#     form_class = LogsUploadForm
#     template_name = 'applications/create_log_upload.html'
#     success_url = '/applications/airspace'


# class LogsUploadListView(ListView):
#     model = LogsUpload
#     template_name = 'applications/log_uploads_list.html'
#     context_object_name = 'logs'
