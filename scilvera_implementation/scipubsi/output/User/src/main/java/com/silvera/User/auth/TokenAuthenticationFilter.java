package com.silvera.User.auth;


import java.io.IOException;
import java.util.Collections;

import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;


import com.silvera.User.utils.TokenUtils;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.web.authentication.www.BasicAuthenticationFilter;
import org.springframework.web.filter.OncePerRequestFilter;

import io.jsonwebtoken.ExpiredJwtException;
public class TokenAuthenticationFilter extends BasicAuthenticationFilter {


    private UserDetailsService userDetailsService;

    private final TokenUtils jwtTokenUtils;

    public TokenAuthenticationFilter(AuthenticationManager authManager, TokenUtils tokenUtils) {
        super(authManager);
        this.jwtTokenUtils = tokenUtils;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res, FilterChain chain) throws IOException, ServletException {

        // retrieve request authorization header
        final String authorizationHeader = req.getHeader("Authorization");

        // authorization header must be set and start with Bearer
        if (authorizationHeader != null && authorizationHeader.startsWith("Bearer ")) {



            final String username = jwtTokenUtils.getUsernameFromToken(authorizationHeader);

            // if user e-mail has been retrieved correctly from the token and if user is not already authenticated
            if (username != null && SecurityContextHolder.getContext().getAuthentication() == null) {

                // authenticate user
                final UsernamePasswordAuthenticationToken authentication = new UsernamePasswordAuthenticationToken(username, null);

                // set authentication in security context holder
                SecurityContextHolder.getContext().setAuthentication(authentication);

            }
        }
        // no token specified
        else {
            res.setStatus(HttpServletResponse.SC_BAD_REQUEST);
        }

        // pass request down the chain, except for OPTIONS requests
        if (!"OPTIONS".equalsIgnoreCase(req.getMethod())) {
            chain.doFilter(req, res);
        }

    }

}