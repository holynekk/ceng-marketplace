package com.holynekk.cengMarketplace.service;

import org.springframework.beans.factory.annotation.Autowired;
import com.holynekk.cengMarketplace.entity.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class CustomUserDetailsService implements UserDetailsService {

  @Autowired private UserService userService;

  @Override
  public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {
    Optional<User> optUser = userService.findByEmail(email);

    if (optUser.isEmpty()) {
      return null;
    }
    User user = optUser.get();
    return org.springframework.security.core.userdetails.User.builder()
        .username(user.getEmail())
        .password(user.getPassword())
        .roles(user.getRole())
        .build();
  }
}
