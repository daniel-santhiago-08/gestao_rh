function utilizouHoraExtra(id){
    console.log(id);
    alert("Funcionou");
    token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    $.ajax({
        type: 'POST',
        url: '/horas-extras/utilizou-hora-extra/' + id + '/',
        data: {
            csrfmiddlewaretoken: token,
            outro_param: 123
        },
        success: function(result){
            console.log(result);
            $("#mensagem").text(result.mensagem);
            $("#horas_atualizadas").text(result.horas);
        }
    });
}