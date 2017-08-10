# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from honorario.forms import FormContrato


def honorario_page(request):
    form_contrato = FormContrato()
    return render_to_response("honorario/honorario.html",{'formulario_contrato':form_contrato})


def contrato_page(request):
    form_contrato = FormContrato()
    return render_to_response("honorario/contrato.html",{'formulario_contrato':form_contrato})
