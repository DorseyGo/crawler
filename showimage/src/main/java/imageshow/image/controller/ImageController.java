package imageshow.image.controller;

import com.alibaba.fastjson.JSON;
import imageshow.Page;
import imageshow.image.bean.Categories;
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

import java.util.LinkedList;
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

    @GetMapping(value="/{domainId}")
    public String list(@PathVariable final int domainId, final Model model) {

        List<Page<Image>> list = new LinkedList<>();
        List<Categories> categories = imageService.loadCategories();

        for(Categories cat:categories) {
            final Page<Image> images = imageService.loadImages(2, 1, null,cat.getId(),domainId);
            list.add(images);
        }

        model.addAttribute("imagePage", list);
        model.addAttribute("categories", categories);
        String json = JSON.toJSONString(categories);
        model.addAttribute("categoriesJson", json);
        model.addAttribute("imagePageJson", JSON.toJSONString(list));

        return  "image/imageList";
    }

    @GetMapping(value="/page")
    public String page(@RequestParam("pageSize") int pageSize, @RequestParam("pageNo") int pageNo,@RequestParam("categoryId") long categoryId,@RequestParam("domainId") int domainId,final Model model) {

        List<Page<Image>> list = new LinkedList<>();

        List<Categories> categories = imageService.loadCategories();
        Page<Image> images;
        for(Categories cat:categories) {
            if(cat.getId() == categoryId){
                images = imageService.loadImages(pageSize, pageNo, null, cat.getId(), domainId);
            }else {
                images = imageService.loadImages(2, 1, null, cat.getId(), domainId);
            }
            list.add(images);
        }

        model.addAttribute("imagePage", list);
        model.addAttribute("categories", categories);
        String json = JSON.toJSONString(categories);
        model.addAttribute("categoriesJson", json);
        model.addAttribute("imagePageJson", JSON.toJSONString(list));
        model.addAttribute("categoryId", categoryId);

        return "image/imageList";
    }

    @GetMapping(value = "/detail/{imageId}")
    public String detailList(@PathVariable final int imageId, final Model model) {
        final List<ImageDetail> imageDetail = imageService.loadImageDetail(imageId);
        model.addAttribute("imageDetail", imageDetail);
        return "image/imageDetail";
    }

    //@GetMapping(value = "/{id}")
    //public String detail(@PathVariable final int id, final Model model) {
    //    final Image image = imageService.loadImage(id);
    //    model.addAttribute("image", image);
    //    return "image/imageDetail";
    //}


}
