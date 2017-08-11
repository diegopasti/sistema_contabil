# -*- encoding: utf-8 -*-
from entidade.formularios import MENSAGENS_ERROS
from honorario.models import Contrato
from servico.models import Plano
from django import forms


class FormContrato(forms.Form):
    opcoes_tipos_contratos = (('PF', 'PESSOA FÍSICA'), ('PJ', 'PESSOA JURÍDICA'))

    tipo_cliente = forms.ChoiceField(
        label="Tipo de Contrato*", choices=opcoes_tipos_contratos, required=True,error_messages=MENSAGENS_ERROS,
        widget=forms.Select(
            attrs={
                'id': 'tipo_cliente', 'class': "form-control", 'ng-model':'tipo_cliente'
            }
        )
    )

    vigencia_inicio = forms.DateField(
        label="Início do Contrato", required=False, error_messages=MENSAGENS_ERROS,
        widget=forms.TextInput(
            attrs={
                'id': 'vigencia_inicio', 'class': "form-control", 'ng-model':'vigencia_inicio'
            }
        )
    )

    vigencia_fim = forms.DateField(
        label="Fim do Contrato", required=False, error_messages=MENSAGENS_ERROS,
        widget=forms.TextInput(
            attrs={
                'class': "form-control", 'id': 'vigencia_fim', 'ng-model':'vigencia_fim'
            }
        )
    )

    #lista_planos = Plano.objects.filter(ativo=True)

    plano = forms.ModelChoiceField(
        label='Plano*',required=True,
        queryset=Plano.objects.filter(ativo=True),empty_label=None,
        widget=forms.Select(
            attrs={
                'class': "form-control", 'id': 'plano', 'ng-model':'plano'
            }
        )
    )

    salario_vigente = forms.CharField(
        label="Salário Minímo",max_length=30,required=False,error_messages=MENSAGENS_ERROS,
        widget=forms.TextInput(
            attrs={
                'class':"form-control uppercase", 'id':'salario_vigente','ng-model':'salario_vigente'
            }
        )
    )

    honorario = forms.CharField(
        label="Honorário*", max_length=30, required=True, error_messages=MENSAGENS_ERROS,
        widget=forms.TextInput(
            attrs={
                'class': "form-control uppercase", 'id': 'honorario', 'ng-model': 'honorario'
            }
        )
    )

    opcoes_tipos_honorario = (('FIXO', 'VALOR EM REAIS'), ('VARIAVEL', 'VALOR EM SALARIOS (%)'))

    tipo_honorario = forms.ChoiceField(
        label="Tipo do Honorário", choices=opcoes_tipos_honorario, initial='VARIAVEL',
        required=False,error_messages=MENSAGENS_ERROS,
        widget=forms.Select(
            attrs={'id': 'tipo_honorario', 'class': "form-control", 'ng-model':'tipo_honorario'}
        )
    )

    taxa_honorario = forms.DecimalField(
        label="Índice / Referência", max_digits=5, decimal_places=2, required=False, error_messages=MENSAGENS_ERROS,
        widget=forms.TextInput(
            attrs={
                'id': 'taxa_honorario','class': "form-control decimal", 'ng-model':'taxa_honorario',
                'ng-blur':'calcular_valor_base()'
            }
        )
    )

    total = forms.DecimalField(
        label="Total (R$)", max_digits=6, decimal_places=2, required=False, error_messages=MENSAGENS_ERROS,
        widget=forms.TextInput(
            attrs={
                'id': 'total','class': "form-control", 'ng-model':'total'
            }
        )
    )

    opcoes_tipos_vencimento = (('MENSAL', 'MENSAL'), ('ANUAL', 'ANUAL'))

    tipo_vencimento = forms.ChoiceField(
        label="Tipo do Vencimento", choices=opcoes_tipos_vencimento,
        required=False, error_messages=MENSAGENS_ERROS,
        widget=forms.Select(
            attrs={'id': 'tipo_vencimento', 'class': "form-control", 'ng-model': 'tipo_vencimento'}
        )
    )

    opcoes_dias = (('5', 'DIA 05'), ('10', 'DIA 10'), ('15', 'DIA 15'), ('20', 'DIA 20'), ('25', 'DIA 25'))

    dia_vencimento = forms.ChoiceField(
        label="Dia do Vencimento", required=False, error_messages=MENSAGENS_ERROS,choices=opcoes_dias,
        widget=forms.Select(
            attrs={
                'id': 'dia_vencimento_contrato','class': "form-control decimal", 'ng-model':'dia_vencimento_contrato'
            }
        )
    )

    data_vencimento = forms.DateField(
        label="Data de Vencimento", required=False, error_messages=MENSAGENS_ERROS,
        widget=forms.TextInput(
            attrs={
                'id': 'data_vencimento_contrato', 'class': "form-control decimal", 'ng-model': 'data_vencimento_contrato'
            }
        )
    )

    desconto_temporario = forms.DecimalField(
        label="Desconto Temporário (%)", required=False, max_digits=5, decimal_places=2, error_messages=MENSAGENS_ERROS,
        widget=forms.TextInput(
            attrs={
                'id': 'desconto_temporario', 'class': "form-control decimal", 'ng-model':'desconto_temporario'
            }
        )
    )

    desconto_inicio = forms.DateField(
        label="Início do Desconto", required=False, error_messages=MENSAGENS_ERROS,
        widget=forms.TextInput(
            attrs={'id': 'desconto_inicio', 'class': "form-control", 'ng-model':'desconto_inicio'}
        )
    )

    desconto_fim = forms.DateField(
        label="Término do Desconto", required=False, error_messages=MENSAGENS_ERROS,
        widget=forms.TextInput(
            attrs={
                'id': 'desconto_fim', 'class': "form-control", 'ng-model':'desconto_fim'
            }
        )
    )

    """
    tipo_contrato = forms.ForeignKey(entidade, default=0)


    desconto_indicacoes = forms.DecimalField("Desconto por Indicações:", max_digits=5, decimal_places=2, null=True,
                                              blank=True)
    cadastrado_por = forms.ForeignKey(entidade, related_name="cadastrado_por", default=0)
    data_cadastro = forms.DateField(auto_now_add=True)
    ultima_alteracao = forms.DateTimeField(null=True, auto_now=True)
    alterado_por = forms.ForeignKey(entidade, related_name="alterado_por", default=0)
    ativo = forms.BooleanField(default=True)
    """

    def clean(self):
        form_data = self.cleaned_data
        if len(self.cleaned_data) == len(self.fields):
            result = self.validar_inicio_fim_contrato()
            result = self.validar_inicio_fim_desconto()
        else:
            print("ERRORS:",self.errors)
            print("VALORES: ",self.data)
        return form_data

    def validar_inicio_fim_contrato(self):
        form_data = self.cleaned_data
        if form_data['desconto_fim'] != None and form_data['desconto_inicio'] != None:
            if form_data['contrato_fim'] < form_data['contrato_inicio']:
                self._errors["contrato_fim"] = ["Encerramento do contrato não pode ser anterior ao inicio do contrato."]  # Will raise a error message
                del form_data['contrato_fim']
                return False
        return True

    def validar_inicio_fim_desconto(self):
        form_data = self.cleaned_data
        if form_data['desconto_fim'] != None and form_data['desconto_inicio'] != None:
            if form_data['desconto_fim'] < form_data['desconto_inicio']:
                self._errors["desconto_fim"] = ["Data de encerramento do desconto não pode ser anterior à data de inicio do desconto."]  # Will raise a error message
                del form_data['contrato_fim']
                return False
        return True

    def form_to_object(self):
        contrato = Contrato()
        for item in self.fields:
            contrato.__dict__[item] = self.cleaned_data[item]
        return contrato
        #contrato.tipo_contrato = self.cleaned_data['tipo_contrato']



