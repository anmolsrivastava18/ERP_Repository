/* Project specific Javascript goes here. */
function auto_fill_part_name_uom(url) {
	 // Auto fill Part Name
         var part_name = $('#id_part_name');
         part_name.prop("readonly", true);

         var unit_of_measure = $('#id_unit_of_measure');
         unit_of_measure.prop("disabled", true);

         $("#id_part_number").change(function(e){
            e.preventDefault();
            var part_number = $(this).val();

            $.ajax({
               type : 'GET',
               url :  url,
               data : {"part_number":part_number},
               success : function(response){
                  part_name.val(response.part_name);
                  unit_of_measure.val(response.uom);
                  $('#uom_select_hack').val(response.uom);
               },
               error : function(response){
                  console.error(response);
                  part_name.val("");
                  unit_of_measure.val("");
               }
            })
         })

}
