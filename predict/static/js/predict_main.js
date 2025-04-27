document.addEventListener('DOMContentLoaded', function() {
    var button = document.getElementById('myButton');
    var text = document.getElementById('display');
    var date1 = document.getElementById('date1');
    var date2 = document.getElementById('date2');
    var csrf = document.getElementById('csrf');
    button.addEventListener('click', function() {
        // const xhr = new XMLHttpRequest();
        const url = 'predict'; // データ送信先のURL
        var date1 = document.getElementById('date1').value;
        var date2 = document.getElementById('date2').value;
        let formdata = new FormData()
        // formdata.append('date1',12)
        // formdata.append('date2',15)

        const data = { date1: date1, date2: date2 }; // 送信するデータ
        const xhr = new XMLHttpRequest();
        xhr.open("POST", url);
        xhr.send(JSON.stringify(data));
        // xhr.responseType = "json";
        xhr.onload = () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            const data = xhr.response;
            console.log(data);
        } else {
            console.log(`Error: ${xhr.status}`);
        }
        };
    });
});