package imageshow.image.mapper;

import imageshow.image.bean.Categories;
import imageshow.image.bean.Image;
import imageshow.image.bean.ImageDetail;
import imageshow.image.bean.PicDomain;
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
               final @Param("domainId") String domainId);

    @SelectProvider(type = ImageSqlBuilder.class, method = "buildPaginateSql")
    List<Image> paginate(final @Param("offset") int offset,
                         final @Param("pageSize") int pageSize,
                         final @Param("name") String name,
                         final @Param("categoryId") long categoryId,
                         final @Param("domainId") String domainId);

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

    @Select(" select " +
            " ID as id," +
            " DOMAIN as domain" +
            " from PIC_DOMAINS" +
            " order by CREATED_TIME desc")
    List<PicDomain> loadPicDomain();

    @Select(" select" +
            "  ID as id," +
            "  NAME as name," +
            "  FULL_NAME as fullName," +
            "  STORE_PATH as storePath," +
            "  CATEGORY_ID as categoryId," +
            "  DOMAIN_ID as domainId," +
            "  CREATED_TIME as createdTime" +
            " from IMAGES" +
            " where ID = #{id}")
    Image loadImage(final int id);

    class ImageSqlBuilder {

        public String buildCountSql(final @Param("name") String name,
                                    final @Param("categoryId") long categoryId,
                                    final @Param("domainId") String domainId) {
            return new SQL() {
                {
                    SELECT("count(*)");
                    FROM("IMAGES");
                    WHERE(" CATEGORY_ID = #{categoryId} ");
                    if(domainId.trim().length() > 0 && !domainId.contains("-1")) {
                        String[] ids = domainId.split(",");
                        String inPar = "DOMAIN_ID in (";
                        for(String tmp:ids){
                            inPar = inPar + tmp+",";
                        }
                        inPar = inPar.substring(0,inPar.length()-1)+")";
                        WHERE(inPar);
                    }
                    if (StringUtils.hasText(name)) {
                        WHERE(" (NAME like #{name} or FULL_NAME like #{name})");
                    }
                }
            }.toString();
        }

        public String buildPaginateSql(final @Param("offset") int offset,
                                       final @Param("pageSize") int pageSize,
                                       final @Param("name") String name,
                                       final @Param("categoryId") long categoryId,
                                       final @Param("domainId") String domainId) {
            return new SQL() {
                {
                    SELECT("ID as id",
                            "NAME as name",
                            "FULL_NAME as fullName",
                            "STORE_PATH as storePath",
                            "CATEGORY_ID as categoryId",
                            "DOMAIN_ID as domainId",
                            "date_format(CREATED_TIME,'%Y-%c-%d %h:%i:%s') as createdTime");
                    FROM("IMAGES");
                    WHERE(" CATEGORY_ID = #{categoryId}");
                    if(domainId.trim().length() > 0 && !domainId.contains("-1")) {
                        String[] ids = domainId.split(",");
                        String inPar = "DOMAIN_ID in (";
                        for(String tmp:ids){
                            inPar = inPar + tmp+",";
                        }
                        inPar = inPar.substring(0,inPar.length()-1)+")";
                        WHERE(inPar);
                    }
                    if (StringUtils.hasText(name)) {
                        WHERE(" (NAME like #{name} or FULL_NAME like #{name})");
                    }
                    ORDER_BY(" CREATED_TIME desc ");
                }
            }.toString()
                    + " LIMIT #{offset}, #{pageSize}";
        }
    }
}
