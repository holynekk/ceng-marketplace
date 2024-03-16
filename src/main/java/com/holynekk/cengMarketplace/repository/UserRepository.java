package com.holynekk.cengMarketplace.repository;

import com.holynekk.cengMarketplace.entity.User;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UserRepository extends MongoRepository<User, String> {}
