// window.document.getElementById('id') $('.id')
// window.document.getElementsByClassName('class') $('#class')
// window.addEventListener('click', function) $('#id').on('click', function){
// }
// скрипт, помогающий редактированию корзины

window.onload = function() {
    $('.basket_list ').on('click', 'input[type="number"]', function(event){
        // fetch().then(function())
        var t = event.target;
        $.ajax({
            url: "/basket/edit/" + t.name + "/" + t.value + "/",
            success: function (data) {
                $('.basket_list').html(data.result);
            }
        })
    });
}