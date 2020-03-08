function get_fields_ajax(url){

    var filters_dictionary;

    $.ajax({
    async: false,
    type: 'POST',
    url: url,
    data: {
        csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
        etapa: 'inicial'
    },
    success: function(result){

        console.log(result);

        fields_json = result['fields_dictionary'];
        rows_per_page = result['rows_per_page'];
        order_by = result['order_by'];
        filtered_fields = result['filtered_fields'];


        var dict = []
        for (i=0; i<fields_json['field_name'].length; i++){

            dict[i] = {
             'field_name': fields_json['field_name'][i],
             'label_name': fields_json['label_name'][i],
             'fields_type': fields_json['fields_type'][i],
             'type': fields_json['type'][i]}
            }

        fields_dictionary = dict
        }
    });

    return [fields_dictionary, rows_per_page, order_by, filtered_fields];


}


function get_fields_dictionary(filtered_fields, fields_dictionary){

    filters_dictionary = []

    for (i=0; i<filtered_fields.length; i++){
        $.each(fields_dictionary, function(key,filter) {
            if (filter.field_name == filtered_fields[i]){
                filters_dictionary[i] = {
                 'field_name':filter.field_name,
                 'label_name': filter.label_name,
                 'fields_type': filter.fields_type,
                 'type': filter.type }
            }
        });
    }

    return filters_dictionary;

}




function createFilter(filters_dictionary, filter_element_id ){


    $.each(filters_dictionary, function (index, filter_field) {

        if ( filter_field.type == 'date'){
            input_group_id = "input-group-"+filter_field.field_name+"_inicial"
            input_group = $("<div id="+input_group_id+" class='input-group input-group-sm mb-2'></div>").text('');
            $(filter_element_id).append(input_group);

            ig_prepend_id = "input-group-prepend-"+filter_field.field_name+"_inicial"
            ig_prepend_class = "input-group-prepend justify-content-center mb-1"
            input_group_prepend = $("<div id="+ig_prepend_id+" class='"+ig_prepend_class+"' style='width: 100%;'></div>").text('');
            $("#"+input_group_id).append(input_group_prepend);

            input_group_text_id = "input-group-text-"+filter_field.field_name+"_inicial"
            input_group_text = $("<span id="+input_group_text_id+"  style='font-weight: bold;' class='input-group-text'></div>").text(filter_field.label_name+" Inicial");
            $("#"+ig_prepend_id).append(input_group_text);


            input_search_id = filter_field.field_name+"_inicial"+"_search"
            input_search = $("<input type="+filter_field.type+" id="+input_search_id+" class='form-control mx-2'>").text('');
            $("#"+input_group_id).append(input_search);

            /////////////////////////////////////////////////////////////

            input_group_id = "input-group-"+filter_field.field_name+"_final"
            input_group = $("<div id="+input_group_id+" class='input-group input-group-sm mb-2'></div>").text('');
            $(filter_element_id).append(input_group);

            ig_prepend_id = "input-group-prepend-"+filter_field.field_name+"_final"
            ig_prepend_class = "input-group-prepend justify-content-center mb-1"
            input_group_prepend = $("<div id="+ig_prepend_id+" class='"+ig_prepend_class+"' style='width: 100%;'></div>").text('');
            $("#"+input_group_id).append(input_group_prepend);

            input_group_text_id = "input-group-text-"+filter_field.field_name+"_final"
            input_group_text = $("<span id="+input_group_text_id+" style='font-weight: bold;' class='input-group-text'></div>").text(filter_field.label_name+" Final");
            $("#"+ig_prepend_id).append(input_group_text);


            input_search_id = filter_field.field_name+"_final"+"_search"
            input_search = $("<input type="+filter_field.type+" id="+input_search_id+" class='form-control mx-2'>").text('');
            $("#"+input_group_id).append(input_search);


        }else{
            input_group_id = "input-group-"+filter_field.field_name
            input_group = $("<div id="+input_group_id+" class='input-group input-group-sm mb-2'></div>").text('');
            $(filter_element_id).append(input_group);

            ig_prepend_id = "input-group-prepend-"+filter_field.field_name
            ig_prepend_class = "input-group-prepend justify-content-center mb-1"
            input_group_prepend = $("<div id="+ig_prepend_id+" class='"+ig_prepend_class+"' style='width: 100%;'></div>").text('');
            $("#"+input_group_id).append(input_group_prepend);

            input_group_text_id = "input-group-text-"+filter_field.field_name
            input_group_text = $("<span id="+input_group_text_id+" style='font-weight: bold;' class='input-group-text'></div>").text(filter_field.label_name);
            $("#"+ig_prepend_id).append(input_group_text);


            input_search_id = filter_field.field_name+"_search"
            input_search = $("<input type="+filter_field.type+" id="+input_search_id+" class='form-control mx-2'>").text('');
            $("#"+input_group_id).append(input_search);

        }
    })
}

