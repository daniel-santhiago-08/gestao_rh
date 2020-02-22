from django.shortcuts import render
from django.urls import reverse

from .models import Documento
from django.views.generic import (
    CreateView
)


class DocumentoCreate(CreateView):
    template_name = 'documentos/documento_form.html'
    models = Documento
    fields = ['descricao','arquivo']

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.instance.pertence_id = self.kwargs['funcionario_id']

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # def get_success_url(self):
    #     return reverse('update_funcionarios', args=[self.kwargs['funcionario_id']])


    def get_queryset(self):
        funcionario_selecionado = self.kwargs['funcionario_id']
        queryset = Documento.objects.filter(pertence=funcionario_selecionado)
        return queryset



    # def form_valid(self, form):
    #     funcionario = form.save(commit=False)
    #     username = funcionario.nome.split(' ')[0]+ funcionario.nome.split(' ')[1]
    #     funcionario.empresa = self.request.user.funcionario.empresa
    #     funcionario.user = User.objects.create(username=username)
    #     funcionario.save()
    #     return super(FuncionarioNovo, self).form_valid(form)