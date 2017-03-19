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

    private Integer domainId;

    private String createdTime;

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

    public String getCreatedTime() {
        return createdTime;
    }

    public void setCreatedTime(final String createdTime) {
        this.createdTime = createdTime;
    }

    public Integer getDomainId() {
        return domainId;
    }

    public void setDomainId(Integer domainId) {
        this.domainId = domainId;
    }

    @Override
    public String toString() {
        return "Image{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", fullName='" + fullName + '\'' +
                ", storePath='" + storePath + '\'' +
                ", categoryId=" + categoryId +
                ", domainId=" + domainId +
                ", createdTime=" + createdTime +
                '}';
    }
}
