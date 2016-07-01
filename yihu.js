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

//封装一个ajax
$.myajax = function (_url, _data, _success, _error, _loading) {
    if (arguments[3] === void(0) || arguments[3] === '') {
        //错误执行代码
        _error = function () {
        };
    }
    if (arguments[3] === void(0) || arguments[3] === '') {
        //不显示等待
        _loading = false;
    }
    //封装AJAX数据
    var _ajax = {};
    _ajax.url = _url;
    _ajax.data = _data;
    _ajax.timeout = 8000;
    _ajax.type = 'post';
    _ajax.async = true;
    var myart = '';
    //默认开始
    _ajax.beforeSend = function () {
        if (_loading) {
            myart = $.loading("String"==typeof (_loading)?_loading:void(0));
        }
    };
    //默认结束
    _ajax.complete = function () {
        if (_loading) {
            myart.close();
        }
    };
    //AJAX执行成功
    _ajax.success = function (result) {
        _success(result);
    };
    //ajax执行遇到错误
    _ajax.error = function () {
        _error();
    };
    $.ajax(_ajax);
};

 //在当前的URL上增加或者修改参数
$.createUrl = function(param,old_url){
    if(typeof old_url==='undefined'){
        var _url = window.location.href;
    }else{
        var _url = old_url;
    }
    for(i=0;i<param.length;i++){
        var _obj = param[i];
        var _key = _obj.key;
        var _value = _obj.value;
        if(_url.indexOf(_key+'=')===-1){
            if(_url.indexOf('?')===-1){
                //没有任何get
                _url +='?'+_key+'='+_value;
            }else{
                //有get
                _url +='&'+_key+'='+_value;
            }
        }else{
            var _reg = new RegExp(_key+'=([^&#.]*)');
            _url = _url.replace(_reg, _key+'='+_value);
        }
    }
    return _url;
};

$(function () {
    var isAtBtnPageto;
    $('html').on('mouseenter','.btn-pageto', function () {
        isAtBtnPageto = !0;
    });
    $('html').on('mouseleave', '.btn-pageto',function () {
        isAtBtnPageto = !1;
    });
    $("html").delegate(".input-pageto", "focus", function () {
        $(this).parent().addClass("pageto-focus");
    }).delegate(".input-pageto", "blur", function (e) {
        isAtBtnPageto || $(this).parent().removeClass("pageto-focus");
    });

    //自定义跳转页面
    window.pageToUrl = function () {
        var _page_num = parseInt($('#pageToNum').val());
        var _page_count = parseInt($('#pageWidget').attr('data-count'));
        if (_page_num > _page_count) {
            _page_num = _page_count;
        }
        var param = [{'key': 'page', 'value': _page_num}];
        var _url = $.createUrl(param,now_doc_list_url);
        doGetDoctorList(_url);
    };
});

//ajax加载医院列表
var doGetDoctorList = function(url){
    var _url = url;
    var _data = {};
    var _success = function (res) {
        $('#ajaxDoctorList').html(res);
         //改变自定义跳转的HTML
        var html = '<input class="btn-pageto" type="button" value="确定" onclick="pageToUrl()">';
        $('.btn-pageto').replaceWith(html);
        window.now_doc_list_url =  _url;
        //对医生图片错误进行过滤
        checkImgError();
        //加载当日的医生排班
        $('html').trigger("arrange:getList");
    };
    var _error = function(){
        $.alert('系统超时，请稍后重试');
        $('#ajaxDoctorList').html('<div class=" c-hidden c-t-center c-f18 pt50 pb50">\
        <span class="icon icon-list"></span>暂无相关医生\
    </div>');
    };
    
    var _beforesend = function(){
        $('#ajaxDoctorList').html('<div class=" c-hidden c-t-center c-f18 pt50 pb50">\
                <img src="/v3/images/loading/2.gif"/>\
                数据加载中，请稍候...\
        </div>');
    };
    $.ajax({
        'url':_url,
        'data':_data,
        'timeout':8000,
        'type':'post',
        'async':true,
        'beforeSend':_beforesend,
        'success':_success,
        'error':_error
    });
};

