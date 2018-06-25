import requests
from django.urls import reverse_lazy
from django.views.generic import FormView

from .form import ControllerForm
from .models import Setting


class ControllerView(FormView):
    form_class = ControllerForm
    template_name = 'core/control.html'
    success_url = reverse_lazy('form')

    def get_context_data(self, **kwargs):
        context = super(ControllerView, self).get_context_data()

        headers = {
            'authorization': "Bearer " + Setting.SMART_HOME_ACCESS_TOKEN,
            'content-type': "application/json",
        }
        req = requests.get(Setting.SMART_HOME_API_URL + "user.controller", headers=headers)
        if req.status_code == 200:
            result = {}
            for param in req.json()['data']:
                result[param["name"]] = param["value"]
            context['data'] = result
            return context
        return None

    def get_initial(self):
        return {}

    def form_valid(self, form):
        return super(ControllerView, self).form_valid(form)
