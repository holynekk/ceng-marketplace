package com.holynekk.cengMarketplace.repository;

import com.holynekk.cengMarketplace.entity.Category;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface CategoryRepository extends MongoRepository<Category, String> {

  List<Category> findAll(Sort sort);
}
