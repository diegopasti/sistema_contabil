var app = angular.module('app', ['angularUtils.directives.dirPagination']);

app.controller('MeuController', ['$scope', function($scope) {

	$scope.sortType           = 'id';    // set the default sort type
	$scope.sortReverse        = false;  // set the default sort order
	$scope.filter_by          = '1';
	$scope.filter_by_index    = parseInt($scope.filter_by);
	$scope.filter_by_options  = ["codigo","cliente", "plano"];
	$scope.search             = '';     // set the default search/filter term

	$scope.opcao_desabilitada = "desabilitado";
	$scope.registro_selecionado = null;
	$scope.esta_adicionando     = null;

	// Carrega os dados ja cadastrados
	$scope.carregar_servicos_cadastrados = function() {
		$.ajax({
			type: "GET",
				url: "/api/preferencias/servicos/",
				success: function (data) {
					$scope.servicos = data;//Object.keys(data).map(function(_) { return data[_]; }) //_(data).toArray();
					$scope.verificar_servicos();
					$scope.$apply();
				},
				failure: function (data) {
					$scope.servicos = [];
					$scope.desabilitar = 'link_desabilitado';
					alert('Erro! Não foi possivel carregar a lista de serviços');
				}
		});
	}

	$scope.adicionar_contrato = function() {
		var tipo_contrato = $('#tipo_contrato').val()
		var plano = $('#plano').val() //.toUpperCase();
		var valor_honorario = $('#valor_honorario').val()//.toUpperCase();



		if(tipo_contrato && plano && valor_honorario){
			alert('ok')
			/*$.ajax({
				type: "POST",
				url: "/api/preferencias/novo_servico",
				data: {
					servico: servico,
					descricao: descricao,
					csrfmiddlewaretoken: '{{ csrf_token }}'
				},

				success: function (data) {
					var resultado = $.parseJSON(data);
					if (resultado['success'] == true){
						var servico = {
								id: resultado["message"],
								nome: angular.uppercase($scope.modal_servico),
								descricao: angular.uppercase($scope.modal_descricao),
								selecionado: ""
						};

						$scope.servicos.push(servico);
						$scope.$apply();
						$scope.resetar_formulario_servico();
					}

					else{
						alert(resultado["message"]);
					}
				},
				failure: function (data) {
					alert('Erro! Falha na execução do ajax');
				}
			});*/
		}
		else{
		alert("VEJA: "+$('#select_tipo_contrato').val())
		alert($('#select_tipo_contrato option:selected').text());
    alert($('#select_tipo_contrato option:selected').val());

			($('#select_tipo_contrato').val()) ? alert('oi') : alert('xau')
			//var test = $('#select_tipo_contrato').val() == '' : $('#select_tipo_contrato').addClass('wrong') : alert('ok')
			//$('#select_tipo_contrato').addClass('wrong')
			//$('#valor_honorario').addClass('wrong')
		}
		$scope.verificar_servicos();
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

		$scope.verificar_servicos();
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
							return {id: $scope.search};
					case 'descricao':
							//alert("filtrar por descricao");
							return {descricao: $scope.search};
					default:
							return {nome: $scope.search}
			}
	}


	$scope.verificar_servicos = function () {
			if ($scope.servicos == "" || $scope.servicos == []){
					$scope.desabilitar  = 'link_desabilitado';
			}
			else{
					$scope.desabilitar  = '';
			}
	}

	$scope.resetar_formulario_servico = function() {
			$('#modal_adicionar_contrato').modal('hide');
			$('#preferencias').val("");
			$('#descricao').val("");
			$scope.model_servico = "";
			$scope.model_descricao = "";
	}

	$scope.selecionar_linha = function(registro) {
			//alert("veja o index: "+registro.id+"-"+registro.nome);

			if ($scope.registro_selecionado != null){
					//alert("tinha uma linha selecionada, entao tem que desmarcar a anterior pra marcar a nova");
					if (registro.selecionado=='selected'){
							//alert("O cara clicou na linha que ja tava selecionada");
							$scope.desmarcar_linha_selecionada();
							//registro.selecionado = "";
							//$scope.registro_selecionado = null;
							//$scope.opcao_desabilitada = "desabilitado";
					}

					else{
							//alert("O usuario tinha um registro selecionado mas selecionou novo registro: "+registro.id+"-"+registro.nome);
							$scope.desmarcar_linha_selecionada();
							registro.selecionado = "selected";
							$scope.registro_selecionado = registro;
							$scope.opcao_desabilitada = "";
					}
			}

			else{
					//alert("nao tinha nada marcado, vou marcar"+$scope.registro_selecionado);
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
											$scope.servicos.splice($scope.servicos.indexOf($scope.registro_selecionado), 1);
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

			$scope.verificar_servicos();

	}
}]);