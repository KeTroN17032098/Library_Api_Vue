const filters = {
    prettydatetime: function(value) {
        if (value == '') return '';

        var js_date = new Date(value);

        var year = js_date.getFullYear();
        var month = js_date.getMonth() + 1;
        var day = js_date.getDate();
        var hour = js_date.getHours();
        var minute = js_date.getMinutes();
        if (month < 10) {
            month = '0' + month;
        }
        if (day < 10) {
            day = '0' + day;
        }
        if (hour < 10) {
            hour = '0' + hour;
        }
        if (minute < 10) {
            minute = '0' + minute;
        }

        return year + '-' + month + '-' + day + ' ' + hour + ':' + minute;
    }
}

export default filters