//鼠标移过医生列表发生的动作
$(function () {
    $("html").on('mouseenter','.doc-results>li',function () {
        $(this).addClass("hover");
    });
    $("html").on('mouseleave','.doc-results>li',function () {
        $(this).removeClass("hover");
    });
    //弹出擅长的详细
    $('html').on('mouseover','[data-tip]', function () {
        if (!$('.tooltip').length) {
            setDOM(this);
        } else {
            $('.tooltip').find('.pop-info-txt').html('<span class="c-bold">擅长：</span>' + $(this).attr('data-tip'));
        }
        $(this).on('mousemove', function (e) {
            var posX = e.pageX, posY = e.pageY;
            $('.tooltip').css({
                left: posX + 12,
                top: posY - $(this).outerHeight(true) / 2
            }).stop(true, true).fadeIn();
        });
    }).on('mouseout', function (e) {
        $('.tooltip').hide();
    });

    function setDOM(ele) {
        var tempStr = '';
        tempStr += '<div class="pop-info-txt"><span class="c-bold">擅长：</span>' + $(ele).attr('data-tip') + '</div>';
        $('<div>').addClass('tooltip').html(tempStr).prependTo('body');
    }
    ;
});

//AJAX获取本医生当日挂号状态
$(function () {
    var old_boaed_html = '';
    $('html').bind("arrange:getList",function(){
        var doctor_list = $('.doctor-arrange-list');
        var sns = '';
        //获取医生sns列表
        doctor_list.each(function(){
            if(sns!=''){
                sns += ',';
            }
            sns += parseInt($(this).attr('data-sn'));
        });
        var _url = '/DoctorArrange/doGetAllRegListBySns';
        var _data = {'sns': sns, 'hospital_id': hospitalId};
        var _success = function (res) {
            if(res==''){
                $('.doctor-arrange-list').html('');
                return false;
            }
            for(var i=0; i<res.length; i++){
                var info = res[i];
                var sn = info['sn'];
                var html = info['html'];
                var _doctor = $('.doctor-arrange-list[data-sn='+sn+']');
                _doctor.html(html);
                if (_doctor.find('li').size() > 5) {
                    _doctor.parent().before('\
                        <div class="carousel-prev" onclick="Carousel(this,1,0,3)"  style="display: none;" ><i class="left-button-image"></i></div>\
                        <div class="carousel-next" onclick="Carousel(this,0,1,3)"><i class="right-button-image"></i></div>');
                }
            }  
        };
        var _error = function(){
            var _doctor = $('.doctor-arrange-list');
            old_boaed_html = _doctor.eq(0).html();
            var _html = "<li class='arrange_loading_err'>\
                    <a href='javascript:;' class='doc-schedule-tz'>\
                        <span class='doc-schedule-date'><em class='c-f16'>点击<br/>刷新</em></span>\
                        <span class='doc-schedule-stat'>网络超时</span>\
                    </a>\
                </li>";
            _doctor.html(_html);
        };
        $.myajax(_url, _data, _success,_error);
        
    });
    
    //点击重新加载
    $(document).on('click','.arrange_loading_err',function(){
        if(old_boaed_html!==''){
            var _doctor = $('.doctor-arrange-list');
            _doctor.html(old_boaed_html);
        }
       $('html').trigger("arrange:getList"); 
    });
    
    //左右滚动
    window.Carousel = function(obj, left, right, step) {
        var $this = $(obj),
                $carouselList = $this.siblings(".carousel-clip-region").find(".carousel-list"),
                $carouselListLeft = $carouselList.css("left"),
                $carouselItemsLength = $carouselList.children('li').length,
                isLeft = left,
                isRight = right,
                step = step ? step : 3,
                temp;
        if (isLeft) {
            if (!$this.siblings(".carousel-next").is(":visible"))
                $this.siblings(".carousel-next").show();
            temp = Math.floor(parseInt($carouselListLeft) / 95) * 95 + step * 95;
            if (temp >= 0) {
                $carouselList.stop().animate({left: 0}, 300);
                $this.hide();
            }
            else
                $carouselList.stop().animate({left: temp + "px"}, 300);
        }
        if (isRight) {
            if (!$this.siblings(".carousel-prev").is(":visible"))
                $this.siblings(".carousel-prev").show();
            temp = Math.floor(parseInt($carouselListLeft) / 95) * 95;
            if (Math.abs(temp - 5 * 95) >= $carouselItemsLength * 95) {
                $this.hide();
                return;
            }
            else {
                temp = Math.floor(parseInt($carouselListLeft) / 95) * 95 - step * 95;
                $carouselList.stop().animate({left: temp + "px"}, 300);
                if (Math.abs(temp - 5 * 95) >= $carouselItemsLength * 95) {
                    $this.hide();
                }
            }
        }
    };

});

