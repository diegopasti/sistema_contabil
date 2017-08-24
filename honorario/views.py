from django.shortcuts import render_to_response
from django.template import RequestContext
from honorario.forms import FormContrato, FormIndicacao


def honorario_page(request):
    form_contrato = FormContrato()
    form_indicacao = FormIndicacao()
    return render_to_response("honorario/honorario.html",{'formulario_contrato':form_contrato, 'formulario_indicacao':form_indicacao},context_instance=RequestContext(request))


def contrato_page(request):
    form_contrato = FormContrato()
    return render_to_response("honorario/contrato.html",{'formulario_contrato':form_contrato},context_instance=RequestContext(request))