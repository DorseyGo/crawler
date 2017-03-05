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
      <c:forEach var="item" items="${categories}" varStatus="status">
        <c:choose>
          <c:when test="${status.index == 0}">
            <li role="presentation" ><a href="#${item.id}">${item.category}</a></li>
          </c:when>
          <c:otherwise>
            <li role="presentation"><a href="#${item.id}">${item.category}</a></li>
          </c:otherwise>
        </c:choose>
      </c:forEach>
    </ul>
    <div class="tab-content">
      <c:forEach var="item1" items="${imagePage}" varStatus="status">
        <c:choose>
          <c:when test="${status.index == 0}">
            <div class="tab-pane" id="${item1.categoryId}">
              <!-- Example row of columns -->
              <div class="row">
                <c:forEach var="item" items="${item1.list}">
                  <div class="col-md-4 thumbnail">
                    <a href="${pageContext.request.contextPath}/images/detail/${item.id}">
                      <img src="http://localhost:8081/${item.storePath}/${item.fullName}"/>
                    </a>
                  </div>
                </c:forEach>
              </div>
              <div style="text-align: center"> <ul id="tt${item1.categoryId}" class="pagination"></ul></div>
            </div>
          </c:when>
          <c:otherwise>
            <div class="tab-pane" id="${item1.categoryId}">
              <!-- Example row of columns -->
              <div class="row">
                <c:forEach var="item" items="${item1.list}">
                  <div class="col-md-4 thumbnail">
                    <a href="${pageContext.request.contextPath}/images/detail/${item.id}">
                      <img src="http://localhost:8081/${item.storePath}/${item.fullName}"/>
                    </a>
                  </div>
                </c:forEach>
              </div>
              <div style="text-align: center"> <ul id="tt${item1.categoryId}" class="pagination"></ul></div>
            </div>
          </c:otherwise>
        </c:choose>
      </c:forEach>
    </div>
  </div>
</div>

<div class="container">
  <!-- Example row of columns -->
  <%--<div class="row">
    <c:forEach var="item" items="${imagePage.list}">
      <div class="col-md-4 thumbnail">
        <a href="${pageContext.request.contextPath}/images/detail/${item.id}">
        <img src="http://localhost:8081/${item.storePath}/${item.fullName}"/>
        </a>
      </div>
    </c:forEach>

  </div>
  <div style="text-align: center"> <ul id="tt" class="pagination"></ul></div>--%>
  <hr>

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

  if (${categoryId} !== null || ${categoryId} !== '')
  {
    $('#mytabs a[href="#'+ ${categoryId}+'"]').tab('show')
  }

</script>
</html>
