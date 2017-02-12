package imageshow.image.bean;

import java.util.Date;

/**
 * @author Created by shuaqiu on 2017-02-10.
 */
public class Image {

    private Integer id;

    private String name;

    private String fullName;

    private String storePath;

    private Integer categoryId;

    private Date createdTime;

    public int getId() {
        return id;
    }

    public void setId(final Integer id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(final String name) {
        this.name = name;
    }

    public String getFullName() {
        return fullName;
    }

    public void setFullName(final String fullName) {
        this.fullName = fullName;
    }

    public String getStorePath() {
        return storePath;
    }

    public void setStorePath(final String storePath) {
        this.storePath = storePath;
    }

    public Integer getCategoryId() {
        return categoryId;
    }

    public void setCategoryId(final Integer categoryId) {
        this.categoryId = categoryId;
    }

    public Date getCreatedTime() {
        return createdTime;
    }

    public void setCreatedTime(final Date createdTime) {
        this.createdTime = createdTime;
    }
}
