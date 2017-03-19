package imageshow;

import java.util.List;

/**
 * @author Created by shuaqiu on 2017-02-10.
 */
public class Page<T> {

    private final int pageSize;

    private final int pageNo;

    private final long total;

    private final int totalPage;

    private final List<T> list;

    private final long categoryId;

    private final String domainId;

    public Page(final int pageSize, final int pageNo, final long total, final List<T> pageData,final long categoryId,final String domainId) {
        this.pageSize = pageSize;
        this.pageNo = pageNo;
        this.total = total;
        this.totalPage = (int) ((total - 1) / pageSize + 1);
        this.list = pageData;
        this.categoryId = categoryId;
        this.domainId = domainId;
    }

    public int getPageSize() {
        return pageSize;
    }

    public int getPageNo() {
        return pageNo;
    }

    public long getTotal() {
        return total;
    }

    public int getTotalPage() {
        return totalPage;
    }

    public List<T> getList() {
        return list;
    }

    public long getCategoryId() {
        return categoryId;
    }

    public String getDomainId() {
        return domainId;
    }
}
