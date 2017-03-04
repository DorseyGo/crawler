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

    public Page(final int pageSize, final int pageNo, final long total, final List<T> pageData) {
        this.pageSize = pageSize;
        this.pageNo = pageNo;
        this.total = total;
        this.totalPage = (int) ((total - 1) / pageSize + 1);
        this.list = pageData;
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
}
