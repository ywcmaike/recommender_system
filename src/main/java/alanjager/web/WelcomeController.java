package alanjager.web;

import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

/**
 * Created by AlanJager on 2016/10/19.
 */
@Controller
@EnableConfigurationProperties
public class WelcomeController {
    @RequestMapping(value="/",method= RequestMethod.GET)
    @ResponseBody
    public String welcome(){
        return "welcome";
    }
}