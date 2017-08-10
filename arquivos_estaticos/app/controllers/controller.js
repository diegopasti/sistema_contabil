(function() {
 'use strict';
 angular.module('app').controller('CartController', function($scope, $http) {
	$scope.pedido = {
 	itens: [],
 	total: function() {
   	var total = 0;
   	angular.forEach($scope.pedido.itens, function(item) {
     	total += item.qtd * item.preco;
   	})
   	return total;
 	}
	}

	$scope.adicionarItem = function() {
 	var produto = {
   	descricao: 'A guerra dos tronos - The Board Game',
   	preco: 150.0,
   	qtd: 1
 	}

 	$http.post('/adicionar/', {item: produto})
   	.success(function(data) {
     	$scope.pedido.itens = data;
   	})
	}

	$scope.excluirItem = function(index) {
 	$http.post('/excluir/' + index)
   	.success(function(data) {
     	$scope.pedido.itens = data;
   	})
	}
 });
})();