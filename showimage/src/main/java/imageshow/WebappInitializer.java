/**
 *
 */
package imageshow;

import javax.servlet.ServletContext;
import javax.servlet.ServletException;
import javax.servlet.ServletRegistration.Dynamic;

import org.springframework.web.WebApplicationInitializer;
import org.springframework.web.context.ContextLoaderListener;
import org.springframework.web.context.support.AnnotationConfigWebApplicationContext;
import org.springframework.web.servlet.DispatcherServlet;

/**
 * Web启动
 * 
 * @author shuaqiu 2013年12月31日
 *
 */
public class WebappInitializer implements WebApplicationInitializer {

    @Override
    public void onStartup(final ServletContext servletContext)
            throws ServletException {

        final AnnotationConfigWebApplicationContext rootContext = new AnnotationConfigWebApplicationContext();
        rootContext.register(AppConfig.class);
        rootContext.refresh();

        // Manage the lifecycle of the root application context
        servletContext.addListener(new ContextLoaderListener(rootContext));
        
        Dynamic servlet = servletContext.addServlet("imageshow", DispatcherServlet.class);
        servlet.setInitParameter("contextConfigLocation", "classpath:/imageshow-servlet.xml");
        servlet.setLoadOnStartup(1);
        servlet.addMapping("/");
    }

}
