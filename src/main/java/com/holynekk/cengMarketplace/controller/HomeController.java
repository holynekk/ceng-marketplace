package com.holynekk.cengMarketplace.controller;

import com.holynekk.cengMarketplace.entity.Category;
import com.holynekk.cengMarketplace.repository.CategoryRepository;
import com.holynekk.cengMarketplace.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;

@Controller
public class HomeController {

  @Autowired private UserRepository userRepository;
  @Autowired private CategoryRepository categoryRepository;

  @GetMapping("/")
  public String home(Model model) {
    List<Category> categories =
        categoryRepository.findAll(Sort.by(Sort.Direction.ASC, "name"));
    model.addAttribute("categories", categories);
    return "index.html";
  }
}
