//Michaella Schaszberger
// mls2290
// UI Design, HW6
var display_sales_list = function(sales){
      $("#record").empty()

      if(sales.length ==0){
            var row = $("<div class='row'>")
            var col_client = $("<div class='col-md-4'>")
            $(col_client).append("No tasks")
            $("#record").append(row)
      }
      else{
            $.each(sales,function(i,sale){
                  var row = $("<div class ='row'>")

                  var col_salesperson = $("<div class='col-md-2'>")
                  $(col_salesperson).append(sale["Assigned By"]+ "</div>")
                  $(row).append(col_salesperson)

                  var col_client = $("<div class='col-md-2'>")
                  $(col_client).append(sale["Member"] + "</div>")
                  $(row).append(col_client)

                  var col_reams =$("<div class='col-md-6'>")
                  $(col_reams).append(sale["Task"] + "</div>")
                  $(row).append(col_reams)

                  var col_butt = $("<div class='col-md-2'>")
                  var delete_button = $("<button class = 'btn btn_cancel'>X</button>" + "</div>")
                  $(delete_button).click(function(){
                        delete_sale(sale["id"])
                        sales.splice(sales["id"],1)

                  })

                  $(col_butt).append(delete_button)
                  $(row).append(col_butt)
                  $("#record").append(row)
            })
      }
}

var submit_sale = function(){
      var new_sale = {}
    var assigned = $("#assigned").val()

      var clientVar = $("#member").val()
      var reamsVar = $.trim($("#task").val())
    console.log(assigned);
      // if($.trim(clientVar) == ""){
      //       // alert("Client can't be empty!")
      //       // $("#clients").val("")
      //       // $("#clients").focus()
      // }
      // else if(reamsVar == ""){
      //       // alert("The # of reams can't be empty!")
      //       // $("#reams").val("")
      //       // $("#reams").focus()
      // }
      // else if(!$.isNumeric(reamsVar)){
      //       // alert("The # of reams has to be a number!")
      //       // $("#reams").focus()
      // }
      // else{
            new_sale = {
                  "Assigned By": assigned,
                  "Member": clientVar,
                  "Task": reamsVar
            }
            // sales.unshift(new_sale)

            //if it's a new client, add to clients

            //reset focus and value to "entering data state"
            $("#clients").val("")
            $("#reams").val("")
            $("#assigned").focus()
            return new_sale
      // }

}


var save_sale = function(new_sale){
    // var data_to_save = submit_sale()
      var data_to_save = {"Assigned By": new_sale["Assigned By"],
      "Member": new_sale["Member"], "Task": new_sale["Task"]}
    // console.log(data_to_save)
    $.ajax({
        type: "POST",
        url: "add_task",
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify(data_to_save),
        success: function(result){
            // var all_data = result["data"]
              //sales.unshift(data_to_save)
              display_sales_list(sales)
              location.reload()
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }
    });
      // sales.unshift(data_to_save)
}

var delete_sale = function(id){
      console.log(id)
      var to_delete = {"id": id}
      $.ajax({
        type: "POST",
        url: "delete_sale",
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify(to_delete),
        success: function(result){
              console.log(result)
              display_sales_list(sales)
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }
    });
}
$(document).ready(function(){
      display_sales_list(sales)
      $("#submit").click(function(){
            save_sale(submit_sale())
            location.reload()
      });
      $('#task').keypress(function (e) {
        if (e.which == 13) {
            save_sale(submit_sale())
            location.reload()
             return false;
        }
        });
      $("#reams").keypress(function(e){
            if(e.which == 13){
                  save_sale(submit_sale())
                  location.reload()
            }
      });
    display_sales_list(sales)
})
