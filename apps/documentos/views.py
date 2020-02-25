from django.shortcuts import render
from django.urls import reverse

from .models import Documento
from django.views.generic import (
    CreateView
)


class DocumentoCreate(CreateView):
    template_name = 'documentos/documento_form.html'
    model = Documento
    fields = ['descricao','arquivo']

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.instance.pertence_id = self.kwargs['funcionario_id']

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # def get_queryset(self):
    #     funcionario_selecionado = self.kwargs['funcionario_id']
    #     queryset = Documento.objects.filter(pertence=funcionario_selecionado)
    #     return queryset


