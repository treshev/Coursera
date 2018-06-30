from django.http import HttpResponse
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
        context = super(ControllerView, self).get_context_data()
        print("### ALTR IN GET_CONTEXT_DATA ###")

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

        if self.devices:
            result["bedroom_light"] = self.devices["bedroom_light"]
            result["bathroom_light"] = self.devices["bathroom_light"]
            context['data'] = self.devices

        form = ControllerForm(initial=result)
        context['form'] = form
        return context

    def get_initial(self):
        print("### ALTR GET_INITIAL ###")

    def form_valid(self, form):
        print("### ALTR FORM_VALID ###")
        self.devices = smart_home_manager()
        form.save()
        if self.devices:
            return super(ControllerView, self).form_valid(form)
        else:
            return HttpResponse(status=502)

    def get(self, request, *args, **kwargs):
        print("### ALTR GET ###")
        self.devices = smart_home_manager()
        if self.devices:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponse(status=502)
