/* Criando um módulo de aplicação para o aplicativo, observe que o nome AppTheClub é o nome que defini para o meu aplicativo.*/
var app = angular.module("AppTheClub", ["ngAnimate"]);
/*SIMULANDO A LATENCIA DA INTERNET E O TEMPO DE CARREGAMENTO. Note que não irei declarar o ngApp no inicio da página mestre do projeto pois iremos inciá-lo nesta função, que também da vida a nossa tela de carregamento:*/
setTimeout(
     function asyncBootstrap() {
         angular.bootstrap(document, ["AppTheClub"]);
              },
         (3 * 1000)//basta trocar o 3 para aumentar o                      //tempo que a tela de pré-carregamento                       //é exibida.
         );
/* Esta função controla a raiz da aplicação, ela apenas exibe uma mensagem no Console do navegador dizendo que o aplicativo carregou corretamente:*/
app.controller(
    "AppController",
    function ($scope) {
        console.log("Aplicativo Carregado! ", $scope);
    }
);
/* Esta classe CSS controla o efeito que anima a tela de pré-carregamento quando ela termina de carregar:*/

app.directive(
    "mAppLoading",
    function ($animate) {
        return ({
            link: link,
            restrict: "C"
        });
/* Esta função vincula os eventos JavaScript ao scope.*/
        function link(scope, element, attributes) {
           /* NOTE: Estou utilizando o .eq(1) para não estilizar o Style block.*/
            $animate.leave(element.children().eq(1)).then(
                function cleanupAfterAnimation() {
                    element.remove();
                    scope = element = attributes = null;
                });}});