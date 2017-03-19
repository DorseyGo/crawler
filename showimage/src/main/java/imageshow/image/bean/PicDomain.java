package imageshow.image.bean;

/**
 * Created by xujun on 2017/3/15.
 */
public class PicDomain {
    private long id;

    private String domain;

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public String getDomain() {
        return domain;
    }

    public void setDomain(String domain) {
        this.domain = domain;
    }

    @Override
    public String toString() {
        return "PicDomain{" +
                "id=" + id +
                ", domain='" + domain + '\'' +
                '}';
    }
}
