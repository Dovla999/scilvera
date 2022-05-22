package com.silvera.User.config;

import com.silvera.User.auth.CustomAuthenticationManager;
import com.silvera.User.auth.TokenAuthenticationFilter;
import com.silvera.User.utils.TokenUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.BeanIds;
import org.springframework.security.config.annotation.method.configuration.EnableGlobalMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class WebSecurityConfig {

    @Autowired
    private TokenUtils jwtTokenUtils;

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
                // disable CSRF as we do not serve browser clients
                .csrf().disable()

                // add JWT authorization filter
                .addFilter(new TokenAuthenticationFilter(new CustomAuthenticationManager(), jwtTokenUtils))

                // allow access restriction using request matcher
                .authorizeRequests()
                // allow all other requests
                .anyRequest().permitAll().and()
                // make sure we use stateless session, session will not be used to store user's state
                .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS);
        return http.build();
    }

}