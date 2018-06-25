import requests
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from .tasks import smart_home_manager

from .form import ControllerForm


class ControllerView(FormView):
    form_class = ControllerForm
    template_name = 'core/control.html'
    success_url = reverse_lazy('form')

    def get_context_data(self, **kwargs):
        print("ALTR get_context_data")
        context = super(ControllerView, self).get_context_data()
        context['data'] = smart_home_manager()
        form = ControllerForm()
        form.load()
        print(form.data)
        context['form'] = form
        print(form)
        return context

    def get_initial(self):
        return {}

    def form_valid(self, form):
        return super(ControllerView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = self.form_class(request.POST)
        return render(request, self.template_name, {'form': form, 'data': smart_home_manager()})
        # return super(ControllerView, self).form_valid(form)
