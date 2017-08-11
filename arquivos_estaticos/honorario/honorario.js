function configurar_formulario_padrao(){
	$("#tipo_cliente").val('PJ')
	$("#plano").val(1)
	$("#tipo_honorario").val('FIXO')
	$("#tipo_vencimento").val('MENSAL')
	$("#dia_vencimento_contrato").val('5')

	$("#vigencia_inicio").mask("99/99/9999");
	$("#vigencia_fim").mask("99/99/9999");
	$("#data_vencimento_contrato").mask("99/99/9999");
	$("#desconto_fim").mask("99/99/9999");
	$("#desconto_inicio").mask("99/99/9999");
	$("#honorario").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});
	$("#total").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});
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

