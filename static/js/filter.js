// INICIALIZAÇAO DA PÁGINA
$(function() {
    // CAPTURANDO O TOKEN PADRÃO
    token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    // ALTERANDO AS CONFIGURAÇÕES PARA O BOTÃO DE PÁGINA 1
    $('.btn-group button').eq(0).addClass("active");
    $('.btn-group button').eq(0).addClass("btn-dark");
    $('.btn-group button').eq(0).removeClass("btn-secondary");
    var btnActive = $('.btn-group button.active');
    var current_page = btnActive.text()

    $.ajax({
    type: 'POST',
    url: '/price-crawler/hist/',
    data: {
        csrfmiddlewaretoken: token,
        pesquisa_produto: $('#produto_search').val(),
        pesquisa_loja: $('#loja_search').val(),
        current_page: current_page
    },
    success: function(result){
        $('#data_inicial_search').attr('value', result['min_date']);
        $('#data_final_search').attr('value', result['max_date']);
        result_actions(result)
    }

    });
});

// FILTRO DE PRODUTO
$('#produto_search').on('keyup', function(e) {
    token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    var btnActive = $('.btn-group button.active');
    var current_page = btnActive.text();

    $.ajax({
    type: 'POST',
    url: '/price-crawler/hist/',
    data: {
        csrfmiddlewaretoken: token,
        pesquisa_produto: $('#produto_search').val(),
        pesquisa_loja: $('#loja_search').val(),
        pesquisa_data_inicial: $('#data_inicial_search').val(),
        pesquisa_data_final: $('#data_final_search').val(),
        current_page: current_page
    },
    success: function(result){
        result_actions(result)
        }
    });
});

// FILTRO DE LOJA
$('#loja_search').on('keyup', function(e) {
    token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    var btnActive = $('.btn-group button.active');
    var current_page = btnActive.text();

    $.ajax({
    type: 'POST',
    url: '/price-crawler/hist/',
    data: {
        csrfmiddlewaretoken: token,
        pesquisa_produto: $('#produto_search').val(),
        pesquisa_loja: $('#loja_search').val(),
        pesquisa_data_inicial: $('#data_inicial_search').val(),
        pesquisa_data_final: $('#data_final_search').val(),
        current_page: current_page
    },
    success: function(result){
        result_actions(result)
        }
    });
});

// FILTRO DE DATA
$('#data_inicial_search').change(function(e) {
    token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    var btnActive = $('.btn-group button.active');
    var current_page = btnActive.text();

    $.ajax({
    type: 'POST',
    url: '/price-crawler/hist/',
    data: {
        csrfmiddlewaretoken: token,
        pesquisa_produto: $('#produto_search').val(),
        pesquisa_loja: $('#loja_search').val(),
        pesquisa_data_inicial: $('#data_inicial_search').val(),
        pesquisa_data_final: $('#data_final_search').val(),
        current_page: current_page
    },
    success: function(result){
        result_actions(result)
        }
    });
});


// FILTRO DE PÁGINA
$('.btn-group button').on('click', function(e) {
    $('.btn-group button').not(this).removeClass("active");
    $('.btn-group button').not(this).removeClass("btn-dark");
    $('.btn-group button').not(this).addClass("btn-secondary");

    $(this).addClass("active");
    $(this).addClass("btn-dark");
    $(this).removeClass("btn-secondary");
    var btnActive = $('.btn-group button.active');
    var current_page = btnActive.text();

    token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    $.ajax({
    type: 'POST',
    url: '/price-crawler/hist/',
    data: {
        csrfmiddlewaretoken: token,
        pesquisa_produto: $('#produto_search').val(),
        pesquisa_loja: $('#loja_search').val(),
        pesquisa_data_inicial: $('#data_inicial_search').val(),
        pesquisa_data_final: $('#data_final_search').val(),
        current_page: current_page
    },
    success: function(result){
        result_actions(result)
        }
    });
});

