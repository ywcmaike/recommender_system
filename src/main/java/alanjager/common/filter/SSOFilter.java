// Created by AlanJager on 2016/10/31.
package alanjager.common.filter;

import org.apache.log4j.Logger;
import org.springframework.core.annotation.Order;

import javax.servlet.*;
import javax.servlet.annotation.WebFilter;
import java.io.IOException;

@Order(5)
@WebFilter(filterName = "SSOFilter", urlPatterns = {"/github", "/facebook"})
public class SSOFilter implements Filter {
    private Logger logger = Logger.getLogger(getClass());

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        logger.info("SSO filter created");
    }

    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
        filterChain.doFilter(servletRequest, servletResponse);
        logger.info("SSO filter worked");
    }

    @Override
    public void destroy() {
        logger.info("SSO filter destroyed");
    }
}
