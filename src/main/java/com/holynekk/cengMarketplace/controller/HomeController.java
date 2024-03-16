package com.holynekk.cengMarketplace.controller;

import com.holynekk.cengMarketplace.entity.User;
import com.holynekk.cengMarketplace.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController {

  @Autowired private UserRepository userRepository;

  @GetMapping("/")
  public String home() {
    if (userRepository.findAll().isEmpty()) {
      userRepository.save(new User("mertknylmz"));
      userRepository.save(new User("holynekk"));
      userRepository.save(new User("m3rt_k44n"));
    }
    System.out.println(userRepository.findAll().get(0));
    return "index.html";
  }
}
