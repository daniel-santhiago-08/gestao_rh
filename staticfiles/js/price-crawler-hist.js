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
    filters_dictionary = get_fields_dictionary(
                            filtered_fields,
                            fields_dictionary)


    // CRIAÇÃO DO FILTRO
    createFilter(filters_dictionary, filter_element_id)

    ajax_call(etapa, url, rows_per_page, order_by)


    // FILTROS
//    $.each(filters_dictionary, function(key,filter) {
    $.each(filters_dictionary, function(key,filter) {
        etapa = 'filtro';
        object_id = "#"+filter['field_name']+"_search"

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

//function get_fields_ajax(url){
//
//    var filters_dictionary;
//
//    $.ajax({
//    async: false,
//    type: 'POST',
//    url: url,
//    data: {
//        csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
//        etapa: 'inicial'
//    },
//    success: function(result){
//        fields_json = result;
//
//        var dict = []
//        for (i=0; i<fields_json['field_name'].length; i++){
//
//            dict[i] = {
//             'field_name': fields_json['field_name'][i],
//             'label_name': fields_json['label_name'][i],
//             'fields_type': fields_json['fields_type'][i],
//             'type': fields_json['type'][i]}
//            }
//
//        filters_dictionary = dict
//        }
//    });
//
//    return filters_dictionary;
//
//
//}

function ajax_call(etapa, url, rows_per_page, order_by){


    $.ajax({
    type: 'POST',
    url: url,
    data: {
        csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
        pesquisa_produto: $('#produto_search').val(),
        pesquisa_loja: $('#loja_search').val(),
        pesquisa_data_inicial: $('#data_de_extracao_inicial_search').val(),
        pesquisa_data_final: $('#data_de_extracao_final_search').val(),
        rows_per_page: rows_per_page,
        current_page: $('.btn-group button.active').text(),
//        teste_param: values ,
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
//    num = result['num'];
    first_page = result['first_page'];
    previous_page = result['previous_page'];
    current_page = result['current_page'];
    next_page = result['next_page'];
    last_page = result['last_page'];
    fields_list = result['fields_list'];

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
    createFillTable(object_list, fields_list, order_by, date_field)

}




//function createFilter(filters_dictionary, filter_element_id ){
//
//
//    $.each(filters_dictionary, function (index, filter_field) {
//
//        console.log(filter_field.field_name)
//        console.log(filter_field.type)
//
//        if ( filter_field.type == 'date'){
//            input_group_id = "input-group-"+filter_field.field_name+"_inicial"
//            input_group = $("<div id="+input_group_id+" class='input-group input-group-sm mb-2'></div>").text('');
//            $(filter_element_id).append(input_group);
//
//            ig_prepend_id = "input-group-prepend-"+filter_field.field_name+"_inicial"
//            ig_prepend_class = "input-group-prepend justify-content-center mb-1"
//            input_group_prepend = $("<div id="+ig_prepend_id+" class='"+ig_prepend_class+"' style='width: 100%;'></div>").text('');
//            $("#"+input_group_id).append(input_group_prepend);
//
//            input_group_text_id = "input-group-text-"+filter_field.field_name+"_inicial"
//            input_group_text = $("<span id="+input_group_text_id+" class='input-group-text'></div>").text(filter_field.label_name+" Inicial");
//            $("#"+ig_prepend_id).append(input_group_text);
//
//
//            input_search_id = filter_field.field_name+"_inicial"+"_search"
//            input_search = $("<input type="+filter_field.type+" id="+input_search_id+" class='form-control'>").text('');
//            $("#"+input_group_id).append(input_search);
//
//            /////////////////////////////////////////////////////////////
//
//            input_group_id = "input-group-"+filter_field.field_name+"_final"
//            input_group = $("<div id="+input_group_id+" class='input-group input-group-sm mb-2'></div>").text('');
//            $(filter_element_id).append(input_group);
//
//            ig_prepend_id = "input-group-prepend-"+filter_field.field_name+"_final"
//            ig_prepend_class = "input-group-prepend justify-content-center mb-1"
//            input_group_prepend = $("<div id="+ig_prepend_id+" class='"+ig_prepend_class+"' style='width: 100%;'></div>").text('');
//            $("#"+input_group_id).append(input_group_prepend);
//
//            input_group_text_id = "input-group-text-"+filter_field.field_name+"_final"
//            input_group_text = $("<span id="+input_group_text_id+" class='input-group-text'></div>").text(filter_field.label_name+" Final");
//            $("#"+ig_prepend_id).append(input_group_text);
//
//
//            input_search_id = filter_field.field_name+"_final"+"_search"
//            input_search = $("<input type="+filter_field.type+" id="+input_search_id+" class='form-control'>").text('');
//            $("#"+input_group_id).append(input_search);
//
//
//        }else{
//            input_group_id = "input-group-"+filter_field.field_name
//            input_group = $("<div id="+input_group_id+" class='input-group input-group-sm mb-2'></div>").text('');
//            $(filter_element_id).append(input_group);
//
//            ig_prepend_id = "input-group-prepend-"+filter_field.field_name
//            ig_prepend_class = "input-group-prepend justify-content-center mb-1"
//            input_group_prepend = $("<div id="+ig_prepend_id+" class='"+ig_prepend_class+"' style='width: 100%;'></div>").text('');
//            $("#"+input_group_id).append(input_group_prepend);
//
//            input_group_text_id = "input-group-text-"+filter_field.field_name
//            input_group_text = $("<span id="+input_group_text_id+" class='input-group-text'></div>").text(filter_field.label_name);
//            $("#"+ig_prepend_id).append(input_group_text);
//
//
//            input_search_id = filter_field.field_name+"_search"
//            input_search = $("<input type="+filter_field.type+" id="+input_search_id+" class='form-control'>").text('');
//            $("#"+input_group_id).append(input_search);
//
//        }
//    })
//}

//
//function createFillTable(object_list,fields_list, order_by, date_field){
//
//    $("#table-fill-header").empty();
//    $("#table-fill-body").empty();
//
//    order_by_column = order_by.replace('-','');
//    if (order_by.search('-')){
//        icon_class = 'fa fa-chevron-up ml-2'
//    }else{
//        icon_class = 'fa fa-chevron-down ml-2'
//    }
//
//    // CRIAÇÃO DO HEADER
//    $.each(object_list.slice(0,1), function (row, data) {
//        table_row = $("<tr></tr>").text('')
//        $("#table-fill-header").append(table_row);
//        $.each(data, function (column, data) {
//            var th_id = "header-".concat(column);
//            var th_style = "'white-space: nowrap; text-transform:capitalize;'"
//            var th_tag = "<th id="+th_id+" style="+th_style+"></th>";
//            if (column == order_by_column){
//                var i_tag = "<i class='"+icon_class+"' style='color: #27A2FC;' id='"+column+"-order'></i>"
//            }else{
//                var i_tag = "<i class='fa fa-chevron-down ml-2' id='"+column+"-order'></i>"
//            }
//
//            var table_head_row = $(th_tag).text(column);
//            var table_head_row_head = $(i_tag).text('');
//
//            $("#table-fill-header tr").append(table_head_row);
//            var th_id = "header-".concat(column);
//            $("#"+th_id).append(table_head_row_head)
//        })
//    })
//    // CRIAÇÃO E PREENCHIMENTO DO BODY
////    $.each(object_list.slice(0,num), function (row, data) {
//    $.each(object_list, function (row, data) {
//        id_row_name = "table-row-".concat(row)
//
//        var table_row = $("<tr id="+id_row_name+" onmouseover='this.style.background=lightgray;'  ></td>").text('');
//        $("#table-fill-body").append(table_row)
//
//        $.each(data, function (column, data) {
//            for (col=0; col < fields_list.length; col++){
//                if (fields_list[col] == column){
//                    id_name = "object_list-".concat(column,'-',row)
//                    var table_data;
//                    if ( column == date_field ){
//                        table_data = $("<td id="+id_name+"></td>").
//                            text(formatDate(data));
//
//                    }else{
//                        table_data = $("<td id="+id_name+"></td>").text(data);
//                    }
//                    $("#"+id_row_name).append(table_data);
//                }
//            }
//        })
//
//    })
//
//}

//
//function formatDate(d) {
//    var date = new Date(d);
//
//    if ( isNaN( date .getTime() ) ) {
//        return d;
//    }else{
//        var month = new Array();
//        month[0] = "Janeiro";
//        month[1] = "Fevereiro";
//        month[2] = "Março";
//        month[3] = "Abril";
//        month[4] = "Maio";
//        month[5] = "Junho";
//        month[6] = "Julho";
//        month[7] = "Agosto";
//        month[8] = "Setembro";
//        month[9] = "Outubro";
//        month[10] = "Novembro";
//        month[11] = "Dezembro";
//
//        day = date.getDate() + 1;
//        if(day < 10){
//            day = "0"+day;
//        }
//    return day + " de "+month[date.getMonth()]+ " de " + date.getFullYear();
//    }
// }

function fill_search_result_object_field_list(object_list, num, current_page, field_list){

    for (j=0; j < field_list.length; j++ ){
        field_name = field_list[j];
//        object_temp='#search-result-object-'.concat(field_name,'-');
        object_temp='#object_list-'.concat(field_name,'-');
        for (i = 0; i < num; i++) {
            object_name = object_temp.concat(i)
            element = (current_page - 1 ) * num + i
            try{
                if (field_name == 'id'){
                    $(object_name).text(object_list[element].id);
                }else if (field_name == 'produto'){
                    $(object_name).text(object_list[element].produto);
                }else if (field_name == 'loja'){
                    $(object_name).text(object_list[element].loja);
                }else if (field_name == 'data_de_extracao'){
                    $(object_name).text(formatDate(object_list[element].data_de_extracao));
                }else if (field_name == 'preco'){
                    $(object_name).text(object_list[element].preco);
                }

            }
            catch(err) {
              $(object_name).text("");
            }
        }
    }

}
