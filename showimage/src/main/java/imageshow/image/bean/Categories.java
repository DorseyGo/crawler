package imageshow.image.bean;

/**
 * Created by xujun on 2017/3/5.
 */
public class Categories {

    private long id;

    private String category;

    private String abbreviation;

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public String getAbbreviation() {
        return abbreviation;
    }

    public void setAbbreviation(String abbreviation) {
        this.abbreviation = abbreviation;
    }

    @Override
    public String toString() {
        return "Categories{" +
                "id=" + id +
                ", category='" + category + '\'' +
                ", abbreviation='" + abbreviation + '\'' +
                '}';
    }
}
