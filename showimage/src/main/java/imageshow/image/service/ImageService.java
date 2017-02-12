package imageshow.image.service;

import java.util.List;

import imageshow.Page;
import imageshow.image.bean.Image;
import imageshow.image.mapper.ImageMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.StringUtils;

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

    public Page<Image> loadImages(final int pageSize, final int pageNo, final String name) {
        final String nameLike = StringUtils.hasText(name) ? "%" + name + "%" : null;
        final long total = imageMapper.count(nameLike);
        final int offset = pageSize * Math.max(0, pageNo - 1);
        final List<Image> pageData = imageMapper.paginate(offset, pageSize, nameLike);

        return new Page<>(pageSize, pageNo, total, pageData);
    }

    public Image loadImage(final int id) {
        return imageMapper.loadImage(id);
    }
}
