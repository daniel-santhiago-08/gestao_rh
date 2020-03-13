// INICIALIZAÇAO DA PÁGINA
$(function() {

    // INICIALIZAÇÃO DE VARIÁVEIS
    var etapa = 'inicial';
    var filter_element_id = "#filters-list";

    // REQUISIÇÃO PARA OBTER A LISTA DE CAMPOS DO MODELO
    result = get_fields_ajax(url)
    result[0] = fields_dictionary
    result[1] = rows_per_page
    result[2] = order_by
    result[3] = filtered_fields
    result[4] = fillObject
    result[5] = date_field

    filters_dictionary = get_fields_dictionary(
                            filtered_fields,
                            fields_dictionary)

    // CRIAÇÃO DO FILTRO
    createFilter(filters_dictionary, filter_element_id)

    ajax_call(etapa, url, rows_per_page, order_by, filter_element_id, fillObject, date_field)


    // FILTROS
    filters = $(filter_element_id).find("input")
    $.each(filters,function(key,filter) {
        $("#"+filter['id']).bind('change keyup', function(e) {
            ajax_call(etapa, url, rows_per_page, order_by,filter_element_id, fillObject, date_field)
        })
    });

   // PAGINAÇÃO
    $('.btn-group button').on('click', function(e) {
        etapa = 'pagination';
        $('.btn-group button').not(this).removeClass("active");
        $(this).addClass("active");

        ajax_call(etapa, url, rows_per_page, order_by, filter_element_id, fillObject, date_field)

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
        ajax_call(etapa, url, rows_per_page, order_by, filter_element_id, fillObject, date_field)
    });


});


//function ajax_call(etapa, url, rows_per_page, order_by, filter_element_id, fillObject, date_field){
//
//    filters = $(filter_element_id).find("input");
//    json_filters = {}
//    $.each(filters, function(key,data) {
//        json_filters[data['id']] = data['value']
//    })
//
//    $.ajax({
//    type: 'POST',
//    url: url,
//    data: {
//        csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
//        filter_values: JSON.stringify(json_filters),
//        rows_per_page: rows_per_page,
//        current_page: $('.btn-group button.active').text(),
//        order_by: order_by
//    },
//    success: function(result){
//        if (etapa == 'inicial') {
//
////            $('#data_de_extracao_inicial_search').attr('value', result['min_date']);
//            $('#'+date_field+'_inicial_search').attr('value', result['min_date']);
////            $('#data_de_extracao_inicial_search').attr('value', result['min_date']);
//            $('#'+date_field+'_final_search').attr('value', result['max_date']);
//        }
//        result_actions(result, order_by, fillObject)
//    }
//    });
//}
