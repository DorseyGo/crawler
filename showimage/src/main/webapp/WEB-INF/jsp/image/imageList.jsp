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
    <ul id="mytabs" class="nav nav-tabs">
      <li role="presentation" class="active"><a href="#home">Home</a></li>
      <li role="presentation"><a href="#profile">Profile</a></li>
      <li role="presentation"><a href="#message">Messages</a></li>
    </ul>
    <div class="tab-content">
      <div id="home" class="tab-pane fade active in"><p>home</p></div>
      <div id="profile" class="tab-pane fade"><p>profile</p></div>
      <div id="message" class="tab-pane fade"><p>message</p></div>
    </div>
  </div>
</div>

<div class="container">
  <!-- Example row of columns -->
  <div class="row">
    <c:forEach var="item" items="${imagePage.list}">
      <div class="col-md-4 thumbnail">
        <a href="${pageContext.request.contextPath}/images/detail/${item.id}">
        <img src="http://localhost:8081/${item.storePath}/${item.fullName}"/>
        </a>
      </div>
    </c:forEach>

  </div>
  <div style="text-align: center"> <ul id="tt" class="pagination"></ul></div>
  <hr>

  <footer>
    <p>&copy; 2017 Company, Inc.</p>
  </footer>
</div> <!-- /container -->


</body>
<script>
  var options = {
    currentPage: ${imagePage.pageNo},
    totalPages: ${imagePage.totalPage},
    numberOfPages: 10,
    size:"normal",
    bootstrapMajorVersion: 3,
    alignment:"right",
    pageUrl: function(type,page,current){
      return "${pageContext.request.contextPath}/images/page?pageSize=${imagePage.pageSize}&pageNo="+page}
  }

  $('#tt').bootstrapPaginator(options);

  $("#mytabs a").click(function(e){
    e.preventDefault()
    $(this).tab('show')
  })
</script>
</html>
