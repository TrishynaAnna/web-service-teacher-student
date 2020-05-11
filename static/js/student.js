$("button[name='btn_delete_student']").click(function() {

    var data = { student_login : $(this).data('student_login')}

    $.ajax({
      type: 'POST',
      url: "/delete_student",
      data: data,
      dataType: "text",
      success: function(resultData) {
          location.reload();
      }
});
});


$("button[name='btn_edit_student']").click(function() {

    window.location = "edit_student?student_login="+$(this).data('student_login');

});


$("button[name='btn_new_student']").click(function() {

    window.location = "new_student";

});

$("button[name='btn_new_function']").click(function() {

    window.location = "new_function/"+$(this).data('student_login');

});

$("button[name='btn_ban']").click(function() {

    window.location = "ban/"+$(this).data('student_login');

});



$("button[name='btn_unban']").click(function() {

    window.location = "unban/"+$(this).data('person_login');

});
