from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from .form import ControllerForm
from .models import Setting
from .tasks import smart_home_manager


class ControllerView(FormView):
    form_class = ControllerForm
    template_name = 'core/control.html'
    success_url = reverse_lazy('form')
    devices = {}

    def get_context_data(self, **kwargs):
        print("### ALTR get_context_data ###")
        context = super(ControllerView, self).get_context_data()
        devices = self.get_devices()
        if devices:
            context["data"] = devices
        return context

    def get_initial(self):
        print("### ALTR get_initial ###")
        result = {}
        try:
            bedroom_target_temperature = Setting.objects.get(controller_name="bedroom_target_temperature")
        except Setting.DoesNotExist:
            bedroom_target_temperature = Setting.objects.create(controller_name="bedroom_target_temperature", value=21)
        result["bedroom_target_temperature"] = bedroom_target_temperature.value

        try:
            hot_water_target_temperature = Setting.objects.get(controller_name="hot_water_target_temperature")
        except Setting.DoesNotExist:
            hot_water_target_temperature = Setting.objects.create(controller_name="hot_water_target_temperature",
                                                                  value=80)
        result["hot_water_target_temperature"] = hot_water_target_temperature.value

        devices = self.get_devices()
        result["bedroom_light"] = devices["bedroom_light"]
        result["bathroom_light"] = devices["bathroom_light"]

        return result

    def form_valid(self, form):
        return super(ControllerView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        print("### ALTR POST ###")
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            context = {}
            devices = self.get_devices()
            if devices:
                form_params = {
                    "bedroom_target_temperature": form.data["bedroom_target_temperature"],
                    "hot_water_target_temperature": form.data["hot_water_target_temperature"],
                    "bedroom_light": devices["bedroom_light"],
                    "bathroom_light": devices["bathroom_light"]
                }
                updated_form = ControllerForm(initial=form_params)
                context["data"] = devices
                context["form"] = updated_form

                return render(request, self.template_name, context)
            else:
                return HttpResponse(status=502)
        else:
            return HttpResponse(status=400)

    def get_devices(self):
        return smart_home_manager()
