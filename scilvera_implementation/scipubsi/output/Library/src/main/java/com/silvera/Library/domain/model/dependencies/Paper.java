package com.silvera.Library.domain.model.dependencies;


import org.springframework.data.annotation.Id;
import javax.validation.constraints.*;
public class Paper {


    @Id

    @NotNull(message="Field 'id' is mandatory!")
    private java.lang.Integer id;


    @NotBlank(message="Field 'author' cannot be empty!")
    private java.lang.String author;

    private java.lang.String title;

    private java.util.List<Section> sections= java.util.Collections.emptyList();



    public java.lang.Integer getId() {
        return this.id;
    }

    public void setId(java.lang.Integer id) {
        this.id = id;
    }

    public java.lang.String getAuthor() {
        return this.author;
    }

    public void setAuthor(java.lang.String author) {
        this.author = author;
    }

    public java.lang.String getTitle() {
        return this.title;
    }

    public void setTitle(java.lang.String title) {
        this.title = title;
    }

    public java.util.List<Section> getSections() {
        return this.sections;
    }

    public void setSections(java.util.List<Section> sections) {
        this.sections = sections;
    }





}