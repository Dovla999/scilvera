package com.silvera.EntryGateway;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;

import org.springframework.cloud.client.discovery.EnableDiscoveryClient;



@SpringBootApplication

@EnableDiscoveryClient
public class App {

  public static void main(String[] args) {
    SpringApplication.run(App.class, args);
  }

  @Bean
  public RouteLocator gatewayRoutes(RouteLocatorBuilder routeLocatorBuilder)
  {
    return routeLocatorBuilder.routes()
            .route("User", rt -> rt.path("/api/u/**")
                    .filters(f -> f.rewritePath("/api/u/(?<segment>.*)", "/${segment}"))
                    .uri("lb://User"))
    
            .route("Scipaper", rt -> rt.path("/api/s/**")
                    .filters(f -> f.rewritePath("/api/s/(?<segment>.*)", "/${segment}"))
                    .uri("lb://Scipaper"))
    
            .route("Library", rt -> rt.path("/api/l/**")
                    .filters(f -> f.rewritePath("/api/l/(?<segment>.*)", "/${segment}"))
                    .uri("lb://Library"))
    
            .build();
  }

}