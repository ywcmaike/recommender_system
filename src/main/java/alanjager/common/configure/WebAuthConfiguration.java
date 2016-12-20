package alanjager.common.configure;

import org.apache.log4j.Logger;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableGlobalMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;

/**
 * Created by AlanJager on 2016/10/19.
 */

@EnableGlobalMethodSecurity(prePostEnabled = true)
@Configuration
@EnableWebSecurity
public class WebAuthConfiguration extends WebSecurityConfigurerAdapter {
    private Logger logger = Logger.getLogger(WebAuthConfiguration.class);

    protected void configure(HttpSecurity http) throws Exception {
        logger.debug("Using default configure(HttpSecurity). If subclassed this will potentially override subclass configure(HttpSecurity).");
        // set url filter
        http.authorizeRequests().antMatchers("/", "/user/**", "test/v1/*").permitAll()
                .anyRequest().authenticated()
                .and()
                .formLogin().and()
                .httpBasic()
                .and().rememberMe();
    }
}
