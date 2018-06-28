from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from coursera_house.core.models import Setting
from .form import ControllerForm
from .tasks import smart_home_manager


class ControllerView(FormView):
    form_class = ControllerForm
    template_name = 'core/control.html'
    success_url = reverse_lazy('form')

    def get_context_data(self, **kwargs):
        context = super(ControllerView, self).get_context_data()
        devices = self.get_devices()
        if devices:
            context["data"] = devices
        return context

    def post(self, request, *args, **kwargs):
        print("### ALTR POST ###")
        form = self.form_class(request.POST)

        if form.is_valid():
            context = self.get_context_data()
            if context["data"]:
                context["form"] = form
                return render(request, self.template_name, context)
            else:
                return HttpResponse(code=502)
        else:
            return HttpResponse(code=400)

    def get_initial(self):
        bedroom_target_temperature, created = Setting.objects.get_or_create(
            controller_name="bedroom_target_temperature", value=21)
        hot_water_target_temperature, created = Setting.objects.get_or_create(
            controller_name="hot_water_target_temperature", value=80)

        return {bedroom_target_temperature.controller_name: bedroom_target_temperature.value,
                hot_water_target_temperature.controller_name: hot_water_target_temperature.value}

    def form_valid(self, form):
        return super(ControllerView, self).form_valid(form)

    @staticmethod
    def get_devices():
        return smart_home_manager()


''' 
if form.is_valid():
            for param in settings:
                param.value = request.POST[param.controller_name]
                param.save()
                '''
