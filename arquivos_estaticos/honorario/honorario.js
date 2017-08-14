function configurar_formulario_padrao(){
	$("#tipo_cliente").val('PJ')
	$("#plano").val(1)
	$("#tipo_honorario").val('FIXO')
	$("#tipo_vencimento").val('MENSAL')
	$("#dia_vencimento_contrato").val('5')
	configurar_campo_data('vigencia_inicio')
	configurar_campo_data('vigencia_fim')
	configurar_campo_data('data_vencimento_contrato')
	configurar_campo_data('desconto_inicio')
	configurar_campo_data('desconto_fim')
	$("#honorario").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});
	$("#total").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});

	desabilitar('group_data_venvimento')
	desabilitar('group_taxa_honorario')
	desabilitar('group_total')



	//$("#group_data_venvimento").addClass('desabilitado')
}

function resetar_formulario(){
	configurar_formulario_padrao()
	$("#vigencia_inicio").val('')
	$("#vigencia_fim").val('')
	$("#data_vencimento").val('')
	$("#taxa_honorario").val('')
	$("#honorario").val('')
	$("#desconto_inicio").val('')
	$("#desconto_fim").val('')
	$("#desconto_temporario").val('')
	$("#total").val('')
	$('#modal_adicionar_contrato').modal('hide');
}

/*	Funções de eventos	*/
function verificar_tipo_vencimento () {
	var tipo_vencimento = $('#select_tipo_vencimento option:selected').val();
	if (tipo_vencimento == 'ANUAL'){
		$("#dia_vencimento_contrato").val('')
		desabilitar('group_dia_vencimento');
		habilitar('group_data_venvimento');
	}else{
		$("#dia_vencimento_contrato").val('5')
		desabilitar('group_data_venvimento');
		habilitar('group_dia_vencimento')
	}
}

function verificar_tipo_honorario () {
	var tipo_vencimento = $('#select_tipo_honorario option:selected').val();
	if (tipo_vencimento == 'VARIAVEL'){
		habilitar('group_taxa_honorario');
	}else{
		$('#taxa_honorario').val('')
		$('#honorario').val('')
		desabilitar('group_taxa_honorario')

	}
}

function calcular_honorario() {
	var salario_vigente = angular.element(document.getElementById('controle_angular')).scope().salario_vigente;
	salario_vigente = parseFloat(salario_vigente.replace('R$ ','').replace('.','').replace(',','.'));
	var multiplicador = $('#taxa_honorario').val()
	if (multiplicador != ''){
		var total = salario_vigente * parseFloat(multiplicador)
		$('#honorario').val(total)
	}
}

function calcular_total (){
	var honorario = $('#honorario').val();
	var desconto = $('#desconto_temporario').val();
	if (!(honorario == '') && !(desconto == '')) {
		honorario = parseFloat(honorario.replace('R$ ', '').replace('.', '').replace(',', '.'));
		desconto = parseFloat(desconto.replace('% ', '').replace('.', '').replace(',', '.'));
		var total = Math.floor([honorario * (1 - (desconto / 100))] *100)/ 100.0
		$('#total').val('R$ '+total);
	}
}


/*	Funções de validar no final	*/
function verificar_data_vigencia(inicio, fim) {
	//alert('venho aqui?')
	var data_inicio = $('#' + inicio).val();
	var data_fim = $('#' + fim).val();
	var retorno = false
	if (!((data_inicio && data_fim) == ('__/__/____' || '') )) {
		var Compara01 = parseInt(data_inicio.split("/")[2].toString() + data_inicio.split("/")[1].toString() + data_inicio.split("/")[0].toString());
		var Compara02 = parseInt(data_fim.split("/")[2].toString() + data_fim.split("/")[1].toString() + data_fim.split("/")[0].toString());
		if (Compara01 < Compara02 || Compara01 == Compara02) {
			retorno = true;
		}
	}
	return retorno;
}


