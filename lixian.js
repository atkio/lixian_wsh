
$.ajaxSetup({scriptCharset:'utf-8'});

/*******************************
*服务器电文构造(JSON)
	+-msg
	|-log
	|-rst
	|-data
********************************/

/******************************************************
*$.lixian
*	离线定义
*******************************************************/
$.lixian={"cgitimeout":10000, // 超时秒数
		  "startup":false, // CGI启动
		  "logined":false,// 登陆
		  "logInterval":3000}; //log表示频度
	  

// indexpage
$.lixian.page={
	"home":"index.html",
	"task":"task.html",
	"add":"add.html",
	"login":"user.html",
	"env":"setup.html",
	"file":"file.html"
};


$.lixian.cgi={
	"startup":"cgi-bin/startup.py",
	"saveconf":"cgi-bin/saveconfig.py",
	"loadconf":"cgi-bin/loadconfig.py",
	"listtask":"cgi-bin/list.py",
	"download":"cgi-bin/download.py",
	"log":"cgi-bin/log.py",
	"add":"cgi-bin/add.py",
};


/*
$.lixian.cgi={ // inner test
	"startup":"cgi-test/startup.json",
	"saveconf":"http://adsf.w.d/sdfa.cgi",
	//"saveconf":"cgi-test/saveconfig.json",
	"loadconf":"cgi-test/loadconfig.json",
	"listtask":"cgi-test/list.json",
	"download":"cgi-test/download.json",
	"log":"cgi-test/log.json",
	"add":"cgi-test/add.json",
};
*/

//
$.lixian.message={
		"cgitimeout":"CGI加载超时。<br/>请检查CGI配置<br/>或修改超时秒数。",
		"coreerr":"缺少核心脚本。<br/>请检查脚本文件<br/>或文件执行权限。",
		"configerr":"缺少配置文件。<br/>请配置文件夹<br/>或文件执行权限。",
		"needlogin":"离线还未登陆。<br/>请重新输入用户名和密码。",
		"faillogin":"登陆失败。<br/>请重新输入用户名和密码。",		
		"loginok":"登陆成功。",
		"changeok":"修改成功。",		
		"downloadexist":"下载已经存在<br/>请确认系统信息。",
		"downloadok":"开始下载<br/>请确认系统信息。",
		"downloadng":"下载失败<br/>请确认系统信息。",
		"downloadagain":"相同文件重新下载<br/>请确认系统信息。",
		"addok":"离线添加成功。",
		"addng":"离线添加失败。",
		show:function(key)
		{											
			$.dynamic_popup(this[key]);
		},		
		loading:function(flag)
		{
			if(flag)
			{
				$.mobile.loading( 'show', {
					text: 'Loading...',
					textVisible: true,
					theme: '3',
					html: ""
				});
			}
			else
			{
				$.mobile.loading( 'hide');
			}
		}
	};	
	
//
$.lixian.cache=
	{
		tasktype:"all"
	};

$.lixian.func =
	{
		round:function(num, dec) {
			return Math.round(num*Math.pow(10,dec))/Math.pow(10,dec);
		},
		sizeformat: function(fs) {
			if (fs >= 1073741824) { return this.round(fs / 1073741824, 2) + ' GB'; }
			if (fs >= 1048576)    { return this.round(fs / 1048576, 2) + ' MB'; }
			if (fs >= 1024)       { return this.round(fs / 1024, 0) + ' KB'; }
			return fs + ' B';
			},
		logformat: function(str) {
			return str
				.replace(/\r\n/g, "<br/>")
				.replace(/(\n|\r)/g, "<br/>");
		}
	};
/******************************************************
*indexpage: index.html
*	开始页
*******************************************************/
$( "#indexpage" ).live( "pageinit", function(e){	
		$( "#task" ).bind( "click", function(e) {
			if($.lixian.logined)
			$.mobile.changePage($.lixian.page.task, { transition: "slide"});
			else
			$.lixian.message.show("faillogin");
		});
		
		$( "#add" ).bind( "click", function(e) { 
			if($.lixian.logined)
			$.mobile.changePage($.lixian.page.add, { transition: "slide"});
			else
			$.lixian.message.show("faillogin");
		});
		
		
		$( "#login" ).bind( "click", function(e) {
			if($.lixian.startup)
			$.mobile.changePage($.lixian.page.login, { transition: "slide"});
			else
			$.lixian.message.show("cgitimeout");
		});
		
		$( "#env" ).bind( "click", function(e) {
			if($.lixian.startup)
			$.mobile.changePage($.lixian.page.env, { transition: "slide"});
			else
			$.lixian.message.show("cgitimeout");
		});
});	

