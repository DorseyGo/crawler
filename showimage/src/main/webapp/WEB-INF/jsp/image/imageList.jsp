<%@ page pageEncoding="utf-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<html>
<head>
  <title>图片展示</title>
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="${pageContext.request.contextPath}/static/bootstrap-3.3.7/css/bootstrap.min.css" rel="stylesheet" type="text/css"/>
  <link href="${pageContext.request.contextPath}/static/image/image.css" rel="stylesheet" type="text/css"/>
  <script src="${pageContext.request.contextPath}/static/jquery/jquery-3.1.1.min.js"></script>
  <script src="${pageContext.request.contextPath}/static/bootstrap-3.3.7/js/bootstrap.min.js"></script>
  <script src="${pageContext.request.contextPath}/static/image/image.js"></script>
  <script src="${pageContext.request.contextPath}/static/paginator/bootstrap-paginator.min.js"></script>
</head>
<body>
<nav class="navbar navbar-inverse navbar-fixed-top">
  <div class="container">
    <div class="navbar-header">
      <a class="navbar-brand" href="#">图片展示</a>
    </div>
  </div>
</nav>

<!-- Main jumbotron for a primary marketing message or call to action -->
<div class="jumbotron">
  <div class="container">
    <div id="domain" >
      <li class="btn col-sm-2">
        <a id="domain--1" href="#" style="text-decoration: none">all</a>
      </li>
      <c:forEach var="item" items="${picDomains}" varStatus="status">
        <li class="btn col-sm-2">
          <a id="domain-${item.id}" href="#" style="text-decoration: none">${item.domain}</a>
        </li>
      </c:forEach>
    </div>
    <div>
      <li class="btn col-sm-2">
        <input type="text" id="imageName"/>
        <a id="queryBtn" class="btn btn-info">确&nbsp;&nbsp;定</a>
      </li>
    </div>
  </div>
  <div class="container">
    <ul id="mytabs" class="nav nav-tabs">
      <c:forEach var="item" items="${categories}" varStatus="status">
        <li role="presentation" ><a href="#${item.id}">${item.category}</a></li>
      </c:forEach>
    </ul>
    <div class="tab-content">
      <c:forEach var="item1" items="${imagePage}" varStatus="status">
        <div class="tab-pane" id="${item1.categoryId}">
          <!-- Example row of columns -->
          <div class="row">
            <c:forEach var="item" items="${item1.list}">
              <div class="col-md-4 thumbnail">
                <a href="${pageContext.request.contextPath}/images/detail/${item.id}?categoryId=${item1.categoryId}&domainId=${item.domainId}&createdTime=${item.createdTime}" >
                  <img src="http://localhost:8081/${item.storePath}/${item.fullName}"/>
                </a>
                <p><h6>图片名称:&nbsp;${item.name}</h6></p>
              </div>
            </c:forEach>
          </div>
          <div style="text-align: center"> <ul id="tt${item1.categoryId}" class="pagination"></ul></div>
        </div>
      </c:forEach>
    </div>
  </div>
</div>

<div class="container">
  <footer>
    <p>&copy; 2017 Company, Inc.</p>
  </footer>
</div> <!-- /container -->


</body>
<script>
  $.each(${imagePageJson},function(index,item){
    var next = index+1;

    var options = {
      currentPage: item.pageNo,
      totalPages: item.totalPage,
      numberOfPages: 10,
      size:"normal",
      bootstrapMajorVersion: 3,
      alignment:"right",
      pageUrl: function(type,page,current){
        return "${pageContext.request.contextPath}/images/page?pageSize="+item.pageSize+"&pageNo="+page+"&categoryId="+item.categoryId+"&domainId="+item.domainId}
    }

    if(item.list.length > 0)
      $('#tt'+next).bootstrapPaginator(options);
  })

  $('#mytabs a').click(function(e){
    e.preventDefault()
    $(this).tab('show')
  })

  if ("${categoryId}" !== null || "${categoryId}" !== '')
  {
    $('#mytabs a[href="#'+ ${categoryId}+'"]').tab('show')
  }

  if ("${domainIds}" !== null || "${domainIds}" !== ''){
    var idArr = "${domainIds}".split(",");
    for(var i=0;i<idArr.length;i++){
      $('#domain-'+idArr[i]).toggleClass("btn-primary active");
    }
  }

  $('.tab-content .thumbnail a').click(function(){

    var pageNo = $('.tab-content .active .active a').text();
    $(this).attr("href",$(this).attr("href")+"&pageNo="+pageNo);
  })

  $('#domain a').click(function(){
    $(this).toggleClass("btn-primary active");
  })

  $('#queryBtn').click(function(){
    var arr = new Array();
    $('#domain a').each(function(){
      if($(this).hasClass("btn-primary active")){
        arr.push($(this).attr("id"));
      }
    })

    var ids = arr.join(",");

    var imageName = $('#imageName').val();
    $(this).attr('href','${pageContext.request.contextPath}/images/multiIds?domainIds='+ids+'&imageName='+imageName);
  })
</script>
</html>
