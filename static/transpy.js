$(document).ready(function(){

    $('form[name=myform]').submit(function(e){
        e.preventDefault();

        let depature = $('#dept-state option:selected').text(),
            destination = $('#dest-state option:selected').val(),
            depature_date = $('#date-input').val(),
                number = $('#number option:selected').val(),
                seat = $('input[name=seat]:checked').val(),
                creditCard = $('input[name=creditCard]').val()

        console.log(depature,destination,number, seat, creditCard, depature_date)

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
