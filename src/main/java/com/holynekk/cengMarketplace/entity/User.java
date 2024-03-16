package com.holynekk.cengMarketplace.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@Document
public class User {

  @Id private String id;

  @Field private String username;

  public User() {}

  public User(String username) {
    this.username = username;
  }

  public String getRno() {
    return id;
  }

  public void setRno(String rno) {
    this.id = rno;
  }

  public String getUsername() {
    return username;
  }

  public void setUsername(String username) {
    this.username = username;
  }
}
