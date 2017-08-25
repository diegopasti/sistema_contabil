var app = angular.module('app', ['angularUtils.directives.dirPagination']);

app.controller('MeuController', ['$scope', function($scope) {

	$scope.screen_height = window.innerHeight // screen.availHeight; - PEGA O TAMANHO DA TELA DO DISPOSITIVO
	$scope.screen_width  = window.innerWidth  // PEGA O TAMANHO DA JANELA DO BROWSER

	$scope.screen4 = null;
	$scope.screen3 = null;
	$scope.screen2 = null;
	$scope.screen1 = null;

	$scope.sortType           = 'codigo';    // set the default sort type
	$scope.sortReverse        = false;  // set the default sort order
	$scope.filter_by          = '1';
	$scope.filter_by_index    = parseInt($scope.filter_by);
	$scope.filter_by_options  = ["codigo","cliente", "plano"];
	$scope.search             = '';     // set the default search/filter term
	$scope.minimal_quantity_rows = [1,2,3,4,5,6,7,8,9,10]

	$scope.opcao_desabilitada = "desabilitado";
	$scope.registro_selecionado = null;
	$scope.esta_adicionando     = null;

	$scope.reajustar_tela = function (){
		$scope.screen_height = window.innerHeight
		$scope.screen_width  = window.innerWidth

		$scope.screen5 = false;  // Giant Screen:   1681 or more
		$scope.screen4 = false;  // Larger Screen:  1025 ~ 1680 + 656
		$scope.screen3 = false;  // Large Screen:    769 ~ 1024 + 304
		$scope.screen2 = false;  // Medium Screen:   321 ~ 720 + 240
		$scope.screen1 = false;  // Small Screen:    361 ~ 480 + 120
		$scope.screen0 = false;  // Smaller Screen:    0 ~ 360


		//if ($scope.col_cliente_size){
		//	$scope.col_cliente_size = $scope.col_cliente_size - 50; // PROBLEMA QUANDO 481,482,483,484px no 485 volta ao normal
		//}
		//else{
		//	$scope.col_cliente_size = 100;
		//}


		// QUANDO A TELA TA NO MENOR TAMANHO (304px) A COLUNA CLIENTE TEM 185px. SE EU QUERO UM OFFSET NO FINAL
		//alert("VEJA A COLUNA: "+$scope.col_cliente_size)

		//alert("TEM ALGUMA COISA AQui: "+$scope.col_cliente_size)
		// PROBLEMA QUANDO TO REFRESH NUMA TELA MAIOR DEPOIS DESCO PRA UMA MENOR
		//if(!$scope.col_cliente_size){
		//	$scope.col_cliente_size = $scope.screen_width - ($scope.screen_width*0,6788); // 120

			// 304 -> 185 = 0,6058
			// 360 -> 241 = 0,6694
			// 480 -> 360 = 0,7500
			// 720 -> 497 = 0,6902
			// MEDIA 0,6788
		//}

		//alert("VEJA O TAMANHO (NA RESOLUCAO BAIXA COMECA COM 185px: "+ $scope.col_cliente_size)
		//$scope.col_cliente_size = $('.col-cliente').width();

		if ($scope.screen_width <= 360){
			$scope.screen0 = true;
			//if($scope.screen_width <= $scope.col_cliente_size){
			//	alert("COLUNA SERIA MAIOR QUE A A TELA.. AI VOU ACERTAR.."+$scope.col_cliente_size)
			//	$scope.col_cliente_size = $scope.screen_width - 120;
			//}

			//else{
			//	alert("OLHA AS PROPORÇOES.."+$scope.screen_width+" - "+$scope.col_cliente_size)
			//}
			//$scope.col_cliente_size = $scope.screen_width - 120;
			//$scope.col_cliente_size = $scope.col_cliente_size - 10;
		}

		else if ($scope.screen_width <= 480){
			$scope.screen1 = true;
			//$scope.col_cliente_size = $scope.col_cliente_size - 120;
		}

		else if ($scope.screen_width <= 720){
			$scope.screen2 = true;
			//$scope.col_cliente_size = $scope.col_cliente_size - 10;
		}

		else if ($scope.screen_width <= 1024){
			$scope.screen3 = true;
		}
		else if ($scope.screen_width <= 1268){
			$scope.screen4 = true;
		}
		else{
			$scope.screen5 = true;
		}
		$scope.$apply();
	}

	// Carrega os dados ja cadastrados
	$scope.carregar_clientes = function() {
		$.ajax({
			type: "GET",
				url: "/api/honorario/lista_contratos",
				success: function (data) {

					$scope.contratos = JSON.parse(data);//Object.keys(data).map(function(_) { return data[_]; }) //_(data).toArray();
					//$scope.verificar_contratos();
					$scope.contratos_carregados = true;
					$scope.$apply();
					$scope.reajustar_tela();

				},
				failure: function (data) {
					$scope.contratos = [];
					$scope.desabilitar = 'link_desabilitado';
					alert('Erro! Não foi possivel carregar a lista de serviços');
				}
		});
	}

	/*Carregar Lista Indicacoes*/
	$scope.carregar_indicacao = function () {
		$.ajax({

			type: 'GET',
			url: "/api/honorario/lista_indicacao/" + $scope.registro_selecionado.cliente_id,

			success: function (data) {
				//alert("VEJA A RESPOSTA: "+JSON.stringify(data))
				$scope.registro_selecionado.indicacoes = JSON.parse(data);
				$scope.$apply();
				//alert("VEJA O QUE TEMOS NAS INDICACOES: "+$scope.registro_selecionado.indicacoes[0].cliente_id)
			},
			failure: function (data) {
				$scope.indicacao = [];
				$scope.desabilitar = 'link_desabilitado'
				alert("Não foi possivel carregar a lista de indicacoes")
			}
		});
	}

	$scope.adicionar_indicacao = function () {
		var empresa = $('#indicacao').val()
		var taxa_desconto = $('#taxa_desconto_indicacao').val()
		var cliente_id = $scope.registro_selecionado.cliente_id

		var data = {
			empresa : empresa,
			taxa_desconto : taxa_desconto,
			cliente_id : cliente_id
		}

		function validate_function () {
			if(empresa == '' || taxa_desconto==''){
				alert('Preecha os campos')
				return false
			}
			return true
		}

		function success_function(message) {
			var date = message['fields']["data_cadastro"]
			nova_indicaco = {
				cliente_id: cliente_id,
				indicacao: {
					nome_razao : $('#indicacao option:selected').text(),
					taxa_desconto : taxa_desconto,
					indicacao_ativa : true,
					data_cadastro : date
				}
			}
			$scope.registro_selecionado.indicacoes.push(nova_indicaco)
			$scope.$apply()
		}

		function fail_function() {
			alert('Empresa informada já foi indicada anteriormente')
		}
		//request_api(url,data_paramters,validator_functions,success_function,fail_function){
		request_api("/api/honorario/salvar_indicacao/",data,validate_function,success_function,fail_function)

	}

	$scope.adicionar_contrato = function() {

		var tipo_cliente = $('#select_tipo_cliente option:selected').val()
		var plano = $('#select_plano option:selected').val()
		var honorario = $('#valor_honorario').val()

		var vigencia_inicio = $("#vigencia_inicio").val()
		var vigencia_fim = $("#vigencia_fim").val()

		alert("VEJA AS DATAS: "+vigencia_inicio+" - "+vigencia_fim)

		var tipo_vencimento = $('#select_tipo_vencimento option:selected').val()
    var dia_vencimento = $('#select_dia_vencimento option:selected').val()

    var data_vencimento = $("#data_vencimento").val()

		var tipo_honorario = $('#select_tipo_honorario option:selected').val()
    var taxa_honorario = $("#taxa_honorario").val()
    var valor_honorario = $('#valor_honorario').val().replace(".","").replace(",",".")

    var desconto_inicio = $('#desconto_inicio').val()
    var desconto_fim = $('#desconto_fim').val()
    var desconto_temporario = parseFloat($('#desconto_temporario').val())


    var total = $('#total').val().replace("R$ ","").replace(".","").replace(",",".")

		tipo_cliente ? $('#select_tipo_cliente').removeClass('wrong') :  $('#select_tipo_cliente').addClass('wrong')
		plano ? $('#select_plano').removeClass('wrong') :  $('#select_plano').addClass('wrong')
		valor_honorario ? $('#valor_honorario').removeClass('wrong') :  $('#valor_honorario').addClass('wrong')

		var cliente = $scope.registro_selecionado.cliente_id
		if(tipo_cliente && plano && valor_honorario){

			var data = {
				cliente: cliente,
				tipo_cliente:tipo_cliente,
				plano:plano,
				valor_honorario:valor_honorario,

				vigencia_inicio:vigencia_inicio,
				vigencia_fim:vigencia_fim,

				tipo_vencimento:tipo_vencimento,
				dia_vencimento:dia_vencimento,
				data_vencimento:data_vencimento,

				tipo_honorario:tipo_honorario,
				taxa_honorario:taxa_honorario,
				valor_honorario:valor_honorario,

				desconto_inicio:desconto_inicio,
				desconto_fim:desconto_fim,
				desconto_temporario:desconto_temporario,
				total:total
				}


			function validate_function(){
				return true
			}


			function success_function(message) {
				//alert("VEJA O RESULT: "+JSON.stringify(message))
				$scope.registro_selecionado.contrato.tipo_cliente = $('#tipo_cliente option:selected').text()
				$scope.registro_selecionado.plano = $('#select_plano option:selected').text()
				$scope.registro_selecionado.contrato.vigencia_inicio = vigencia_inicio
				$scope.registro_selecionado.contrato.vigencia_fim = vigencia_fim
				$scope.registro_selecionado.contrato.valor_honorario = message.fields.valor_honorario
				$scope.registro_selecionado.contrato.desconto_temporario = parseFloat(message.fields.desconto_temporario)


				if (message.fields.desconto_indicacoes!=0){
					$scope.registro_selecionado.contrato.desconto_indicacoes = message.fields.desconto_indicacoes//parseFloat(message.fields.desconto_indicacoes)
				}
				else{
					$scope.registro_selecionado.contrato.desconto_indicacoes = 0
				}

				$scope.registro_selecionado.contrato.desconto_temporario = message.fields.desconto_temporario

				$scope.$apply()
				resetar_formulario()
				$('#modal_adicionar_contrato').modal('hide');
			}

			function fail_function(message) {
				alert("ERRO: "+message)
			}

			request_api("/api/honorario/salvar_contrato",data,validate_function,success_function,fail_function)
		}
		else{
		}
	}

	$scope.alterar_contrato = function() {
		var servico = $('#modal_servico').val().toUpperCase();
		var descricao = $('#modal_descricao').val().toUpperCase();


		if(servico){
			if (confirm('Deseja mesmo alterar esse Serviço?')) {
				$.ajax({
					type: "POST",
					url: "/api/preferencias/alterar_contrato/" + $scope.registro_selecionado.id + "/",
					data: {
						servico: servico,
						descricao: descricao,
						csrfmiddlewaretoken: '{{ csrf_token }}'
					},

					success: function (data) {
						var resultado = $.parseJSON(data);

						if (resultado['success'] == true) {
							$scope.registro_selecionado.nome = servico;
							$scope.registro_selecionado.descricao = descricao;
							$scope.registro_selecionado.selecionado = '';
							$scope.$apply();
							$scope.resetar_formulario_servico();
						}

						else {
							alert(resultado["message"]);
						}
					},
					failure: function (data) {
							alert('Erro! Falha na execução do ajax');
					}
				});
			}

			else{
				e.preventDefault();
			}
		}
		else{
			alert('Erro! Preencha os campos antes de enviar');
		}

		$scope.verificar_contratos();
	}

	$scope.select_filter_by = function (index) {
			$scope.filter_by_index = parseInt($scope.filter_by);
			$scope.apply();
	}

	$scope.get_filter_column = function(){
			var filtrar_pesquisa_por = $scope.filter_by_options[$scope.filter_by_index];
			switch (filtrar_pesquisa_por) {
					case 'codigo':
							//alert("filtrar por codigo");
							return {cliente_id: $scope.search};
					case 'plano':
							//alert("filtrar pelo plano");
							return {plano: $scope.search};
					default:
							return {cliente_nome: $scope.search}
			}
	}


	$scope.verificar_contratos = function () {
			if ($scope.contratos == "" || $scope.contratos == []){
					$scope.desabilitar  = 'link_desabilitado';
			}
			else{
					$scope.desabilitar  = '';
			}
	}

	$scope.selecionar_linha = function(registro) {
			//alert("veja o index: "+registro.cliente_id+"-"+registro.cliente_nome);

			if ($scope.registro_selecionado != null){
					//alert("tinha uma linha selecionada, entao tem que desmarcar a anterior pra marcar a nova");
					if (registro.selecionado=='selected'){
							//alert("O cara clicou na linha que ja tava selecionada");
							$scope.desmarcar_linha_selecionada();
							//registro.selecionado = "";
							$scope.registro_selecionado = null;
							//$scope.opcao_desabilitada = "desabilitado";
					}

					else{
							$scope.desmarcar_linha_selecionada();
							registro.selecionado = "selected";
							$scope.registro_selecionado = registro;
							$scope.opcao_desabilitada = "";
					}
			}

			else{

					registro.selecionado = 'selected';
					$scope.registro_selecionado = registro;
					$scope.opcao_desabilitada = "";
			}
			$scope.apply();
	}

	$scope.desmarcar_linha_selecionada = function(){
			$scope.registro_selecionado.selecionado = "";
			$scope.registro_selecionado = null;
			$scope.opcao_desabilitada = "desabilitado";
			//$scope.apply();
	}

	$scope.configurar_inclusao_servico = function(){
			$scope.esta_adicionando = true;
			$("#titulo_modal_adicionar_contrato").text("Novo Contrato");
			$("#modal_servico").val("");
			$("#modal_descricao").val("");
			$scope.modal_servico = "";
			$scope.modal_descricao = "";
			$scope.apply();
	}

	$scope.configurar_alteracao_servico = function(){
			$scope.esta_adicionando = false;
			$("#titulo_modal_adicionar_contrato").text("Alterar Serviço");
			$("#modal_servico").val($scope.registro_selecionado.nome);
			$("#modal_descricao").val($scope.registro_selecionado.descricao);
	}

	$scope.excluir_servico = function () {
			var servico = $('#modal_servico').val().toUpperCase();
			var descricao = $('#modal_descricao').val().toUpperCase();

			if (confirm('Deseja mesmo excluir esse Serviço?')) {

					$.ajax({
							type: "POST",
							url: "/api/preferencias/excluir_servico/"+$scope.registro_selecionado.id+"/",
							data: {
									servico: servico,
									descricao: descricao,
									csrfmiddlewaretoken: '{{ csrf_token }}'
							},

							success: function (data) {

									var resultado = $.parseJSON(data);

									if (resultado['success'] == true){
											$scope.contratos.splice($scope.contratos.indexOf($scope.registro_selecionado), 1);
											$scope.registro_selecionado = null;
											$scope.opcao_desabilitada = "desabilitado";
											$scope.$apply();
											$scope.resetar_formulario_servico();
											//alert(resultado['message']);
									}

									else{
											alert(resultado["message"]);
									}
							},
							failure: function (data) {
									alert('Erro! Falha na execução do ajax');
							}
					});

					//return true;
			}
			else {
					e.preventDefault();

					//return false;
			}

			$scope.verificar_contratos();

	}

	$scope.get_salario_vigente = function(){
		$.ajax({
			url: '/api/preferencias/salario_vigente/',
			type: 'get', //this is the default though, you don't actually need to always mention it

			success: function(data) {
				$('#form-group-taxa-salario').tooltip({title:"Valor de Referência: "+data.salario_vigencia_atual});
				$scope.salario_vigente = data.salario_vigencia_atual;
				$('#salario_vigente').val(data.salario_vigencia_atual)
				$scope.$apply();
			},

			failure: function(data) {
				alert('Got an error dude');
			}
		});
	}

	$scope.load_fields = function(){
		var plano = $scope.registro_selecionado.plano
		//var tipo_cliente = $scope.registro_selecionado.contrato.tipo_cliente
		alert("plano:		"+plano);
		//$scope.registro_selecionado;
		$scope.esta_adicionando = true;
		$('#plano ').val(plano)
		//$('#tipo_cliente option:selected').val(tipo_cliente)
		$('#vigencia_inicio').val($scope.registro_selecionado.contrato.vigencia_inicio)
		$('#vigencia_fim').val($scope.registro_selecionado.contrato.vigencia_fim)
		$('#dia_vencimento').val($scope.registro_selecionado.contrato.dia_vencimento)
		$("#data_vencimento").val($scope.registro_selecionado.contrato.data_vencimento)
		$('#tipo_honorario').select($scope.registro_selecionado.contrato.tipo_honorario)
		$("#taxa_honorario").val($scope.registro_selecionado.contrato.taxa_honorario)
		$('#valor_honorario').val($scope.registro_selecionado.contrato.valor_honorario *100.0).trigger('mask.maskMoney')
		$('#desconto_inicio').val($scope.registro_selecionado.contrato.desconto_inicio)
		$('#desconto_fim').val($scope.registro_selecionado.contrato.desconto_fim)
		$('#desconto_temporario').val($scope.registro_selecionado.contrato.desconto_temporario)
		calcular_total();
		$scope.apply();
	}

	$scope.load_clientes = function () {
		alert("vindo aqui")
		$.ajax({

			type: 'GET',
			url: "/api/honorario/clientes/" + $scope.registro_selecionado.cliente_id,

			success: function (data) {
				//alert("VEJA A RESPOSTA: "+JSON.stringify(data))
				$scope.registro_selecionado.clientes = JSON.parse(data);
				$scope.$apply();
				//alert("VEJA O QUE TEMOS NAS INDICACOES: "+$scope.registro_selecionado.indicacoes[0].cliente_id)
			},
			failure: function (data) {
				$scope.clientes = [];
				$scope.desabilitar = 'link_desabilitado'
				alert("Não foi possivel carregar a lista de indicacoes")
			}
		});
	}

}]);