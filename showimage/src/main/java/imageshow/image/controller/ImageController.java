package imageshow.image.controller;

import imageshow.Page;
import imageshow.image.bean.Image;
import imageshow.image.bean.ImageDetail;
import imageshow.image.service.ImageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;

/**
 * @author Created by shuaqiu on 2017-02-09.
 */
@Controller
@RequestMapping(value = "images")
public class ImageController {

    private ImageService imageService;

    @Autowired
    public void setImageService(final ImageService imageService) {
        this.imageService = imageService;
    }

    @GetMapping
    public String list(final Model model) {
        final Page<Image> images = imageService.loadImages(12, 1, null);
        model.addAttribute("imagePage", images);
        return "image/imageList";
    }

    @GetMapping(value="/page")
    public String page(@RequestParam("pageSize") int pageSize, @RequestParam("pageNo") int pageNo,final Model model) {
        final Page<Image> images = imageService.loadImages(pageSize, pageNo, null);
        model.addAttribute("imagePage", images);
        return "image/imageList";
    }

    @GetMapping(value = "/detail/{imageId}")
    public String detailList(@PathVariable final int imageId, final Model model) {
        final List<ImageDetail> imageDetail = imageService.loadImageDetail(imageId);
        model.addAttribute("imageDetail", imageDetail);
        return "image/imageDetail";
    }

    @GetMapping(value = "/{id}")
    public String detail(@PathVariable final int id, final Model model) {
        final Image image = imageService.loadImage(id);
        model.addAttribute("image", image);
        return "image/imageDetail";
    }
}
