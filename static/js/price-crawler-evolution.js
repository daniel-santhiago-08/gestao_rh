// INICIALIZAÇAO DA PÁGINA
$(function() {

//    $('#first-page').addClass("active");
    // INICIALIZAÇÃO DE VARIÁVEIS
    var etapa = 'inicial';
//    var order_by = "-data_de_extracao";
    var url = '/price-crawler/evolution/';
//    var rows_per_page = 7;
//    var filtered_fields = ['data_de_extracao'];
    var filter_element_id = "#filters-list";

    // REQUiSIÇÃO PARA OBTER A LISTA DE CAMPOS DO MODELO
    result = get_fields_ajax(url)
    result[0] = fields_dictionary
    result[1] = rows_per_page
    result[2] = order_by
    result[3] = filtered_fields
    filters_dictionary = get_fields_dictionary(
                            filtered_fields,
                            fields_dictionary)

    // CRIAÇÃO DO FILTRO
    createFilter(filters_dictionary, filter_element_id)

    ajax_call(etapa, url, rows_per_page, order_by)

    // FILTROS
    $.each(filters_dictionary, function(key,filter) {
        etapa = 'filtro';

        if (filter['type'] == 'text'){

            $("#"+filter['field_name']+"_search").on('keyup', function(e) {
            ajax_call(etapa, url, rows_per_page, order_by)
            });
        }else if (filter['type'] == 'date'){
            $("#"+filter['field_name']+"_inicial_search").on('change', function(e) {
            ajax_call(etapa, url, rows_per_page, order_by)
            });
            $("#"+filter['field_name']+"_final_search").on('change', function(e) {
            ajax_call(etapa, url, rows_per_page, order_by)
            });
        }
    });

   // PAGINAÇÃO
    $('.btn-group button').on('click', function(e) {
        etapa = 'pagination';
        $('.btn-group button').not(this).removeClass("active");
        $(this).addClass("active");

        ajax_call(etapa, url, rows_per_page, order_by)

        id = $(this).attr("id");
        middle_pages = ['previous-page', 'current-page', 'next-page'];
        check = middle_pages.includes(id);
        if (check){
            $(this).removeClass("active");
        }
    });

    // ORDERNAÇÃO
    $('.thead').on('click', 'i.fa' ,function() {
        etapa = 'sort';
        $(".thead").find("i").css('color', 'black');

        field_asc = $(this).attr("id").split('-')[0]

        if (order_by == field_asc){
            order_by = '-'.concat(field_asc);
        }else if (order_by == '-'.concat(field_asc)){
            order_by = field_asc;
        }else{
            order_by = field_asc;
        }
        ajax_call(etapa, url, rows_per_page, order_by)
    });

});



function ajax_call(etapa, url, rows_per_page, order_by){

    $.ajax({
    type: 'POST',
    url: url,
    data: {
        csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
        pesquisa_data_inicial: $('#data_de_extracao_inicial_search').val(),
        pesquisa_data_final: $('#data_de_extracao_final_search').val(),
        rows_per_page: rows_per_page,
        current_page: $('.btn-group button.active').text(),
        order_by: order_by
    },
    success: function(result){
        if (etapa == 'inicial') {
            $('#data_de_extracao_inicial_search').attr('value', result['min_date']);
            $('#data_de_extracao_final_search').attr('value', result['max_date']);
        }
        result_actions(result, order_by)
    }
    });
}


function result_actions(result, order_by){
    console.log(result)
    object_list = result['object_list']
    first_page = result['first_page'];
    previous_page = result['previous_page'];
    current_page = result['current_page'];
    next_page = result['next_page'];
    last_page = result['last_page'];
    fields_list = result['fields_list'];
    field_names_order = result['field_names_order'];

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
        $("#current-page").addClass("active");

    }
    $("#first-page").text(first_page);
    $("#previous-page").text(previous_page);
    $("#current-page").text(current_page);
    $("#next-page").text(next_page);
    $("#last-page").text(last_page);

    date_field = 'data_de_extracao'

    // CRIAÇÃO E PREENCHIMENTO DA TABELA COM JAVASCRIPT
    createFillTable(object_list, fields_list,field_names_order, order_by, date_field)

}