function createFillTable(object_list,fields_list,field_names_order, order_by, date_field){

    $("#table-fill-header").empty();
    $("#table-fill-body").empty();

    order_by_column = order_by.replace('-','');
    if (order_by.search('-')){
        icon_class = 'fa fa-chevron-up ml-2'
    }else{
        icon_class = 'fa fa-chevron-down ml-2'
    }

    // CRIAÇÃO DO HEADER

    console.log("Loop object_list");
    console.log(object_list.slice(0,1));
//    field_names_order = ['id','loja','produto','data_de_extracao','preco'];
    var object_list_new_order = JSON.parse(JSON.stringify( object_list, field_names_order , 4));
    console.log(object_list_new_order);

    if ( field_names_order.length > 0){
        object_list = JSON.parse(JSON.stringify( object_list, field_names_order , 4));
    }


    $.each(object_list.slice(0,1), function (row, data) {
        table_row = $("<tr></tr>").text('')
        $("#table-fill-header").append(table_row);
        $.each(data, function (column, data) {
            var th_id = "header-".concat(column);
            var th_style = "'white-space: nowrap; text-transform:capitalize;'"
            var th_tag = "<th id="+th_id+" style="+th_style+"></th>";
            if (column == order_by_column){
                var i_tag = "<i class='"+icon_class+"' style='color: #27A2FC;' id='"+column+"-order'></i>"
            }else{
                var i_tag = "<i class='fa fa-chevron-down ml-2' id='"+column+"-order'></i>"
            }

            var table_head_row = $(th_tag).text(column);
            var table_head_row_head = $(i_tag).text('');

            $("#table-fill-header tr").append(table_head_row);
            var th_id = "header-".concat(column);
            $("#"+th_id).append(table_head_row_head)
        })
    })
    // CRIAÇÃO E PREENCHIMENTO DO BODY
//    $.each(object_list.slice(0,num), function (row, data) {
    $.each(object_list, function (row, data) {
        id_row_name = "table-row-".concat(row)
        bg = "this.style.background='lightgray';"
        mouse_over = "this.bgColor='white'"
        var table_row = $("<tr id="+id_row_name+" onmouseover=\"this.style.background='lightgray';\"  onmouseout=\"this.style.background='';\" ></td>").text('');
        $("#table-fill-body").append(table_row)

        $.each(data, function (column, data) {
            for (col=0; col < fields_list.length; col++){
                if (fields_list[col] == column){
                    id_name = "object_list-".concat(column,'-',row)
                    var table_data;
                    if ( column == date_field ){
                        table_data = $("<td id="+id_name+"></td>").
                            text(formatDate(data));

                    }else{
                        table_data = $("<td id="+id_name+"></td>").text(data);
                    }
                    $("#"+id_row_name).append(table_data);
                }
            }
        })

    })

}


function formatDate(d) {
    var date = new Date(d);

    if ( isNaN( date .getTime() ) ) {
        return d;
    }else{
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
        if(day < 10){
            day = "0"+day;
        }
    return day + " de "+month[date.getMonth()]+ " de " + date.getFullYear();
    }
 }
