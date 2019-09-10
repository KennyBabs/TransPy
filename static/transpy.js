$(document).ready(function(){

    $('#dest-state').change(function(){

        let arrival = $('#dest-state option:selected').text()
        
        $.get("/checkprice?arrival="+arrival, function(data){
            $('#amount p').html(data);
            $('.amountFee').show();   
        })
    })

})
