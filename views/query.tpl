<!--
%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<p>The open items are as follows:</p>
<table border="1">
%for row in rows:
  <tr>
  %for col in row:
    <td>{{col}}</td>
  %end
  </tr>
%end
</table>
-->
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <title>info inquery</title>
    
    <link href="bootstrap-3.3.7-dist/css/bootstrap.min.css" rel="stylesheet">
  </head>
    <body>
	  <div class="container">
	      <div class="row clearfix">
	        <div class="col-md-12 column">
	          <ul class="nav nav-pills">
	            <li>
	               <a href="main">首页</a>
	            </li>
	            <li class="active">
	               <a href="query">查询</a>
	            </li>
	            <li>
	               <a href="modify">更新</a>
	            </li>
	            <li class="dropdown pull-right">
	               <a href="#" data-toggle="dropdown" class="dropdown-toggle">下拉<strong class="caret"></strong></a>
	              <ul class="dropdown-menu">
	                <li>
	                   <a href="#">操作</a>
	                </li>
	                <li>
	                   <a href="#">设置栏目</a>
	                </li>
	                <li>
	                   <a href="#">更多设置</a>
	                </li>
	                <li class="divider">
	                </li>
	                <li>
	                   <a href="#">分割线</a>
	                </li>
	              </ul>
	            </li>
	          </ul>
	          		<h1 class="text-center text-success">
						书籍信息管理系统
					</h1>
	          <form role="form" action="query" method="GET">
	           <fieldset>
	           <legend>请输入查询信息</legend>
                    <div class="form-group">
                        <label for="exampleInputBookinfo1">标题</label><input class="form-control" id="exampleInputBookinfo1" type="text" name = "title" style="display: inline-block;width: 44.5%;"/>
                        <select name="title_query">
							<option value="exact" selected>精确</option>
							<option value="vague">模糊</option>
						</select>
                    </div>
                    <div class="form-group">
                        <select name="writer_choose">
							<option value="and" selected>并且</option>
							<option value="or">或者</option>
						</select>
                        <label for="exampleInputBookinfo2">作者</label><input class="form-control" id="exampleInputPassword1" type="text" name = "writer" style="display: inline-block;width: 38.5%;" />
                        <select name="writer_query">
							<option value="exact" selected>精确</option>
							<option value="vague">模糊</option>
						</select>
                    </div>
                    <div class="form-group">
                        <select name="pyear_choose">
							<option value="and" selected>并且</option>
							<option value="or">或者</option>
						</select>
                        <label for="exampleInputBookinfo3">出版年份</label><input class="form-control" id="exampleInputPassword1" type="month" name = "pyear" style="display: inline-block;width: 36%;"/>
                        <select name="pyear_query">
							<option value="exact" selected>精确</option>
							<option value="vague">模糊</option>
						</select>
                    </div>
                    <div class="form-group">
                        <select name="pinstitution_choose">
							<option value="and" selected>并且</option>
							<option value="or">或者</option>
						</select>
                         <label for="exampleInputBookinfo4">出版机构</label><input class="form-control" id="exampleInputPassword1" type="text" name = "pinstitution" style="display: inline-block;width: 36%;"/>
                        <select name="pinstitution_query">
							<option value="exact" selected>精确</option>
							<option value="vague">模糊</option>
						</select>
                    </div>
                    <div class="form-group">
                        <select name="plocation_choose">
							<option value="and" selected>并且</option>
							<option value="or">或者</option>
						</select>
                        <label for="exampleInputBookinfo5">出版地</label><input class="form-control" id="exampleInputPassword1" type="text" name = "plocation" style="display: inline-block;width: 37.5%;"/>
                        <select name="plocation_query">
							<option value="exact" selected>精确</option>
							<option value="vague">模糊</option>
						</select>
                    </div>
                    <div class="form-group">
                        <select name="page_choose">
							<option value="and" selected>并且</option>
							<option value="or">或者</option>
						</select>
                        <label for="exampleInputBookinfo6">页数</label><input class="form-control" id="exampleInputPassword1" type="number" name = "page" style="display: inline-block;width: 39%;"/>
                        <select name="page_query">
							<option value="exact" selected>精确</option>
							<option value="vague">模糊</option>
						</select>
                    </div></br><button type="submit" class="btn btn-default" name="save" value="save">查询</button>
              </fieldset>
            </form>  
			<h1 align = "center">查询结果</h1>
				<div class="container">
					<div class="row clearfix">
						<div class="col-md-12 column">
							<table class="table">
								<thead>
									<tr>
										<th>
											标题
										</th>
										<th>
											作者
										</th>
										<th>
											出版年份
										</th>
										<th>
											出版机构
										</th>
										<th>
											出版地点
										</th>
										<th>
											页数
										</th>
									</tr>
								</thead>
								<tbody>
								%for row in rows:
				  					<tr class = "success">
				  					%for col in row:
				    					<td>{{col}}</td>
				 					%end
				  					</tr>
								%end
								</tbody>
							</table>
						</div>
					</div>
				</div>
			</div>
		  </div>
		</div>
	    <script src="./bootstrap-3.3.7-dist/js/jquery-3.2.1.js"></script>
      <script src="./bootstrap-3.3.7-dist/js/bootstrap.min.js"></script>
	</body>
</html>