$('.thead-dark th').on('click', function(e) {
    text = $(this).text();
    alert(text);
});


function result_actions(result){
    console.log(result)
    object_list = result['object_list']
    num = result['num'];
    first_page = result['first_page'];
    previous_page = result['previous_page'];
    current_page = result['current_page'];
    next_page = result['next_page'];
    last_page = result['last_page'];

    if (next_page >= last_page){
        next_page = last_page;
        $("#next-page").addClass("d-none");
    }else{
        $("#next-page").removeClass("d-none");
    }

    if (previous_page <= first_page){
        previous_page = first_page;
        $("#previous-page").addClass("d-none");
    }else{
        $("#previous-page").removeClass("d-none");
    }

    if ((current_page >= last_page) || (current_page <= first_page)) {
        $("#current-page").addClass("d-none");
        if (current_page >= last_page)  {
            current_page = last_page;
        }
        if (current_page <= first_page) {
            current_page = first_page;
        }
    }else{
        $("#current-page").removeClass("d-none");
    }





    $("#first-page").text(first_page);
    $("#previous-page").text(previous_page);
    $("#current-page").text(current_page);
    $("#next-page").text(next_page);
    $("#last-page").text(last_page);
    fill_search_result_object_id(object_list, num, current_page);
    fill_search_result_object_produto(object_list, num, current_page);
    fill_search_result_object_loja(object_list, num, current_page);
    fill_search_result_object_data(object_list, num, current_page);
    fill_search_result_object_preco(object_list, num, current_page);
}



function formatDate(d) {
  var date = new Date(d);

 if ( isNaN( date .getTime() ) )
 {
    return d;
 }
 else
{

  var month = new Array();
  month[0] = "Janeiro";
  month[1] = "Fevereiro";
  month[2] = "Março";
  month[3] = "Abril";
  month[4] = "Maio";
  month[5] = "Junho";
  month[6] = "Julho";
  month[7] = "Agosto";
  month[8] = "Setembro";
  month[9] = "Outubro";
  month[10] = "Novembro";
  month[11] = "Dezembro";

  day = date.getDate() + 1;

  if(day < 10)
  {
     day = "0"+day;
  }

  return day + " de "+month[date.getMonth()]+ " de " + date.getFullYear();
  }

 }

function fill_search_result_object_id(object_list, num, current_page){
    for (i = 0; i < num; i++) {
    object_name='#search-result-object-id-'.concat(i)
    element = (current_page - 1 ) * num + i
    try{
        $(object_name).text(object_list[element].id);
    }
    catch(err) {
      $(object_name).text("");
    }
    }
}
function fill_search_result_object_produto(object_list, num, current_page){
    for (i = 0; i < num; i++) {
    object_name='#search-result-object-produto-'.concat(i)
    element = (current_page - 1 ) * num + i
    try{
    $(object_name).text(object_list[element].produto);
    }
    catch(err) {
      $(object_name).text("");
    }
    }
}
function fill_search_result_object_loja(object_list, num, current_page){
    for (i = 0; i < num; i++) {
    object_name='#search-result-object-loja-'.concat(i)
    element = (current_page - 1 ) * num + i
    try{
    $(object_name).text(object_list[element].loja);
    }
    catch(err) {
      $(object_name).text("");
    }
    }
}
function fill_search_result_object_data(object_list, num, current_page){
    for (i = 0; i < num; i++) {
    object_name='#search-result-object-data-'.concat(i)
    element = (current_page - 1 ) * num + i
    try{
        $(object_name).text(formatDate(object_list[element].data_de_extracao));
    }
    catch(err) {
      $(object_name).text("");
    }
    }
}
function fill_search_result_object_preco(object_list, num, current_page){
    for (i = 0; i < num; i++) {
    object_name='#search-result-object-preco-'.concat(i)
    element = (current_page - 1 ) * num + i
    try{
        $(object_name).text(object_list[element].preco);
    }
    catch(err) {
      $(object_name).text("");
    }
    }
}