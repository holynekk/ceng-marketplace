package com.holynekk.cengMarketplace.controller;

import com.holynekk.cengMarketplace.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/admin")
public class AdminController {

  @Autowired private UserRepository userRepository;

  @GetMapping("/users")
  public String getUsers(Model model, @AuthenticationPrincipal UserDetails userDetails) {

    userDetails.getUsername();
    model.addAttribute("users", userRepository.findAll());
    return "userManagement.html";
  }
}
