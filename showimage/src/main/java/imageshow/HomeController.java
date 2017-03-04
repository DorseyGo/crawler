package imageshow;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

/**
 * @author Created by shuaqiu on 2017-02-10.
 */
@Controller
@RequestMapping(value = "/")
public class HomeController {

    @GetMapping
    public String home() {
        return "redirect:images";
    }
}
