from bs4 import BeautifulSoup

if __name__ == '__main__':
    html_str = """

    <!doctype html>
<html>
  <head>
    <title>教育部考试中心成绩查询 </title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />	
	<meta http-equiv="X-UA-Compatible" content="IE=8" />
	<link href="//www.neea.edu.cn/res/Home/cssjs/15080114L1.css" rel="stylesheet" type="text/css"/>
	<link href="//www.neea.edu.cn/res/Home/cssjs/15080213L1.css" rel="stylesheet" type="text/css">
	<!-- <link href="/tea/neea/chaxun/css/main.css" rel="stylesheet" type="text/css" /> -->
    <script src="//www.neea.edu.cn/query/js/data.js" type="text/javascript"></script>
	<script src="/tea/neea/chaxun/js/neea.js" type="text/javascript"></script>

	<script language="JavaScript">
		//neea.menuOff();
	</script>
	
	<style type="text/css">
	/* 存放到这里 //www.neea.edu.cn/res/Home/cssjs/15080213L1.css */
	.e46{ font:1.25em "微软雅黑", "宋体";
	 color:#333;
	}
	.etit{font:1.25em "微软雅黑", "宋体";color:#333;}
	.e16{
		/*font-weight:bold;font-size:24px;*/
	}
	.bg_1,.bg_2{
		color:#fff;
		font-size:13px;
	}
	.bg_1 th{
		text-align:center;
		background-color:#00adef !important;
	}
	.bg_2 th{text-align:center;
		/*background-color:#ca9900 !important;*/
        background-color:#c0a274 !important;
	}
	#query_result .fb{
		padding-right:10px;
	}
	
	.odere{
		margin: 10px auto;
		border-collapse: collapse;
	}
	.odere th, .odere td {
		font-size:13px;
		text-align:center;
	    border: 1px solid #ccc;
	    padding: 10px 5px;
	    border-collapse: collapse;
	}
	
	.e_bz{font-size:14px;/*color:#999;*/line-height:200%;display:block;margin-bottom:20px;}
	.e_bz em{color:#f00;font-style:normal;}
	</style>

	
<script language="JavaScript">
function goSubmit()
{
	document.getElementById("f").submit();
}
</script>
  </head>
  
<body class='bgs'>
	<div class="queryLeft" id="folatnone">
		<div class='imgpag'>
			<table width="90%" border="0" cellspacing="0" cellpadding="0" class='steptd' align='center'>
				<tr>
					<td><div class="tdoutbox colorlines"><div class="lines"></div><div class="arrt">1</div><span>选择考试项目</span></div></td>
					<td><div class="tdoutbox colorlines"><div class="lines"></div><div class="arrt">2</div><span>输入查询条件</span></div></td>
					<td><div class="tdoutbox colorlines"><div class="lines"></div><div class="arrt">3</div><span>查看成绩</span></div></td>
				</tr>
			</table>
		</div>
		<div class="c_tits" style="font-size: 28px;">中小学教师资格考试(NTCE)<span id="historyStr" style="display: none;">历史</span>成绩</div>
		
		<div class='eers'>
<div class='he_xi'>
您查询的结果为空，请按以下步骤再次确认：<br />
1、	请再次核实所输入信息是否正确。<br />
2、	如果您是按身份证件上的信息输入，请查看身份证件与证书上的信息是否相符，若不相符请按成绩单或证书上的姓名、身份证件号码输入。<br />
</div>
<br><p align='center'><a href='/QueryMarkUpAction.do?act=doQueryCond&sid=2nasVMoohJ6cFnsQEIjGYmh&pram=results' style='font-size: 14px' class='noline'>点此返回</a></p>
</div>

	</div>
<script>
neea.fit();
showHistoryStr();

function showHistoryStr() {
    if(dc_results_subject_list && dc_results_subject_list.length>0){
        for (var i = 0; i < dc_results_subject_list.length; i++) {
            var sub = dc_results_subject_list[i];
            if(sub.code.indexOf('NTCE')==0){
                document.getElementById("historyStr").style.display = "";
                break;
            }
        }
    }
}
</script>
  </body>
</html>

    """
    result = {}
    data_list = []
    soup = BeautifulSoup(html_str, 'lxml')
    if soup.select(".oder tr") is None:
        result['isOk'] = 'N'
    else:
        result['isOk'] = 'Y'
        for idx, tr in enumerate(soup.select(".oder tr")): # 笔试成绩
            if idx != 0:
                tds = tr.find_all('td')
                data_list.append({
                    '科目': tds[0].contents[0],
                    '报告分': tds[1].contents[0],
                    '合格与否': tds[2].contents[0],
                    '准考证号': tds[3].contents[0],
                    '考试批次': tds[4].contents[0],
                    '有效期限': tds[5].contents[0],
                    '考试省份': tds[6].contents[0],
                })
        result['笔试'] = data_list
        data_list = []
        for idx, tr in enumerate(soup.select(".odere tr")): # 笔试成绩
            if idx != 0:
                tds = tr.find_all('td')
                data_list.append({
                    '科目': tds[0].contents[0],
                    '合格与否': tds[1].contents[0],
                    '准考证号': tds[2].contents[0],
                    '考试批次': tds[3].contents[0],
                    '考试省份': tds[4].contents[0],
                })
        result['面试'] = data_list
    print(result)

