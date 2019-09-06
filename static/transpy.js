$(document).ready(function(){

    $('#dest-state').change(function(){

        let arrival = $('#dest-state option:selected').text()

        $.get("/checkprice?="+arrival, function(data){
            $('#amount p').html(data);
            $('#amount p').show();
        })
    })

    $('form[name=myform]').submit(function(e){
        e.preventDefault();

        let depature = $('#dept-state option:selected').text(),
            destination = $('#dest-state option:selected').text(),
            depature_date = $('#date-input').val(),
            number = $('#number option:selected').val(),
            seat = $('input[name=seat]:checked').val(),
            creditCard = $('input[name=creditCard]').val()

        $.ajax({
            url : "/seatselect",
            method: "POST",
            contentType: "application/json, charset-utf-8",
            data: JSON.stringify({
            depature :depature,
            destination :destination,
            depatrure_date: depature_date,
            number: number,
            seat : seat,
            creditCard : creditCard }),
            success: function(data){
                console.log(data)
            }
        })
    })

})
