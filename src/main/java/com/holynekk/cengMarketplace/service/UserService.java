package com.holynekk.cengMarketplace.service;

import com.holynekk.cengMarketplace.entity.User;
import com.holynekk.cengMarketplace.entity.UserRole;
import com.holynekk.cengMarketplace.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class UserService {

  private final PasswordEncoder passwordEncoder;
  @Autowired private UserRepository userRepository;

  public UserService(PasswordEncoder passwordEncoder) {
    this.passwordEncoder = passwordEncoder;
  }

  public void createUser(User user) {
    user.setRole(UserRole.REGULAR.name());
    user.setPassword(passwordEncoder.encode(user.getPassword()));
    userRepository.save(user);
  }

  public List<User> findAll() {
    return userRepository.findAll();
  }

  public Optional<User> findByEmail(String email) {
    return userRepository.findByEmail(email);
  }
}
