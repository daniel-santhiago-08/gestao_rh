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
            ajax_call(etapa, url, rows_per_page, order_by, filter_element_id, fillObject, date_field)
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

