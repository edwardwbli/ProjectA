 //选中子框的时候
    $('#quick_req .cus-sel-list').on('click', 'li>a', function () {
        close();//关闭弹出窗
        
        var _type = $(this).attr('data-type');
        var _value = $(this).attr('data-value');
        var _id = $(this).attr('data-id');
        var _name = $(this).text();

        if (_type === 'hospital') {
            hospital_input.val(_value);
            hospital_input.attr('data-id', _id);
            $(this).parents('.select_hospital').find('.cus-sel-chosed-txt').text(_name);
            $('html').trigger("quickReg:getDepartment");//激活选中医院事件
        } else if (_type === 'department') {
            department_input.val(_value);
            department_input.attr('data-id', _id);
            $(this).parents('.select_department').find('.cus-sel-chosed-txt').text(_name);
            $('html').trigger("quickReg:getDoctor");//激活选中科室事件  
        } else if (_type === 'doctor') {
            doctor_input.val(_value);
            doctor_input.attr('data-id', _id);
            $(this).parents('.select_doctor').find('.cus-sel-chosed-txt').text(_name);
            $('html').trigger("quickReg:selectDoctor");//激活选中医生事件
        }
		
		
//快速挂号的各种事件
+function () {
    
//    $('html').bind('quickReg:getArrange',function(e,doctor_id){
//        
//    });
    
    //ajax获取医院列表
    $('html').bind('quickReg:getHospital', function (e, area_info) {
        if (_.isUndefined(area_info)) {
            return true;
        }
        var _city_id = area_info.split('|')[1];
        if (_.isUndefined(_city_id)) {
            return true;
        }
        var _url = '/QuickReg/doGetHospitalListByCityId';
        var _data = {'city_id': _city_id};
        var _success = function (res) {
            var _temp = _.template("<% _.each(res, function(item) {%>\
<li><a title='<%=item.hosName%>' href='javascript:;' data-type='hospital' data-id='<%=item.hosGuid%>' data-value='<%=item.hospitalId%>'><%=item.hosName%></a></li>\
<%});%>");
            var _html = _temp({'res': res});
            $('#quick_req .select_hospital .cus-sel-list').find('ul').html(_html);
        };
        $.myajax(_url, _data, _success);
    });
    //ajax获取科室列表
    $('html').bind("quickReg:getDepartment", function () {
        //清空科室和医生
        emptyDepartment();
        emptyDoctor();

        //读取医院id
        var _id = $('input[name="hospital_id"]').val();
        if (_.isUndefined(_id)|| _id === '') {
            $.alert('医院数据错误...');
            return true;
        }
        var _url = '/QuickReg/doGetDepartmentListByHospitalId';
        var _data = {'hospital_id': _id};
        var _success = function (res) {    
        var _temp = _.template("<% _.each(res, function(item) {%>\
<li><a title='<%=item.deptName%>' href='javascript:;' data-type='department' data-id='<%=item.bigDepartmentSn%>' data-value='<%=item.hosDeptId%>'><%=item.deptName%></a></li>\
<%});%>");
            
            var _html = _temp({'res':res});
            //将结果写入科室框
            $('#quick_req .select_department .cus-sel-list').find('ul').html(_html);
        };
        $.myajax(_url, _data, _success);
    });
    //ajax获取医生事件
    $('html').bind("quickReg:getDoctor", function () {
        emptyDoctor();
        //读取科室id
        var _id = $('input[name="department_id"]').val();
        if (_.isUndefined(_id)|| _id === '') {
            $.alert('科室数据错误...');
            return true;
        }
        var _url = '/QuickReg/dogetDoctorListByHospitalDepartId';
        var _data = {'department_id': _id};
        var _success = function (res) {
            var _temp = _.template("<% _.each(res, function(item) {%>\
<li><a title='<%=item.doctorName%>' href='javascript:;' data-type='doctor' data-id='<%=item.doctorUid%>' data-value='<%=item.doctorGuid%>'><%=item.doctorName%></a></li>\
<%});%>");
            var _html = _temp({'res': res});
            //将结果写入医生框
            $('#quick_req .select_doctor .cus-sel-list').find('ul').html(_html);
        };
        $.myajax(_url, _data, _success);
    });
    
    //清空医院
    var _hospital = $('#quick_req .select_hospital');
    var _department = $('#quick_req .select_department');
    var _doctor = $('#quick_req .select_doctor');
    //获取医院、科室、医生的默认值
    var _default_hospital = _hospital.find('.cus-sel-chosed-txt').text();
    var _default_department = _department.find('.cus-sel-chosed-txt').text();
    var _default_doctor = _doctor.find('.cus-sel-chosed-txt').text();
    //获取默认的列表内容
    var _defalut_hospital_list = _hospital.find('.cus-sel-list ul').html();
    var _default_department_list = _department.find('.cus-sel-list ul').html();
    var _default_doctor_list = _doctor.find('.cus-sel-list ul').html();
    //还原医院选择框为默认值
    var emptyHospital = function () {
        _hospital.find('.cus-sel-chosed-txt').text(_default_hospital);
        _hospital.find('.cus-sel-list ul').html(_defalut_hospital_list);
        $('#quick_req input[name="hospital_id"]').val('');
    };
    //还原科室选择框为默认值
    var emptyDepartment = function () {
        _department.find('.cus-sel-chosed-txt').text(_default_department);
        _department.find('.cus-sel-list ul').html(_default_department_list);
        $('#quick_req input[name="department_id"]').val('');
    };
    //还原医生选择框为默认值
    var emptyDoctor = function () {
        _doctor.find('.cus-sel-chosed-txt').text(_default_doctor);
        _doctor.find('.cus-sel-list ul').html(_default_doctor_list);
        $('#quick_req input[name="doctor_id"]').val('');
    };
    
}();
