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

function validate_data_vigencia(){
	alert("vim aqui?")
	var data_inicial = $('#vigencia_inicio');
	var data_fim = $('#vigencia_fim');
	data_inicial = data_inicial.split('/');
	data_fim = data_fim.split('/');
	if(!data_fim === '' && !data_inicial === '') {
		if(data_inicial[2]<data_fim[2]) {
			if (data_inicial[1]<data_fim[1]){
				if (data_inicial[0]<data_fim[0]){
					alert('Data invalida')
				}
			}
		}
	}
}


