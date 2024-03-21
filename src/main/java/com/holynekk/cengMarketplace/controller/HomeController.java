package com.holynekk.cengMarketplace.controller;

import com.holynekk.cengMarketplace.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController {

  @Autowired private UserRepository userRepository;

  @GetMapping("/")
  public String home() {
    return "index.html";
  }
}
