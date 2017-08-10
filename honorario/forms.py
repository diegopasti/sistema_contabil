# -*- encoding: utf-8 -*-
from entidade.formularios import MENSAGENS_ERROS
from servico.models import Plano
from django import forms


class FormContrato(forms.Form):
    opcoes_tipos_contratos = (('PF', 'PESSOA FÍSICA'), ('PJ', 'PESSOA JURÍDICA'))

    tipo_contrato = forms.ChoiceField(
        label="Tipo de Contrato*", choices=opcoes_tipos_contratos, required=True,error_messages=MENSAGENS_ERROS,
        widget=forms.Select(
            attrs={
                'id': 'tipo_cliente', 'class': "form-control", 'ng-model':'tipo_cliente'
            }
        )
    )

    contrato_inicio = forms.DateField(
        label="Início do Contrato", required=False, error_messages=MENSAGENS_ERROS,
        widget=forms.TextInput(
            attrs={
                'id': 'contrato_inicio', 'class': "form-control", 'ng-model':'contrato_inicio'
            }
        )
    )

    contrato_fim = forms.DateField(
        label="Fim do Contrato", required=False, error_messages=MENSAGENS_ERROS,
        widget=forms.TextInput(
            attrs={
                'class': "form-control", 'id': 'contrato_fim', 'ng-model':'contrato_fim'
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

    valor_base = forms.CharField(
        label="Honorário*", max_length=30, required=True, error_messages=MENSAGENS_ERROS,
        widget=forms.TextInput(
            attrs={
                'class': "form-control uppercase", 'id': 'valor_base', 'ng-model': 'valor_base'
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

    valor_honorario = forms.DecimalField(
        label="Total (R$)", max_digits=6, decimal_places=2, required=False, error_messages=MENSAGENS_ERROS,
        widget=forms.TextInput(
            attrs={
                'id': 'valor_honorario','class': "form-control", 'ng-model':'valor_honorario'
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
        label="Desconto Temporário (%)", max_digits=5, decimal_places=2, error_messages=MENSAGENS_ERROS,
        widget=forms.TextInput(
            attrs={
                'id': 'desconto_temporario', 'class': "form-control decimal", 'ng-model':'desconto_temporario'
            }
        )
    )

    desconto_inicio = forms.DateField(
        label="Início do Desconto", required=False, error_messages=MENSAGENS_ERROS,
        widget=forms.TextInput(
            attrs={'id': 'desconto_inicio', 'class': "form-control", 'ng-model':'tipo_cliente'}
        )
    )

    desconto_fim = forms.DateField(
        label="Término do Desconto", required=False, error_messages=MENSAGENS_ERROS,
        widget=forms.TextInput(
            attrs={
                'id': 'desconto_fim', 'class': "form-control", 'ng-model':'tipo_cliente'
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
            if form_data['contrato_fim'] < form_data['contrato_inicio']:
                self._errors["contrato_fim"] = ["Fim do Contrato: Data não pode ser anterior ao inicio do contrato."]  # Will raise a error message
                del form_data['contrato_fim']
        return form_data
