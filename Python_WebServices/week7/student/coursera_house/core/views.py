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

        form = ControllerForm(initial=result)
        context['form'] = form
        return context

    def get_initial(self):
        return {}

    def form_valid(self, form):
        return super(ControllerView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        for param in request.POST.keys():
            setting, created = Setting.objects.get_or_create(controller_name=param)
            if created:
                par_value = request.POST[param]
                setting.value = par_value
            setting.save()

        form = self.form_class(request.POST)
        data = smart_home_manager()
        return render(request, self.template_name, {'form': form, 'data': data})
