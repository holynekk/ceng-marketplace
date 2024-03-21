package com.holynekk.cengMarketplace.controller;

import com.holynekk.cengMarketplace.entity.User;
import com.holynekk.cengMarketplace.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/users")
public class UserController {

    @Autowired
    private UserService userService;

    @GetMapping("/login")
    public String getLoginPage() {
        return "login.html";
    }

    @GetMapping("/signup")
    public String getSignUpPage(Model model) {
        model.addAttribute("user", new User());
        return "signup.html";
    }

    @PostMapping("/signup")
    public String createUser(@ModelAttribute User user) {
        System.out.println("heeey");
        userService.createUser(user);
        return "redirect:/users/login?success";
    }


    @GetMapping("/profile")
    public String getProfile() {
        return "profile.html";
    }
}
