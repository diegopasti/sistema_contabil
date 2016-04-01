function desabilitar_botao(botao_id){
	$(botao_id).prop("disabled", true);
}

function habilitar_botao(botao_id){
	$(botao_id).prop("disabled", false);
}

function desmarcar_linha_selecionada(datatable_id){
	alert("Vim aqui ou nao?");
	var table = $(datatable_id).DataTable();
	table.$('tr.selected').removeClass('selected');
}

function configurar_datatable_selecionavel(datatable,botao_apagar,tem_dados){
	
	var table = $(datatable).DataTable();
	
    $(datatable+' tbody').on( 'click', 'tr', function () {
    	
    	//habilitar_botao(botao_apagar);
    	
    	if (tem_dados){
    		//alert("Tem dados armazenados ainda");
    		if ($(this).hasClass('selected') ) {
                $(this).removeClass('selected');
                desabilitar_botao(botao_apagar);
            }
            else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
                habilitar_botao(botao_apagar);
            }
    	}
    	
    	else{
    		desabilitar_botao(botao_apagar);
    	}
    } );
}


function excluir_item_protocolo(datatable_id,botao_id){
	
	$.confirm({
		title: "Excluir Documento",
	    text: "Deseja mesmo excluir esse Documento?",
	    confirmButton: "Excluir",
	    cancelButton: "Cancelar",
	    confirmButtonClass: "btn-danger pull-right",
	    cancelButtonClass: "btn-default botao_desabilitado",
	    
	    confirm: function() {
	    	//var table = $(datatable_id).DataTable();	    	
	    	//desabilitar_botao(botao_id);	 
	    	alert("O cara clicou em sim");
	    	return true;
	    	
	    },
	    
	    cancel: function(){
	    	alert("O cara clicou em não");
	    	return false;
	    }
	    
	});
	
	
	
	
}




function configurar_datatable_padrao(datatable_id){
	
	$(datatable_id).DataTable({
		responsive: true,
		"bPaginate": false,
		"lengthMenu": [[10, 100, -1], [10, 100, "All"]],
		"dom": '<"top">rt"<"rightcolumn"p><"clear">',
		"bSort": false,
		"ordering": false,
		"bAutoWidth": false,
		"bFilter": false,
		"aoColumns": [
	        { "sWidth": "null" },
	        { "sWidth": "60px"},  
	        { "sWidth": "60px"},
	        { "sWidth": "60px"}
	        ]
	});
}

