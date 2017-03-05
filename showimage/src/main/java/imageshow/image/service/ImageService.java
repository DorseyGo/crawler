package imageshow.image.service;

import imageshow.Page;
import imageshow.image.bean.Categories;
import imageshow.image.bean.Image;
import imageshow.image.bean.ImageDetail;
import imageshow.image.mapper.ImageMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.StringUtils;

import java.util.List;

/**
 * @author Created by shuaqiu on 2017-02-10.
 */
@Service
@Transactional(readOnly = true, timeout = 1000)
public class ImageService {

    private ImageMapper imageMapper;

    @Autowired
    public void setImageMapper(final ImageMapper imageMapper) {
        this.imageMapper = imageMapper;
    }

    public Page<Image> loadImages(final int pageSize, final int pageNo, final String name, final long categoryId,final int domainId) {
        final String nameLike = StringUtils.hasText(name) ? "%" + name + "%" : null;
        final long total = imageMapper.count(nameLike,categoryId,domainId);
        final int offset = pageSize * Math.max(0, pageNo - 1);
        final List<Image> pageData = imageMapper.paginate(offset, pageSize, nameLike,categoryId,domainId);

        return new Page<>(pageSize, pageNo, total, pageData,categoryId,domainId);
    }

    public Image loadImage(final int id) {
        return imageMapper.loadImage(id);
    }

    public List<ImageDetail> loadImageDetail(final int imageId){
        return imageMapper.loadImageDetail(imageId);
    }

    public List<Categories> loadCategories(){
        return imageMapper.loadCategories();
    }
}
