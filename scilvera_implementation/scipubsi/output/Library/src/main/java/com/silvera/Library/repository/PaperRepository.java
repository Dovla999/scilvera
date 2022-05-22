package com.silvera.Library.repository;

import com.silvera.Library.domain.model.Paper;
import org.springframework.data.mongodb.repository.MongoRepository;


public interface PaperRepository extends MongoRepository<Paper, java.lang.Integer> {
    // CRUD operations are included in MongoRepository interface

}