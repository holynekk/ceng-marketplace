package com.holynekk.cengMarketplace.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.DBRef;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.time.LocalDateTime;

@Document(collection = "products")
public class Product {
  @Id private String id;
  @DBRef private User owner;
  @Field private String title;
  @Field private double price;
  @Field private String imageLink;
  @Field private String description;
  @DBRef private Category category;
  @Field private LocalDateTime updatedAt;
  @Field private LocalDateTime createdAt;

  public Product() {}

  public Product(
      User owner,
      String title,
      double price,
      String imageLink,
      String description,
      Category category,
      LocalDateTime updatedAt,
      LocalDateTime createdAt) {
    this.owner = owner;
    this.title = title;
    this.price = price;
    this.imageLink = imageLink;
    this.description = description;
    this.category = category;
    this.updatedAt = updatedAt;
    this.createdAt = createdAt;
  }

  public String getId() {
    return id;
  }

  public void setId(String id) {
    this.id = id;
  }

  public User getOwner() {
    return owner;
  }

  public void setOwner(User owner) {
    this.owner = owner;
  }

  public String getTitle() {
    return title;
  }

  public void setTitle(String title) {
    this.title = title;
  }

  public double getPrice() {
    return price;
  }

  public void setPrice(double price) {
    this.price = price;
  }

  public String getImageLink() {
    return imageLink;
  }

  public void setImageLink(String imageLink) {
    this.imageLink = imageLink;
  }

  public String getDescription() {
    return description;
  }

  public void setDescription(String description) {
    this.description = description;
  }

  public Category getCategory() {
    return category;
  }

  public void setCategory(Category category) {
    this.category = category;
  }

  public LocalDateTime getUpdatedAt() {
    return updatedAt;
  }

  public void setUpdatedAt(LocalDateTime updatedAt) {
    this.updatedAt = updatedAt;
  }

  public LocalDateTime getCreatedAt() {
    return createdAt;
  }

  public void setCreatedAt(LocalDateTime createdAt) {
    this.createdAt = createdAt;
  }
}