$( "#indexpage" ).live( "pageshow", function(e){		
		$.lixian.message.loading(true);
		$.ajax({
			url: $.lixian.cgi.startup,  
			timeout: $.lixian.cgitimeout,  
			Type: "POST",			
			dataType:"json",
			async: false,			
			success: function( resp ) {															
				$.lixian.startup= (resp.data.startup == 'true');
				$.lixian.logined= (resp.data.logined == 'true');
				$("#startuplog").empty();
				$("#startuplog").append($.lixian.func.logformat(resp.log));
				$.lixian.message.loading(false);
				if(resp.msg != "")
				{
					$.lixian.message.show(resp.msg);
				}
			},			
			error: function(jqXHR, textStatus, errorThrown) {					
				$.lixian.message.loading(false);
				$.lixian.message.show("cgitimeout");													
			},
			
		});				
	});

/******************************************************
*taskpage: file.html
*	单一任务页，显示文件详细信息并提供下载
*******************************************************/	
$.lixian.func.scribelog = function()
	{
		clearInterval($.lixian.cache.tasklogscribe);
		$.lixian.cache.tasklogscribe =
			setInterval(function(){ 
				$.ajax({
					url: $.lixian.cgi.log,  
					timeout: $.lixian.cgitimeout,
					data: { id:$.lixian.cache.onetask.id,
							lines:$('#loglines').val()},	
					type: "POST",	
					dataType: 'json',
					cache:false,							
					success: function( resp ) {				
						if(resp.rst == "true")
						{
							$('#filelog').empty();
							$('#filelog').append(resp.data.join("<br/>"));
						}
						else
						{
							clearInterval($.lixian.cache.tasklogscribe);
						}
					},
					error: function(jqXHR, textStatus, errorThrown) {				
						clearInterval($.lixian.cache.tasklogscribe);			
					}
				}); 
			}, $.lixian.logInterval);
	};

$( "#taskpage" ).live( "pageinit", function(e){		
	$( "#submit" ).bind( "click", function(e) { 
			$.lixian.message.loading(true);
			$.ajax({
				url: $.lixian.cgi.download,  
				timeout: $.lixian.cgitimeout, 
				data: {id:$.lixian.cache.onetask.id,
					   fname:$.lixian.cache.onetask.name},					
				type: "POST",			
				dataType: 'json',
				async: false,
				success: function( resp ) {	
					$.lixian.message.loading(false);					
					$.lixian.message.show(resp.msg);
					if(resp.rst == "true")
					{
						$.lixian.func.scribelog();
					}
					else
					{
						$('#filelog').empty();
						$('#filelog').append($.lixian.func.logformat(resp.log));
					}
				},			
				error: function(jqXHR, textStatus, errorThrown) {				
					$.lixian.message.loading(false);									
					$.lixian.message.show("cgitimeout");				
				}
			});
		});
});
	
$( "#taskpage" ).live( "pageshow", function(e){		
		$.lixian.message.loading(true);
		$('#filename').empty();
		$('#filename').append($.lixian.cache.onetask.name);
		$('#filesize').empty();
		$('#filesize').append($.lixian.func.sizeformat($.lixian.cache.onetask.size));
		$('#filestat').empty();
		$('#filestat').append($.lixian.cache.onetask.status+":" +$.lixian.cache.onetask.progress);
		$('#filecontent').listview('refresh');		
		$.lixian.func.scribelog();
		$.lixian.message.loading(false);
	});
	
	
$( "#taskpage" ).live( "pagehide", function(e){		
		clearInterval($.lixian.cache.tasklogscribe);
	});
	
/******************************************************
*
*
*******************************************************/	
$.lixian.func.readtasklist = function()
	{
		$.lixian.message.loading(true);
		$.ajax({
				url: $.lixian.cgi.listtask,  
				timeout: $.lixian.cgitimeout,
				data: {tasktype:$.lixian.cache.tasktype},				   						
				cache:false,				
				async: false,
				dataType: 'json',
				success: function( resp ) {										
					$('#tasklist').empty();
					$.each(resp.data, function(index, result) { 
						$('#tasklist').append("<li><a id='id_"+result.id+"' style='white-space: normal;' >"+result.name+
											  "<span class='ui-li-count'>"+result.status+ ":"+result.progress +" </span></a></li>");					
						});				
					$('#tasklist').trigger('create');    
					$('#tasklist').listview('refresh');			
					$.each(resp.data, function(index, result) { 
					$( "#id_"+result.id ).bind( "click", function(e) { 
						$.lixian.cache.onetask=result;
						$.mobile.changePage($.lixian.page.file, { transition: "slide"});
						});
					});
					$('#tasklist').trigger('create');    
					$('#tasklist').listview('refresh');
				},			
				error: function(jqXHR, textStatus, errorThrown) {				
					$.lixian.message.loading(false);
					$.lixian.message.show("cgitimeout");				
				}
			});
		$.lixian.message.loading(false);
	};

