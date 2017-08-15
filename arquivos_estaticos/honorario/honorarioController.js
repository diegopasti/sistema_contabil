var app = angular.module('app', ['angularUtils.directives.dirPagination']);

app.controller('MeuController', ['$scope', function($scope) {

	$scope.screen_height = window.innerHeight // screen.availHeight; - PEGA O TAMANHO DA TELA DO DISPOSITIVO
	$scope.screen_width  = window.innerWidth  // PEGA O TAMANHO DA JANELA DO BROWSER

	$scope.screen_desktop = null;
	$scope.screen_notebook = null;
	$scope.screen_tablet = null;
	$scope.screen_phone = null;

	$scope.sortType           = 'codigo';    // set the default sort type
	$scope.sortReverse        = false;  // set the default sort order
	$scope.filter_by          = '1';
	$scope.filter_by_index    = parseInt($scope.filter_by);
	$scope.filter_by_options  = ["codigo","cliente", "plano"];
	$scope.search             = '';     // set the default search/filter term
	$scope.minimal_quantity_rows = [1,2,3,4,5,6,7,8,9]

	$scope.opcao_desabilitada = "desabilitado";
	$scope.registro_selecionado = null;
	$scope.esta_adicionando     = null;

	$scope.reajustar_tela = function (){
		$scope.screen_height = window.innerHeight
		$scope.screen_width  = window.innerWidth

		$scope.screen_desktop = false;
		$scope.screen_notebook = false;
		$scope.screen_tablet = false;
		$scope.screen_phone = false;

		if ($scope.screen_width < 576){
			$scope.screen_phone = true;
		}

		else if ($scope.screen_width < 768){
			$scope.screen_tablet = true;
		}

		else if ($scope.screen_width < 992){
			$scope.screen_notebook = true;
		}
		else if ($scope.screen_width < 1200){
			$scope.screen_desktop = true;
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

				},
				failure: function (data) {
					$scope.contratos = [];
					$scope.desabilitar = 'link_desabilitado';
					alert('Erro! Não foi possivel carregar a lista de serviços');
				}
		});
	}

	$scope.adicionar_contrato = function() {

		var tipo_cliente = $('#select_tipo_cliente option:selected').val()
		alert("VEJA O TIPO: "+tipo_cliente)
		var plano = $('#select_plano option:selected').val()
		var honorario = $('#honorario').val()

		var vigencia_inicio = $("#vigencia_inicio").val()
		var vigencia_fim = $("#vigencia_fim").val()

		var tipo_vencimento = $('#select_tipo_vencimento option:selected').val()
    var dia_vencimento_contrato = $('#select_dia_vencimento option:selected').val()
    var data_vencimento_contrato = $("#data_vencimento_contrato").val()

		var tipo_honorario = $('#select_tipo_honorario option:selected').val()
    var taxa_honorario = $("#taxa_honorario").val()
    var honorario = $('#honorario').val()

    var desconto_inicio = $('#desconto_inicio').val()
    var desconto_fim = $('#desconto_fim').val()
    var desconto_temporario = $('#desconto_temporario').val()
    var total = $('#total').val()

		tipo_cliente ? $('#select_tipo_cliente').removeClass('wrong') :  $('#select_tipo_cliente').addClass('wrong')
		plano ? $('#select_plano').removeClass('wrong') :  $('#select_plano').addClass('wrong')
		honorario ? $('#honorario').removeClass('wrong') :  $('#honorario').addClass('wrong')

		var cliente = $scope.registro_selecionado.cliente_id

		alert(tipo_cliente+" - "+plano+" - "+honorario)
		if(tipo_cliente && plano && honorario){

			var data = {
				cliente: cliente,
				tipo_cliente:tipo_cliente,
				plano:plano,
				honorario:honorario,

				vigencia_inicio:vigencia_inicio,
				vigencia_fim:vigencia_fim,

				tipo_vencimento:tipo_vencimento,
				dia_vencimento_contrato:dia_vencimento_contrato,
				data_vencimento_contrato:data_vencimento_contrato,

				tipo_honorario:tipo_honorario,
				taxa_honorario:taxa_honorario,
				honorario:honorario,

				desconto_inicio:desconto_inicio,
				desconto_fim:desconto_fim,
				desconto_temporario:desconto_temporario,
				total:total
				}


			function validate_function(){
				return true
			}


			function success_function(message) {
				//$scope.registro_selecionado.plano =
				resetar_formulario()
			}

			function fail_function(message) {
				alert("DEU PAU"+message)
			}

			request_api("/api/honorario/salvar_contrato",data,validate_function,success_function,fail_function)

			//limpar form e fechar modal
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
}]);