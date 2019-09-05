$(function(){
    $('form').submit(function(e){
        e.preventDefault();
        let formData = {
            'depature' : $('#dept-state option:selected').text(),
            'destination' : $('#dest-state option:selected').text(),
            'depatrure-date': $('#date-input').val(),
            'number': $('#number option:selected').text(),
            'seat' : $('input[name=seat]:checked').val(),
            'creditCard' : $('input[name=creditCard]').val()
        }
       

        $.ajax({
            url : "/booking",
            method: "POST",
            data: formData,
            success: function(data){
                console.log(data)
            }
        })
    })

})
