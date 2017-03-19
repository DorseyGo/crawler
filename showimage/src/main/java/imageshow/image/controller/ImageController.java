package imageshow.image.controller;

import com.alibaba.fastjson.JSON;
import imageshow.Page;
import imageshow.image.bean.Categories;
import imageshow.image.bean.Image;
import imageshow.image.bean.ImageDetail;
import imageshow.image.bean.PicDomain;
import imageshow.image.constants.Constants;
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
    public String list(@PathVariable final String domainId, final Model model) {

        List<Page<Image>> list = new LinkedList<>();
        List<Categories> categories = imageService.loadCategories();
        List<PicDomain> picDomains = imageService.loadPicDomains();

        for(Categories cat:categories) {
            final Page<Image> images = imageService.loadImages(Constants.PAGE_SIZE, Constants.FIRST_PAGE, null,cat.getId(),domainId);
            list.add(images);
        }

        model.addAttribute("imagePage", list);
        model.addAttribute("categories", categories);
        model.addAttribute("picDomains",picDomains);
        String json = JSON.toJSONString(categories);
        model.addAttribute("categoriesJson", json);
        model.addAttribute("imagePageJson", JSON.toJSONString(list));
        model.addAttribute("domainIds",domainId);

        return  "image/imageList";
    }

    @GetMapping(value="/multiIds")
    public String listByMultiId(@RequestParam("domainIds") String domainIds,@RequestParam("imageName") String imageName, final Model model){

        if(domainIds ==null || domainIds.trim().length()==0){
            return "redirect:-1";
        }

        List<Page<Image>> list = new LinkedList<>();
        List<Categories> categories = imageService.loadCategories();
        List<PicDomain> picDomains = imageService.loadPicDomains();

        StringBuilder sb = new StringBuilder(50);

        String[] idArr = domainIds.split(",");

        for (int i=0;i<idArr.length;i++) {
            if(i>0){
                sb.append(",");
            }
            sb.append(idArr[i].substring("domain-".length()));
        }

        for(Categories cat:categories) {
            final Page<Image> images = imageService.loadImages(Constants.PAGE_SIZE, Constants.FIRST_PAGE, imageName,cat.getId(),sb.toString());
            list.add(images);
        }

        model.addAttribute("imagePage", list);
        model.addAttribute("categories", categories);
        model.addAttribute("picDomains",picDomains);
        String json = JSON.toJSONString(categories);
        model.addAttribute("categoriesJson", json);
        model.addAttribute("imagePageJson", JSON.toJSONString(list));
        model.addAttribute("domainIds",sb.toString());

        return  "image/imageList";
    }

    @GetMapping(value="/page")
    public String page(@RequestParam("pageSize") int pageSize, @RequestParam("pageNo") int pageNo,@RequestParam("categoryId") long categoryId,@RequestParam("domainId") String domainId,final Model model) {

        List<Page<Image>> list = new LinkedList<>();

        List<Categories> categories = imageService.loadCategories();
        Page<Image> images;
        for(Categories cat:categories) {
            if(cat.getId() == categoryId){
                images = imageService.loadImages(pageSize, pageNo, null, cat.getId(), domainId);
            }else {
                images = imageService.loadImages(Constants.PAGE_SIZE, Constants.FIRST_PAGE, null, cat.getId(), domainId);
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
    public String detailList(@PathVariable final int imageId, final Model model, @RequestParam("pageNo") int pageNo,@RequestParam("categoryId") long categoryId,@RequestParam("domainId") int domainId, @RequestParam("createdTime") String createdTime) {

        System.out.println(pageNo+","+categoryId+","+domainId);
        final List<ImageDetail> imageDetail = imageService.loadImageDetail(imageId);
        model.addAttribute("imageDetail", imageDetail);
        model.addAttribute("pageNo",pageNo);
        model.addAttribute("pageSize",Constants.PAGE_SIZE);
        model.addAttribute("categoryId",categoryId);
        model.addAttribute("domainId",domainId);
        model.addAttribute("createdTime",createdTime);

        return "image/imageDetail";
    }

    //@GetMapping(value = "/{id}")
    //public String detail(@PathVariable final int id, final Model model) {
    //    final Image image = imageService.loadImage(id);
    //    model.addAttribute("image", image);
    //    return "image/imageDetail";
    //}


}
