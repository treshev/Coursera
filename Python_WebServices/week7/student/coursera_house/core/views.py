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

    def get_context_data(self, **kwargs):
        context = super(ControllerView, self).get_context_data()
        context['data'] = smart_home_manager()

        settings = Setting.objects.all()
        result = {}
        for setting in settings:
            result[setting.controller_name] = setting.value

        result["bedroom_light"] = context['data']['bedroom_light']
        result["bathroom_light"] = context['data']['bathroom_light']
        form = ControllerForm(initial=result)
        context['form'] = form

        print("ALTR IN CONTEXT #############################")
        return context

    def get_initial(self):
        print("ALTR GET_INITIAL #############################")
        return {}

    def form_valid(self, form):
        return super(ControllerView, self).form_valid(form)

    def post(self, request, *args, **kwargs):

        settings = Setting.objects.filter(controller_name__in=['bedroom_target_temperature', 'hot_water_target_temperature'])
        for param in settings:
            param.value = request.POST[param.controller_name]
            param.save()

        data = smart_home_manager()
        form = self.form_class(request.POST)
        return render(request, self.template_name, {'form': form, 'data': data})
