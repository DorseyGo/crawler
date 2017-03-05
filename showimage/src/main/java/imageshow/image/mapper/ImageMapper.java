package imageshow.image.mapper;

import imageshow.image.bean.Categories;
import imageshow.image.bean.Image;
import imageshow.image.bean.ImageDetail;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.SelectProvider;
import org.apache.ibatis.jdbc.SQL;
import org.springframework.util.StringUtils;

import java.util.List;

/**
 * @author Created by shuaqiu on 2017-02-10.
 */
public interface ImageMapper {

    @SelectProvider(type = ImageSqlBuilder.class, method = "buildCountSql")
    long count(final @Param("name") String name,
               final @Param("categoryId") long categoryId,
               final @Param("domainId") int domainId);

    @SelectProvider(type = ImageSqlBuilder.class, method = "buildPaginateSql")
    List<Image> paginate(final @Param("offset") int offset,
                         final @Param("pageSize") int pageSize,
                         final @Param("name") String name,
                         final @Param("categoryId") long categoryId,
                         final @Param("domainId") int domainId);

    @Select(" select" +
            "  ID as id," +
            "  NAME as name," +
            "  FULL_NAME as fullName," +
            "  STORE_PATH as storePath," +
            "  IMG_ID as imageId," +
            "  CREATED_TIME as createdTime" +
            " from IMAGE_DETAILS" +
            " where IMG_ID = #{id}")
    List<ImageDetail> loadImageDetail(final int id);

    @Select(" select" +
            "  ID as id," +
            "  CATEGORY as category," +
            "  ABBREVIATION as abbreviation" +
            " from CATEGORIES"+
            " order by id")
    List<Categories> loadCategories();

    @Select(" select" +
            "  ID as id," +
            "  NAME as name," +
            "  FULL_NAME as fullName," +
            "  STORE_PATH as storePath," +
            "  CATEGORY_ID as categoryId," +
            "DOMAIN_ID as domainId," +
            "  CREATED_TIME as createdTime" +
            " from IMAGES" +
            " where ID = #{id}")
    Image loadImage(final int id);

    class ImageSqlBuilder {

        public String buildCountSql(final @Param("name") String name,
                                    final @Param("categoryId") long categoryId,
                                    final @Param("domainId") int domainId) {
            return new SQL() {
                {
                    SELECT("count(*)");
                    FROM("IMAGES");
                    WHERE(" CATEGORY_ID = #{categoryId} and DOMAIN_ID = #{domainId} ");
                    if (StringUtils.hasText(name)) {
                        WHERE(" and (NAME like #{name} or FULL_NAME like #{name})");
                    }
                }
            }.toString();
        }

        public String buildPaginateSql(final @Param("offset") int offset,
                                       final @Param("pageSize") int pageSize,
                                       final @Param("name") String name,
                                       final @Param("categoryId") long categoryId,
                                       final @Param("domainId") int domainId) {
            return new SQL() {
                {
                    SELECT("ID as id",
                            "NAME as name",
                            "FULL_NAME as fullName",
                            "STORE_PATH as storePath",
                            "CATEGORY_ID as categoryId",
                            "DOMAIN_ID as domainId",
                            "CREATED_TIME as createdTime");
                    FROM("IMAGES");
                    WHERE(" CATEGORY_ID = #{categoryId} and DOMAIN_ID = #{domainId} ");
                    if (StringUtils.hasText(name)) {
                        WHERE(" and (NAME like #{name} or FULL_NAME like #{name})");
                    }
                }
            }.toString()
                    + " LIMIT #{offset}, #{pageSize}";
        }
    }
}
