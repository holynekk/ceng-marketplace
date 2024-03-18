package com.holynekk.cengMarketplace.controller;

import com.holynekk.cengMarketplace.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.core.oidc.user.OidcUser;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController {

  @Autowired private UserRepository userRepository;

  @GetMapping("/")
  public String home() {
    return "index.html";
  }

  @GetMapping("/profile")
  public String profile(Model model, @AuthenticationPrincipal OidcUser oidcUser) {
    model.addAttribute("profile", oidcUser.getClaims());
    return "profile.html";
  }
}
