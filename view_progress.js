var display_sales_list = function(tasks){
  $("#record").empty()
        $.each(tasks,function(i,task){
              var row = ""

              var task_view = $("<div>")
              $(task_view).append(task["task"]+ "</div><br>")
              // $(row).append(task_view)
                $("#record").append(task_view)

        })
  }
$(document).ready(function(){
    display_sales_list(tasks)
})