$( "#listpage" ).live( "pageinit", function(e){
	$( "#tasktype" ).change(function(e) { 			
			$.lixian.cache.tasktype = $('#tasktype').val();			
			$.lixian.func.readtasklist($('#tasktype').val());		
		});
	});
	
$( "#listpage" ).live( "pageshow", function(e){
		$('#tasktype').val($.lixian.cache.tasktype);
		$('#tasktype').selectmenu('refresh',true);
		$.lixian.func.readtasklist($('#tasktype').val());
	});	

/******************************************************
*
*
*******************************************************/
$( "#addpage" ).live( "pageinit", function(e){				
		$( "#submit" ).bind( "click", function(e) { 
			$.lixian.message.loading(true);
			$.ajax({
				url: $.lixian.cgi.add,  
				data: { url: $("#url").val(),
						tasktype:$('#tasktype').val()},				
				Type: "POST",		
				dataType:"json",
				async: false,
				success: function( resp ) {
					$.lixian.message.loading(false);								
					$.lixian.message.show(resp.msg);
					if(resp.rst != "true")
					{
						$('#addlog').empty();
						$('#addlog').append($.lixian.func.logformat(resp.log));
					}
				},			
				error: function(jqXHR, textStatus, errorThrown) {				
					$.lixian.message.loading(false);			
					$.lixian.message.show("cgitimeout");				
				}
			});
		});
	});		

/******************************************************
*
*
*******************************************************/
$( "#loginpage" ).live( "pageinit", function(e){		
		$( "#submit" ).bind( "click", function(e) { 
			$.lixian.message.loading(true);
			$.ajax({
				url: $.lixian.cgi.saveconf,  
				timeout: $.lixian.cgitimeout,
				cache:false,		
				data: {username:$('#username').val(),
					   password:$('#password').val()},				
				Type: "POST",
				dataType:"json",
				async: false,
				success: function( resp ) {	
					$.lixian.message.loading(false);
					$.lixian.message.show(resp.msg);
				},			
				error: function(jqXHR, textStatus, errorThrown) {				
					$.lixian.message.loading(false);								
					$.lixian.message.show("cgitimeout");				
				}
			});
		});
	});	

/******************************************************
*
*
*******************************************************/
$( "#envpage" ).live( "pageinit", function(e){
	$( "#submit" ).bind( "click", function(e) { 
				$.lixian.message.loading(true);
				$.ajax({
					url: $.lixian.cgi.saveconf,  
					timeout: $.lixian.cgitimeout, 
					data: {aftertask:$('#chkaftertask').attr("checked")?$('#aftertask').val():"-",
						   pretask:$('#chkpretask').attr("checked")?$('#pretask').val():"-",
						   LIXIAN_DOWNLOAD_PATH:$('#downloadpath').val()},
					Type: "POST",			
					dataType:"json",
					async: false,
					success: function( resp ) {					
						$.lixian.message.loading(false);
						$.lixian.message.show(resp.msg);
					},			
					error: function(jqXHR, textStatus, errorThrown) {				
						$.lixian.message.loading(false);								
						$.lixian.message.show("cgitimeout");				
					}
				});
			});
	});

$( "#envpage" ).live( "pageshow", function(e){
		$.lixian.message.loading(true);
		$.ajax({
			url: $.lixian.cgi.loadconf,  
			timeout: $.lixian.cgitimeout,
			data: {aftertask:"1",
				   pretask:"2",
				   LIXIAN_DOWNLOAD_PATH:"3"},			
			Type: "POST",			
			dataType:"json",
			async: false,
			cache:false,		
			success: function( resp ) {					
				$('#downloadpath').val(resp.data.LIXIAN_DOWNLOAD_PATH);
				$('#pretask').val(resp.data.pretask);
				$('#aftertask').val(resp.data.aftertask);
				$('#chkpretask').attr("checked",(resp.data.pretask.length != 0));
				$('#chkpretask').checkboxradio("refresh");
				$('#chkaftertask').attr("checked",(resp.data.aftertask.length != 0));
				$('#chkaftertask').checkboxradio("refresh");
				
			},			
			error: function(jqXHR, textStatus, errorThrown) {				
				$.lixian.message.loading(false);
				$.lixian.message.show("cgitimeout");				
			}
		});			
		$.lixian.message.loading(false);						
	});