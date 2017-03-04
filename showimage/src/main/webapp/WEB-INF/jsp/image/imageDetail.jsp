<%@ page pageEncoding="utf-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<html>
<head>
  <title>图片展示</title>
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="${pageContext.request.contextPath}/static/bootstrap-3.3.7/css/bootstrap.min.css" rel="stylesheet"
        type="text/css"/>
  <link href="${pageContext.request.contextPath}/static/image/image.css" rel="stylesheet" type="text/css"/>
</head>
<body>
<nav class="navbar navbar-inverse navbar-fixed-top">
  <div class="container">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar"
              aria-expanded="false" aria-controls="navbar">
        <span class="sr-only">切换</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="#">图片展示</a>
    </div>
  </div>
</nav>

<!-- Main jumbotron for a primary marketing message or call to action -->
<div class="jumbotron">
  <div class="container">
    <h1>图片展示</h1>
  </div>
</div>

<div class="container text-center">
  <!-- Example row of columns -->
  <c:forEach var="item" items="${imageDetail}">
    <div class="thumbnail">
      <img src="http://localhost:8081/${item.storePath}/${item.fullName}"/>
      <h2>${item.name}</h2>
      <p><a class="btn btn-default" href="${pageContext.request.contextPath}/images/${item.id}" role="button">查看 &raquo;</a></p>
    </div>
  </c:forEach>

  <hr>

  <footer>
    <p>&copy; 2017 Company, Inc.</p>
  </footer>
</div> <!-- /container -->

<script src="${pageContext.request.contextPath}/static/jquery/jquery-3.1.1.min.js"></script>
<script src="${pageContext.request.contextPath}/static/bootstrap-3.3.7/js/bootstrap.min.js"></script>
<script src="${pageContext.request.contextPath}/static/image/image.js"></script>
</body>
</html>